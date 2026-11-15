import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.connection import Base
from app.api.usage import get_db
from app.services.pricing import calculate_cost
from app.models.usage_db import UsageRecord
from app.models.plan_db import CustomerPlan
import app.api.stripe_billing as stripe_billing
from app.models.stripe_event_db import StripeEvent

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "LLM Usage Metering & Billing Service is running"
    }


def test_usage_endpoint(client):
    response = client.post(
        "/usage",
        json={
            "customer_id": "test_customer",
            "model": "gpt-4o",
            "input_tokens": 1000,
            "output_tokens": 500,
            "idempotency_key": "test-usage-001",
        },
    )

    assert response.status_code == 200

    data = response.json()
    usage = data["usage"]

    assert data["message"] == "Usage recorded successfully"
    assert usage["customer_id"] == "test_customer"
    assert usage["cost"] == pytest.approx(0.0125)
    assert usage["cost_microdollars"] == 12500
    assert "id" in usage


def test_billing_endpoint(client):
    response = client.post(
        "/usage",
        json={
            "customer_id": "billing_test_customer",
            "model": "gpt-4o",
            "input_tokens": 1000,
            "output_tokens": 500,
            "idempotency_key": "test-billing-001",
        },
    )

    assert response.status_code == 200

    billing_response = client.get(
        "/billing/billing_test_customer"
    )

    assert billing_response.status_code == 200

    billing = billing_response.json()

    assert billing["customer_id"] == "billing_test_customer"
    assert billing["total_requests"] == 1
    assert billing["total_input_tokens"] == 1000
    assert billing["total_output_tokens"] == 500
    assert billing["total_cost"] == pytest.approx(0.0125)
    assert billing["total_cost_microdollars"] == 12500


def test_gpt4o_pricing():
    cost = calculate_cost("gpt-4o", 2000, 500)
    assert cost == 17500


def test_claude_pricing():
    cost = calculate_cost("claude-sonnet-5", 2000, 500)
    assert cost == 9000


def test_unsupported_model():
    with pytest.raises(ValueError, match="Unsupported model"):
        calculate_cost("unknown-model", 2000, 500)


def test_cached_input_pricing():
    cost = calculate_cost(
        "gpt-4o",
        input_tokens=1000,
        output_tokens=0,
        cached_input_tokens=1000,
    )

    assert cost == 2500


def test_reasoning_tokens_are_not_double_charged():
    normal = calculate_cost("gpt-4o", 1000, 500)

    with_reasoning = calculate_cost(
        "gpt-4o",
        input_tokens=1000,
        output_tokens=500,
        reasoning_tokens=300,
    )

    assert with_reasoning == normal


def test_cached_input_cannot_exceed_input():
    with pytest.raises(ValueError, match="Cached input tokens"):
        calculate_cost(
            "gpt-4o",
            input_tokens=100,
            output_tokens=0,
            cached_input_tokens=101,
        )


def test_reasoning_tokens_cannot_exceed_output():
    with pytest.raises(ValueError, match="Reasoning tokens"):
        calculate_cost(
            "gpt-4o",
            input_tokens=100,
            output_tokens=50,
            reasoning_tokens=51,
        )


def test_negative_tokens():
    with pytest.raises(
        ValueError,
        match="input_tokens must be a non-negative integer",
    ):
        calculate_cost("gpt-4o", -100, 500)


def test_duplicate_usage_not_charged_twice(client):
    payload = {
        "customer_id": "idempotency_test_customer",
        "model": "gpt-4o",
        "input_tokens": 1000,
        "output_tokens": 500,
        "idempotency_key": "duplicate-test-001",
    }

    first = client.post("/usage", json=payload)
    second = client.post("/usage", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["message"] == "Usage recorded successfully"
    assert second.json()["message"] == "Usage already recorded"

    billing = client.get(
        "/billing/idempotency_test_customer"
    ).json()

    assert billing["total_requests"] == 1
    assert billing["total_cost"] == pytest.approx(0.0125)
    assert billing["total_cost_microdollars"] == 12500


def test_same_idempotency_key_with_different_payload_returns_409(client):
    payload = {
        "customer_id": "idempotency_conflict_customer",
        "model": "gpt-4o",
        "input_tokens": 100,
        "output_tokens": 50,
        "idempotency_key": "same-key",
    }

    first = client.post("/usage", json=payload)
    changed_payload = {**payload, "output_tokens": 60}
    second = client.post("/usage", json=changed_payload)

    assert first.status_code == 200
    assert second.status_code == 409


def test_free_plan_token_quota_exceeded(client):
    response = client.post(
        "/usage",
        json={
            "customer_id": "quota_test_customer",
            "model": "gpt-4o",
            "input_tokens": 100000,
            "output_tokens": 1,
            "idempotency_key": "quota-test-001",
        },
    )

    assert response.status_code == 429
    assert "token quota exceeded" in response.json()["detail"].lower()


def test_free_plan_api_call_quota_exceeded(client):
    db = TestingSessionLocal()

    try:
        for i in range(1000):
            db.add(
                UsageRecord(
                    customer_id="api_quota_customer",
                    idempotency_key=f"api-quota-{i}",
                    model="gpt-4o",
                    input_tokens=1,
                    cached_input_tokens=0,
                    output_tokens=1,
                    reasoning_tokens=0,
                    cost_microdollars=10,
                )
            )

        db.commit()
    finally:
        db.close()

    response = client.post(
        "/usage",
        json={
            "customer_id": "api_quota_customer",
            "model": "gpt-4o",
            "input_tokens": 1,
            "output_tokens": 1,
            "idempotency_key": "api-quota-extra",
        },
    )

    assert response.status_code == 429
    assert "api call quota exceeded" in response.json()["detail"].lower()


def test_pro_plan_allows_usage_above_free_token_limit(client):
    db = TestingSessionLocal()

    try:
        db.add(
            CustomerPlan(
                customer_id="pro_quota_customer",
                plan_name="pro",
            )
        )
        db.commit()
    finally:
        db.close()

    response = client.post(
        "/usage",
        json={
            "customer_id": "pro_quota_customer",
            "model": "gpt-4o",
            "input_tokens": 100001,
            "output_tokens": 0,
            "idempotency_key": "pro-quota-test-001",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Usage recorded successfully"


def test_cached_and_reasoning_tokens_are_recorded_without_double_counting(client):
    response = client.post(
        "/usage",
        json={
            "customer_id": "token_category_customer",
            "model": "gpt-4o",
            "input_tokens": 1000,
            "cached_input_tokens": 400,
            "output_tokens": 500,
            "reasoning_tokens": 200,
            "idempotency_key": "token-category-001",
        },
    )

    assert response.status_code == 200

    usage = response.json()["usage"]

    assert usage["cached_input_tokens"] == 400
    assert usage["reasoning_tokens"] == 200

    billing = client.get(
        "/billing/token_category_customer"
    ).json()

    # Cached input and reasoning are subsets, not additional tokens.
    assert (
        billing["total_input_tokens"]
        + billing["total_output_tokens"]
        == 1500
    )

def test_duplicate_stripe_webhook_event_is_ignored(client, monkeypatch):
    app.dependency_overrides[stripe_billing.get_db] = override_get_db
    monkeypatch.setattr(
        stripe_billing,
        "STRIPE_WEBHOOK_SECRET",
        "whsec_test_secret",
    )
    monkeypatch.setattr(
        stripe_billing.stripe.Webhook,
        "construct_event",
        lambda payload, signature, secret: {
            "id": "evt_duplicate_test",
            "type": "checkout.session.completed",
        },
    )

    db = TestingSessionLocal()
    try:
        db.add(
            StripeEvent(
                stripe_event_id="evt_duplicate_test",
                event_type="checkout.session.completed",
            )
        )
        db.commit()
    finally:
        db.close()

    response = client.post(
        "/webhooks/stripe",
        content=b"{}",
        headers={"stripe-signature": "test_signature"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Event already processed"}


def test_pro_plan_api_call_quota_exceeded(client):
    db = TestingSessionLocal()

    try:
        db.add(
            CustomerPlan(
                customer_id="pro_api_quota_customer",
                plan_name="pro",
            )
        )

        for i in range(10000):
            db.add(
                UsageRecord(
                    customer_id="pro_api_quota_customer",
                    idempotency_key=f"pro-api-quota-{i}",
                    model="gpt-4o",
                    input_tokens=1,
                    cached_input_tokens=0,
                    output_tokens=1,
                    reasoning_tokens=0,
                    cost_microdollars=10,
                )
            )

        db.commit()
    finally:
        db.close()

    response = client.post(
        "/usage",
        json={
            "customer_id": "pro_api_quota_customer",
            "model": "gpt-4o",
            "input_tokens": 1,
            "output_tokens": 1,
            "idempotency_key": "pro-api-quota-extra",
        },
    )

    assert response.status_code == 429
    assert "api call quota exceeded" in response.json()["detail"].lower()
