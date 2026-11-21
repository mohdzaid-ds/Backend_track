# Usage Metering & Billing Engine — Design

## 1. Problem

SaaS applications need to track how much each customer uses the service,
enforce usage limits based on their subscription plan, calculate usage costs,
and keep subscription status synchronized with the payment provider.

This project will build a backend service that provides these capabilities
using usage metering, quota enforcement, cost calculation, and Stripe
test-mode subscriptions.

The system will support multiple tenants, with each tenant having a
subscription plan and its own isolated usage data.

## 2. Plans

The system will initially support two plans.

### Free

- API calls: 1,000 per month
- AI tokens: 100,000 per month

### Pro

- API calls: 10,000 per month
- AI tokens: 1,000,000 per month

The plan limits will be stored in the database and treated as configurable
values rather than hard-coded rules in route handlers.

## 3. Usage Types

The system will meter two types of usage:

1. API calls
2. AI tokens

AI token usage will be simulated. The system does not need to call an actual
AI model.

Each successful billable action will create exactly one usage event. A
rejected request will not create a billable usage event.

## 4. Data Model

### Tenant

Represents a customer organization.

Fields:

- id
- name
- created_at

### Plan

Represents a subscription plan.

Fields:

- id
- name
- api_call_limit
- token_limit

### Subscription

Connects a tenant to a plan and stores subscription information.

Fields:

- id
- tenant_id
- plan_id
- stripe_customer_id
- stripe_subscription_id
- status
- created_at
- updated_at

A tenant's effective plan and subscription status will be determined from
the persisted subscription record. The application will not treat a
successful Checkout redirect alone as proof that a subscription is active.

### Usage Event

Represents one billable usage event.

Fields:

- id
- tenant_id
- usage_type
- quantity
- idempotency_key
- created_at

The database will enforce uniqueness for the combination of tenant_id and
idempotency_key. This protects against duplicate events even if identical
requests arrive concurrently.

### Stripe Event

Stores processed Stripe webhook events so that the same event cannot be
processed more than once.

Fields:

- id
- stripe_event_id
- event_type
- processed_at

The stripe_event_id field will have a database uniqueness constraint.

### Database and migrations

PostgreSQL will be the application database. Database schema changes will
be managed through migrations instead of relying on automatic table creation
as the production schema-management strategy.

Foreign keys and indexes will be added for relationships and common queries,
including tenant-scoped usage lookups and idempotency checks.

Money will be stored as integer units, not floating-point values. The
selected unit and conversion rules will be documented alongside pricing
configuration.

## 5. API Surface

The initial API will contain the following endpoints.

### Health

`GET /health`

Checks whether the service is running.

### Tenant

`POST /tenants`

Creates a tenant for testing and demonstration. The response will provide
the tenant identifier needed for subsequent requests.

### Generate

`POST /generate`

Represents a billable action.

The endpoint will:

1. Identify the tenant from the request.
2. Validate the requested usage and usage type.
3. Check whether the idempotency key has already been processed.
4. If it is a duplicate, return the stored result without recording usage again.
5. Determine the tenant's current plan and monthly usage.
6. Reject the request if it would exceed the applicable quota.
7. Atomically record the allowed usage event and its idempotency key.
8. Return the usage result.

The database and transaction strategy must ensure that concurrent requests
cannot bypass quota checks or create duplicate usage events.

### Usage

`GET /usage`

Returns the authenticated or explicitly identified tenant's usage for the
current billing month, applicable quota limits, and calculated cost.

Every query must be scoped to the intended tenant. The API must not expose
another tenant's records.

### Checkout

`POST /billing/checkout`

Creates a Stripe Checkout session for upgrading a tenant to the Pro plan.
The integration will use Stripe test mode only.

### Stripe Webhook

`POST /webhooks/stripe`

Receives Stripe events, verifies their signatures using the configured
webhook secret, prevents duplicate processing, and synchronizes the tenant's
subscription status.

## 6. Idempotency Strategy

Every billable request will require an idempotency key.

The idempotency key will uniquely identify a billable request for a tenant.
The same key used by a different tenant will be treated as a separate key.

Flow:

1. Validate the request and tenant.
2. Look for an existing result for the tenant and idempotency key.
3. If found, return the previous result without creating another event.
4. If not found, check the quota.
5. Record the event and its key atomically.
6. Return the stored result.

A database uniqueness constraint on `(tenant_id, idempotency_key)` is
required. The implementation must handle a uniqueness conflict by retrieving
and returning the previously stored result. A simple application-level
check alone is not sufficient for concurrent requests.

The same key must not create more than one usage event. Reuse of a key with
a materially different request payload should be rejected with a clear
client error rather than silently charging for a different action.

## 7. Quota Enforcement

Quota will be checked before usage is recorded.

For each usage type, the system will calculate:

`current monthly usage + requested usage`

The request is allowed only when the resulting usage does not exceed the
applicable plan limit. A request that brings usage exactly to the limit is
allowed; a request that would exceed the limit is rejected.

The initial Free and Pro plan limits are defined in Section 2. The quota
period will be the calendar month in UTC, from the first instant of the
month up to, but not including, the first instant of the next month. Usage
queries and quota checks must use this same period definition.

Over-limit requests will return HTTP 429 with a clear message identifying
the exceeded quota and limit. HTTP 402 may be used for a distinct payment
or subscription-required condition, but the implementation will not use
402 interchangeably with ordinary rate/quota exhaustion.

Quota checking and usage recording must be performed transactionally so
concurrent requests cannot exceed a quota because of a race condition.

## 8. Cost Calculation

The system will calculate usage costs using pinned pricing constants stored
in configuration and documented with their source and effective date.

AI token pricing will distinguish between:

- Input tokens
- Cached input tokens
- Output tokens
- Reasoning tokens

Cached input tokens will use their explicitly configured lower rate.
Reasoning tokens will follow the output-token pricing rule required by the
assignment. The calculation must avoid counting the same token in multiple
categories.

Money will be represented using integer units rather than floating-point
values. The implementation will document the selected precision, use
integer arithmetic or a decimal-safe calculation for intermediate values,
and round only according to a documented rule.

Pricing tests will cover ordinary input, cached input, output and reasoning
tokens, including a known example with an exact expected total. The usage
endpoint will return totals calculated from persisted usage records.

## 9. Architecture

The application will use a layered backend architecture:

Client  
↓  
FastAPI Routes  
↓  
Service Layer

- Metering Service
- Quota Service
- Pricing Service
- Stripe Service

↓  
Database Layer  
↓  
PostgreSQL

Stripe will communicate with the application through the verified webhook
endpoint.

The HTTP/API layer will be separated from business logic and database
access. Request validation, business rules and persistence will not all be
implemented inside route handlers.

## 10. Stripe Integration

Stripe will only be used in test mode. Live-mode credentials must not be
used for this capstone.

The application will support:

- Stripe Checkout
- `checkout.session.completed`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- Webhook signature verification
- Webhook event deduplication
- Tenant subscription synchronization

The database will mirror Stripe subscription state only after receiving and
verifying valid webhook events. Duplicate webhook events must not apply the
same state change twice. Forged or invalidly signed webhook requests must
return HTTP 400 and must not change application data.

Stripe secrets and webhook secrets will be supplied through environment
variables. They must not be committed to Git or written to logs.

## 11. Tenant Isolation

Every usage event and subscription belongs to a specific tenant.

Usage data for one tenant must never be returned to another tenant. Every
usage, billing and subscription query will be scoped by tenant ID, and
relationships will be protected with database foreign keys where applicable.

Tenant identity must be validated by the API; a client-supplied tenant ID
must not be treated as proof of authorization in a production system. For
the demonstration API, the tenant-identification approach and its security
limitations will be documented explicitly.

## 12. Background Processing and Reliability

At least one background job will be included for work that should not block
an API request, such as processing queued billing or reconciliation work.

The job will have bounded retries for transient failures and a clear failure
signal or alert when retries are exhausted. Processing must be safe to retry
and must not create duplicate billable usage or duplicate Stripe-event
effects.

The chosen job mechanism and its operational limitations will be documented.

## 13. Testing and Acceptance Checks

Automated tests will cover at least:

1. Repeating a billable request with the same tenant and idempotency key
   creates one usage event and returns the prior result on the retry.
2. A request that brings usage exactly to its quota succeeds; the next
   request that exceeds the limit is rejected with the documented status.
3. A successful Stripe test Checkout followed by a verified webhook changes
   the tenant's plan, and `GET /usage` reports the new limits.
4. A forged webhook returns HTTP 400 and changes no data; replaying a valid
   event does not process it twice.
5. Pinned token-pricing rules calculate exact expected totals, including
   cached input and reasoning tokens.
6. Tenant-scoped queries do not expose another tenant's usage.
7. Invalid input returns a clear 4xx response rather than an unexpected 500.

## 14. Required Submission Files

The repository will include:

- `README.md` — project overview, architecture diagram, exact setup/run/seed
  steps, test instructions and known limitations.
- `capstone.yaml` — run command, seed command, optional test command,
  base URL and endpoints to probe.
- `EVIDENCE.md` — proof for each required metering, quota, pricing, Stripe
  and tenant-isolation behavior.
- `BUILDLOG.md` — honest record of where AI helped, incorrect suggestions
  encountered and changes made.
- `.env.example` — required environment variable names with safe placeholder
  values and no real secrets.

The `.env` file containing local secrets will be excluded by `.gitignore`.
The repository will be committed incrementally as features are implemented.

## 15. Explicit Non-Goal

Real AI model inference is not part of the core project.

AI token usage will be simulated so that the project focuses on usage
metering, quota enforcement, cost calculation, idempotency, and billing
integration.
