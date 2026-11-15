from fastapi import FastAPI
from app.api.usage import router as usage_router
from app.database.connection import Base, engine
from app.models.usage_db import UsageRecord
from app.models.plan_db import CustomerPlan
from app.models.subscription_db import Subscription
from app.models.stripe_event_db import StripeEvent
from app.api.stripe_billing import router as stripe_billing_router
from app.api.stripe_billing import webhook_router
from fastapi import APIRouter

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LLM Usage Metering & Billing Service",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "LLM Usage Metering & Billing Service is running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
app.include_router(usage_router)
app.include_router(stripe_billing_router)
app.include_router(webhook_router)
