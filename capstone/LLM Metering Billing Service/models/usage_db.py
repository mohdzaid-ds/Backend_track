from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.sql import func

from app.database.connection import Base


class UsageRecord(Base):
    __tablename__ = "usage_records"

    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "idempotency_key",
            name="uq_usage_customer_idempotency",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        String,
        nullable=False,
        index=True,
    )

    # Nullable to preserve legacy records that predate idempotency keys.
    idempotency_key = Column(
        String(255),
        nullable=True,
    )

    model = Column(String, nullable=False)

    input_tokens = Column(Integer, nullable=False, default=0)
    cached_input_tokens = Column(
        Integer,
        nullable=False,
        default=0,
    )
    output_tokens = Column(Integer, nullable=False, default=0)
    reasoning_tokens = Column(
        Integer,
        nullable=False,
        default=0,
    )

    # Integer microdollars; 1 USD = 1,000,000 microdollars.
    cost_microdollars = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
