
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.connection import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(
        String,
        nullable=True,
        unique=True,
    )
    plan_name = Column(String, nullable=False, default="free")
    status = Column(String, nullable=False, default="inactive")
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
