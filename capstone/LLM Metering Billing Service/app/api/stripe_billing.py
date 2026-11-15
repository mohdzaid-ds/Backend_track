
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.stripe_event_db import StripeEvent
from app.models.subscription_db import Subscription
from app.models.plan_db import CustomerPlan
from app.services.stripe_config import (
    STRIPE_SECRET_KEY,
    STRIPE_WEBHOOK_SECRET,
    STRIPE_PRO_PRICE_ID,
    STRIPE_SUCCESS_URL,
    STRIPE_CANCEL_URL,
)

# Stripe checkout routes
router = APIRouter(prefix="/billing", tags=["Stripe Billing"])

# Stripe webhook routes
webhook_router = APIRouter(tags=["Stripe Webhooks"])


class CheckoutRequest(BaseModel):
    customer_id: str = Field(min_length=1)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/checkout")
def create_checkout_session(request: CheckoutRequest):
    if (
        not STRIPE_SECRET_KEY
        or not STRIPE_PRO_PRICE_ID
        or STRIPE_SECRET_KEY.startswith("sk_test_replace")
        or STRIPE_PRO_PRICE_ID.startswith("price_replace")
    ):
        raise HTTPException(
            status_code=503,
            detail="Stripe test credentials are not configured.",
        )

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[
                {
                    "price": STRIPE_PRO_PRICE_ID,
                    "quantity": 1,
                }
            ],
            success_url=(
                STRIPE_SUCCESS_URL
                + "?session_id={CHECKOUT_SESSION_ID}"
            ),
            cancel_url=STRIPE_CANCEL_URL,
            client_reference_id=request.customer_id,
            metadata={"customer_id": request.customer_id},
            subscription_data={
                "metadata": {"customer_id": request.customer_id}
            },
        )

        return {
            "checkout_url": session.url,
            "session_id": session.id,
        }

    except stripe.StripeError as e:
        # Print the actual Stripe error in the FastAPI terminal.
        print(f"Stripe checkout error: {e}")

        raise HTTPException(
            status_code=502,
            detail="Unable to create the Stripe Checkout session.",
        )


@webhook_router.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=503,
            detail="Stripe webhook secret is not configured.",
        )

    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    if not signature:
        raise HTTPException(
            status_code=400,
            detail="Missing Stripe signature.",
        )

    # Verify the Stripe webhook signature.
    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            STRIPE_WEBHOOK_SECRET,
        )
    except (ValueError, stripe.SignatureVerificationError):
        raise HTTPException(
            status_code=400,
            detail="Invalid Stripe webhook payload or signature.",
        )

    event_id = event["id"]
    event_type = event["type"]

    # Prevent processing the same event twice.
    existing_event = (
        db.query(StripeEvent)
        .filter(StripeEvent.stripe_event_id == event_id)
        .first()
    )

    if existing_event:
        return {"message": "Event already processed"}

    obj = event["data"]["object"]
    customer_id = None
    obj = obj.to_dict()
    stripe_customer_id = obj.get("customer")
    stripe_subscription_id = None
    status = None

    if event_type == "checkout.session.completed":
        customer_id = (
            obj.get("client_reference_id")
            or (obj.get("metadata") or {}).get("customer_id")
        )
        stripe_subscription_id = obj.get("subscription")
        status = "active"

    elif event_type in (
        "customer.subscription.updated",
        "customer.subscription.deleted",
    ):
        stripe_subscription_id = obj.get("id")
        metadata = obj.get("metadata") or {}
        customer_id = metadata.get("customer_id")

        if not customer_id and stripe_subscription_id:
            existing_subscription = (
                db.query(Subscription)
                .filter(
                    Subscription.stripe_subscription_id
                    == stripe_subscription_id
                )
                .first()
            )

            if existing_subscription:
                customer_id = existing_subscription.customer_id

        status = (
            "canceled"
            if event_type == "customer.subscription.deleted"
            else obj.get("status", "inactive")
        )

    if customer_id:
        subscription = (
            db.query(Subscription)
            .filter(Subscription.customer_id == customer_id)
            .first()
        )

        if not subscription:
            subscription = Subscription(
                customer_id=customer_id,
                plan_name="free",
                status="inactive",
            )
            db.add(subscription)

        subscription.stripe_customer_id = stripe_customer_id
        subscription.stripe_subscription_id = (
            stripe_subscription_id
            or subscription.stripe_subscription_id
        )
        subscription.status = status or subscription.status

        plan_name = (
            "pro"
            if subscription.status in ("active", "trialing")
            else "free"
        )
        subscription.plan_name = plan_name

        customer_plan = (
            db.query(CustomerPlan)
            .filter(CustomerPlan.customer_id == customer_id)
            .first()
        )

        if not customer_plan:
            customer_plan = CustomerPlan(
                customer_id=customer_id,
                plan_name=plan_name,
            )
            db.add(customer_plan)
        else:
            customer_plan.plan_name = plan_name

    # Record the event after processing it.
    db.add(
        StripeEvent(
            stripe_event_id=event_id,
            event_type=event_type,
        )
    )

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Stripe webhook database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Unable to process Stripe webhook event.",
        )

    return {"message": "Stripe event processed successfully"}
