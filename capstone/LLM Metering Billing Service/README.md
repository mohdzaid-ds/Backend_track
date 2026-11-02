# LLM Usage Metering & Billing Service

## Overview

A FastAPI backend service that tracks customer API usage, calculates usage costs, enforces plan-based quotas, and integrates Stripe subscriptions in test mode.

The service supports Free and Pro plans. AI token usage is simulated, so the application does not need to make real AI model calls.

## Features

- Record simulated API and AI token usage.
- Calculate usage costs using model pricing configuration.
- Prevent duplicate usage events through idempotency keys.
- Enforce monthly API-call and token quotas for Free and Pro plans.
- Aggregate usage and costs for individual customers.
- Create Stripe Checkout sessions for Pro subscriptions.
- Process Stripe subscription webhook events.
- Track customer plans, subscriptions, usage records, and processed Stripe events in SQLite.
- Test application behavior with Pytest.

## Architecture

```text
Client
  |
  v
FastAPI Application
  |
  +--> Usage API
  |      |
  |      +--> Input Validation
  |      +--> Idempotency Checks
  |      +--> Quota Enforcement
  |      +--> Cost Calculation
  |      +--> Usage Records
  |
  +--> Billing API
  |      |
  |      +--> Usage Aggregation
  |      +--> Customer Plan
  |
  +--> Stripe Integration
         |
         +--> Checkout Sessions
         +--> Webhook Verification
         +--> Subscription Status
         +--> Customer Plan Updates

                |
                v
          SQLite Database
```

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Stripe Python SDK and Stripe CLI
- Pytest

## Project Structure

```text
capstone-metering-billing/
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── database/
│   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── capstone.yaml
├── DESIGN.md
├── EVIDENCE.md
├── BUILDLOG.md
├── requirements.txt
└── README.md
```

The structure above is representative. Keep the actual directory and file names in the repository consistent with your project.

## Requirements

- Python installed on Windows.
- Project dependencies listed in `requirements.txt`.
- Stripe account and test-mode credentials for subscription testing.
- Stripe CLI for forwarding test webhook events to the local application.

## Setup

Run these commands in PowerShell from the project directory.

### 1. Activate the virtual environment

If the virtual environment already exists:

```powershell
.\venv\Scripts\Activate.ps1
```

If you have not created one yet:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a local `.env` file using `.env.example` as a reference.

Configure the Stripe test-mode variables required by the application:

- `STRIPE_SECRET_KEY`
- `STRIPE_PRO_PRICE_ID`
- `STRIPE_SUCCESS_URL`
- `STRIPE_CANCEL_URL`
- `STRIPE_WEBHOOK_SECRET`

Use your own Stripe test credentials and configured Pro Price ID. The webhook signing secret is provided by Stripe CLI when you start a local webhook listener.

Do not commit `.env` or publish actual credentials. Keep `.env.example` limited to safe placeholder values.

### 4. Start the application

```powershell
uvicorn app.main:app --reload
```

The local API should be available at:

`http://127.0.0.1:8000`

### 5. Open the API documentation

Open Swagger UI in your browser:

`http://127.0.0.1:8000/docs`

Use Swagger UI to inspect available endpoints and submit test requests.

## Main API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/usage` | Record a usage event |
| GET | `/billing/{customer_id}` | Retrieve a customer's usage and cost summary |
| POST | `/billing/checkout` | Create a Stripe Checkout session |
| POST | `/webhooks/stripe` | Receive Stripe webhook events |

Confirm these routes against the running application and Swagger UI before submission.

## Usage Example

Send a simulated usage event to `POST /usage`:

```json
{
  "customer_id": "example_customer",
  "model": "gpt-4o",
  "input_tokens": 1000,
  "output_tokens": 500,
  "idempotency_key": "example-usage-001"
}
```

Use a unique idempotency key for each distinct usage event. Reusing a key should not create an additional charge for the same event.

The accepted request fields and validation rules are defined by the application's request schema.

## Billing and Quotas

The service supports Free and Pro subscription plans with the following intended monthly limits:

| Plan | API calls per month | AI tokens per month |
|---|---:|---:|
| Free | 1,000 | 100,000 |
| Pro | 10,000 | 1,000,000 |

Usage is associated with a customer, checked against the applicable quota, and aggregated into a customer-level usage and cost summary.

Cost calculations use the application's configured model pricing. Verify the pricing values, token categories, monthly usage-window behavior, and monetary precision against the assignment specification before treating these requirements as fully verified.

## Stripe Test-Mode Integration

The service supports Stripe Checkout for Pro subscriptions and processes subscription-related webhook events.

The intended webhook events include:

- `checkout.session.completed`
- `customer.subscription.updated`
- `customer.subscription.deleted`

For local webhook testing:

1. Start the FastAPI application.
2. Start Stripe CLI in another PowerShell terminal.
3. Forward the required events to the local webhook endpoint.
4. Configure the webhook signing secret provided by Stripe CLI in your local `.env`.
5. Complete a Stripe Checkout test flow and verify that the subscription and customer plan are updated.

Example Stripe CLI command:

```powershell
stripe listen --events "checkout.session.completed,customer.subscription.updated,customer.subscription.deleted" --forward-to http://localhost:8000/webhooks/stripe
```

Use test-mode credentials only. Webhook signatures should be verified, and duplicate events should not be processed more than once.

## Running Tests

With the virtual environment activated, run:

```powershell
python -m pytest -v
```

The latest reported test run completed with **19 passed and 1 warning**.

The test suite covers API behavior, pricing, input validation, idempotency, and quota enforcement. A passing test suite does not, by itself, establish that every assignment requirement has been verified.

## Limitations

- AI token usage is simulated; no real AI model calls are made.
- Local development uses SQLite.
- Stripe integration is intended for test-mode verification.
- The project is a capstone implementation, not a complete production billing platform.

## Project Status

The latest reported automated test run passed 19 tests with one deprecation warning.

Stripe Checkout and subscription webhook processing have also been tested during development. Refer to `EVIDENCE.md` for recorded verification results and outstanding checks, and `BUILDLOG.md` for the development and AI-assistance log.

Before submission, verify the remaining requirements against the assignment specification, including pricing calculations, monthly usage aggregation, quota enforcement, Stripe webhook behavior, and the required evidence.
