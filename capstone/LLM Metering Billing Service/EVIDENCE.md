# Evidence — Usage Metering & Billing Engine

## 1. API Health

- **Endpoint:** `GET /health`
- **Evidence:** Automated health-check test.
- **Status:** Verified by passing automated test.

## 2. Usage Metering

- **Endpoint:** `POST /usage`
- **Evidence:** A simulated usage event was recorded for customer `zaidali123`.
- **Status:** Verified.
- **Note:** No real AI model call is required; token usage is simulated as specified by the assignment.

## 3. Billing Aggregation

- **Endpoint:** `GET /billing/zaidali123`
- **Evidence:** The endpoint returns usage totals and calculated cost for the customer.
- **Previously recorded example:** Total cost of `0.0125`.
- **Status:** Previously verified; recheck against the final pricing configuration and recorded usage before submission.

## 4. Model Pricing and Cost Calculation

- **Evidence:** Automated pricing tests for `gpt-4o` and `claude-sonnet-5`.
- **Status:** Both pricing tests previously passed.
- **Remaining verification:**
  - Confirm that the configured rates match the assignment specification.
  - Verify input-token, cached-input-token, output-token, and reasoning-token calculations.
  - Confirm that reasoning tokens are not charged twice when they are already included in output tokens.
  - Confirm that cached input uses its configured discounted rate.
  - Verify that cost storage uses integer-based monetary units rather than floating-point values.
  - Record the expected and actual results for representative pricing tests.

## 5. Idempotency

- **Evidence:** Automated tests for duplicate usage events and conflicting idempotency keys.
- **Status:** Previously reported as passing.
- **Remaining verification:** Confirm that retrying an identical request does not create a second charge and that reusing the same key with a different payload returns the expected conflict response.

## 6. Quota Enforcement

- **Evidence:** Automated tests for Free-plan API-call limits, Free-plan token limits, and Pro-plan usage.
- **Configured limits:**
  - Free: 1,000 API calls per month and 100,000 AI tokens per month.
  - Pro: 10,000 API calls per month and 1,000,000 AI tokens per month.
- **Status:** Related tests previously reported as passing.
- **Remaining verification:** Confirm that requests exceeding the applicable quota are rejected with the expected HTTP status and a clear error message, and that usage remains isolated by customer.

## 7. Stripe Test-Mode Subscription

- **Evidence:** Stripe test-mode Checkout and subscription records.
- **Previously verified result:** Customer `zaidali123` had a Pro plan and an active subscription.
- **Status:** Previously verified.
- **Remaining verification:**
  - Confirm that `checkout.session.completed` updates the customer's plan through a verified webhook.
  - Confirm that `customer.subscription.updated` synchronizes subscription status.
  - Confirm that `customer.subscription.deleted` updates the subscription appropriately.
  - Confirm that invalid webhook signatures are rejected.
  - Confirm that duplicate Stripe event IDs are ignored safely.
- **Security note:** Do not include Stripe secret keys, webhook signing secrets, or other credentials in this file.

## 8. Monthly Usage Rollup

- **Evidence:** Billing endpoint returns aggregated usage totals and cost.
- **Status:** Requires final verification against the assignment's monthly aggregation requirements.
- **Remaining verification:**
  - Confirm that usage is grouped by customer and the correct billing month.
  - Confirm that the totals include the supported usage categories.
  - Confirm that costs are calculated using the configured model rates and monetary precision rules.

## 9. Automated Test Results

- **Command:** `python -m pytest -q`
- **Previously reported result:** 19 passed, 1 warning.
- **Status:** Previously verified by the reported test run.
- **Final action:** Run the test suite again after any changes and record the latest result.

## 10. Swagger UI Evidence

Capture screenshots of successful requests and responses for:

- [ ] `GET /health`
- [ ] `POST /usage`
- [ ] `GET /billing/{customer_id}`
- [ ] Stripe test-mode Checkout and the resulting subscription status

**Status:** Screenshots still need to be captured and saved for submission.

## 11. Final Assignment Checklist

- [ ] Confirm pricing configuration against the assignment specification.
- [ ] Verify monthly usage aggregation and cost calculation.
- [ ] Verify webhook signature validation and duplicate-event handling.
- [ ] Verify subscription update and deletion event handling.
- [ ] Confirm the final automated test result.
- [ ] Capture the required Swagger UI and Stripe evidence.
- [ ] Complete every applicable item in the assignment PDF's Section 6 checklist.
- [ ] Confirm that `.env` and all real credentials are excluded from Git.
- [ ] Confirm that the required documentation and configuration files are present in the submission repository.

## Evidence Integrity Note

This document distinguishes previously reported test results from checks that still require final verification. Mark an item complete only after confirming it against the implementation, automated tests, database records, or captured API responses.
