from pydantic import BaseModel, Field


class UsageEvent(BaseModel):
    customer_id: str = Field(min_length=1)
    model: str = Field(min_length=1)
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    cached_input_tokens: int = Field(default=0, ge=0)
    reasoning_tokens: int = Field(default=0, ge=0)
    idempotency_key: str = Field(min_length=1, max_length=255)
