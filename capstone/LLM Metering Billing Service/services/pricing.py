from decimal import Decimal, ROUND_HALF_UP

MICRODOLLARS_PER_DOLLAR = 1_000_000
TOKENS_PER_PRICING_UNIT = 1_000

# USD per 1,000 tokens.
# Cached input is priced at 50% of the standard input rate.
# These are project-configured example rates, not verified current provider prices.
PRICING = {
    "gpt-4o": {
        "input": Decimal("0.005"),
        "cached_input": Decimal("0.0025"),
        "output": Decimal("0.015"),
    },
    "claude-sonnet-5": {
        "input": Decimal("0.002"),
        "cached_input": Decimal("0.001"),
        "output": Decimal("0.010"),
    },
}


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cached_input_tokens: int = 0,
    reasoning_tokens: int = 0,
) -> int:
    """Return usage cost as integer microdollars."""

    if model not in PRICING:
        raise ValueError(f"Unsupported model: {model}")

    values = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cached_input_tokens": cached_input_tokens,
        "reasoning_tokens": reasoning_tokens,
    }

    for name, value in values.items():
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value < 0
        ):
            raise ValueError(
                f"{name} must be a non-negative integer"
            )

    if cached_input_tokens > input_tokens:
        raise ValueError(
            "Cached input tokens cannot exceed input tokens"
        )

    if reasoning_tokens > output_tokens:
        raise ValueError(
            "Reasoning tokens cannot exceed output tokens"
        )

    rates = PRICING[model]

    regular_input_tokens = input_tokens - cached_input_tokens

    input_cost = (
        Decimal(regular_input_tokens) * rates["input"]
        + Decimal(cached_input_tokens) * rates["cached_input"]
    ) / TOKENS_PER_PRICING_UNIT

    output_cost = (
        Decimal(output_tokens) * rates["output"]
    ) / TOKENS_PER_PRICING_UNIT

    total_microdollars = (
        (input_cost + output_cost)
        * MICRODOLLARS_PER_DOLLAR
    )

    return int(
        total_microdollars.quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )
    )
