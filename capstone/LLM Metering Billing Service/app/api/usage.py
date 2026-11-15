from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.usage import UsageEvent
from app.models.usage_db import UsageRecord
from app.models.plan_db import CustomerPlan
from app.services.pricing import calculate_cost
from app.services.quota import PLAN_LIMITS, DEFAULT_PLAN


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def month_start_utc():
    now = datetime.now(timezone.utc)
    return now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


def get_customer_plan(db: Session, customer_id: str) -> str:
    plan = (
        db.query(CustomerPlan)
        .filter(CustomerPlan.customer_id == customer_id)
        .first()
    )

    if not plan:
        return DEFAULT_PLAN

    plan_name = plan.plan_name.lower()

    if plan_name not in PLAN_LIMITS:
        return DEFAULT_PLAN

    return plan_name


def check_monthly_quota(
    db: Session,
    customer_id: str,
    requested_tokens: int,
):
    plan_name = get_customer_plan(db, customer_id)
    limits = PLAN_LIMITS[plan_name]
    start = month_start_utc()

    monthly_query = db.query(UsageRecord).filter(
        UsageRecord.customer_id == customer_id,
        UsageRecord.created_at >= start,
    )

    current_api_calls = monthly_query.count()

    current_tokens = (
        db.query(
            func.coalesce(
                func.sum(
                    UsageRecord.input_tokens
                    + UsageRecord.output_tokens
                ),
                0,
            )
        )
        .filter(
            UsageRecord.customer_id == customer_id,
            UsageRecord.created_at >= start,
        )
        .scalar()
        or 0
    )

    if current_api_calls + 1 > limits["monthly_api_calls"]:
        raise HTTPException(
            status_code=429,
            detail="Monthly API call quota exceeded",
        )

    if current_tokens + requested_tokens > limits["monthly_tokens"]:
        raise HTTPException(
            status_code=429,
            detail="Monthly token quota exceeded",
        )


def cost_in_dollars(cost_microdollars: int) -> float:
    # The database stores the cost as integer microdollars.
    return cost_microdollars / 1_000_000


def usage_response(record: UsageRecord) -> dict:
    return {
        "id": record.id,
        "customer_id": record.customer_id,
        "model": record.model,
        "input_tokens": record.input_tokens,
        "cached_input_tokens": record.cached_input_tokens,
        "output_tokens": record.output_tokens,
        "reasoning_tokens": record.reasoning_tokens,
        "cost": cost_in_dollars(record.cost_microdollars),
        "cost_microdollars": record.cost_microdollars,
        "idempotency_key": record.idempotency_key,
        "created_at": record.created_at,
    }


@router.post("/usage")
def record_usage(
    event: UsageEvent,
    db: Session = Depends(get_db),
):
    customer_id = event.customer_id.strip()

    if not customer_id:
        raise HTTPException(
            status_code=422,
            detail="customer_id cannot be blank",
        )

    # Check idempotency before quotas so retries are not charged twice.
    existing = (
        db.query(UsageRecord)
        .filter(
            UsageRecord.customer_id == customer_id,
            UsageRecord.idempotency_key == event.idempotency_key,
        )
        .first()
    )

    if existing:
        same_payload = (
            existing.model == event.model
            and existing.input_tokens == event.input_tokens
            and existing.cached_input_tokens == event.cached_input_tokens
            and existing.output_tokens == event.output_tokens
            and existing.reasoning_tokens == event.reasoning_tokens
        )

        if not same_payload:
            raise HTTPException(
                status_code=409,
                detail=(
                    "Idempotency key already used with "
                    "a different payload"
                ),
            )

        return {
            "message": "Usage already recorded",
            "usage": usage_response(existing),
        }

    try:
        cost_microdollars = calculate_cost(
            model=event.model,
            input_tokens=event.input_tokens,
            output_tokens=event.output_tokens,
            cached_input_tokens=event.cached_input_tokens,
            reasoning_tokens=event.reasoning_tokens,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # Cached input is included in input_tokens.
    # Reasoning tokens are included in output_tokens.
    # Do not count these subsets twice.
    requested_tokens = event.input_tokens + event.output_tokens

    check_monthly_quota(
        db=db,
        customer_id=customer_id,
        requested_tokens=requested_tokens,
    )

    record = UsageRecord(
        customer_id=customer_id,
        idempotency_key=event.idempotency_key,
        model=event.model,
        input_tokens=event.input_tokens,
        cached_input_tokens=event.cached_input_tokens,
        output_tokens=event.output_tokens,
        reasoning_tokens=event.reasoning_tokens,
        cost_microdollars=cost_microdollars,
    )

    try:
        db.add(record)
        db.commit()
        db.refresh(record)
    except Exception:
        db.rollback()

        # Handle a concurrent retry using the same idempotency key.
        existing = (
            db.query(UsageRecord)
            .filter(
                UsageRecord.customer_id == customer_id,
                UsageRecord.idempotency_key == event.idempotency_key,
            )
            .first()
        )

        if existing:
            same_payload = (
                existing.model == event.model
                and existing.input_tokens == event.input_tokens
                and existing.cached_input_tokens == event.cached_input_tokens
                and existing.output_tokens == event.output_tokens
                and existing.reasoning_tokens == event.reasoning_tokens
            )

            if same_payload:
                return {
                    "message": "Usage already recorded",
                    "usage": usage_response(existing),
                }

            raise HTTPException(
                status_code=409,
                detail=(
                    "Idempotency key already used with "
                    "a different payload"
                ),
            )

        raise

    return {
        "message": "Usage recorded successfully",
        "usage": usage_response(record),
    }


@router.get("/usage")
def list_usage(
    customer_id: str,
    db: Session = Depends(get_db),
):
    records = (
        db.query(UsageRecord)
        .filter(UsageRecord.customer_id == customer_id)
        .order_by(UsageRecord.id.desc())
        .all()
    )

    return {
        "customer_id": customer_id,
        "usage": [usage_response(record) for record in records],
    }


@router.get("/billing/{customer_id}")
def get_billing(
    customer_id: str,
    db: Session = Depends(get_db),
):
    start = month_start_utc()

    records = (
        db.query(UsageRecord)
        .filter(
            UsageRecord.customer_id == customer_id,
            UsageRecord.created_at >= start,
        )
        .all()
    )

    total_requests = len(records)
    total_input_tokens = sum(r.input_tokens for r in records)
    total_output_tokens = sum(r.output_tokens for r in records)
    total_cached_input_tokens = sum(
        r.cached_input_tokens for r in records
    )
    total_reasoning_tokens = sum(
        r.reasoning_tokens for r in records
    )
    total_cost_microdollars = sum(
        r.cost_microdollars for r in records
    )

    return {
        "customer_id": customer_id,
        "total_requests": total_requests,
        "total_input_tokens": total_input_tokens,
        "total_cached_input_tokens": total_cached_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_reasoning_tokens": total_reasoning_tokens,
        "total_cost": cost_in_dollars(total_cost_microdollars),
        "total_cost_microdollars": total_cost_microdollars,
    }
