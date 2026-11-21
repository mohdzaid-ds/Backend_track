# Build Log — Usage Metering & Billing Engine

## 1. Project Development

Built a FastAPI service for tracking simulated LLM usage, calculating costs, enforcing customer plan quotas, and integrating Stripe test-mode subscriptions.

## 2. Where AI Helped

- Explained the assignment requirements and broke the work into smaller steps.
- Assisted with FastAPI implementation and debugging.
- Helped develop and run automated tests for usage metering, pricing, idempotency, and quota enforcement.
- Guided the Stripe test-mode and webhook setup.
- Assisted with project documentation and submission files.

## 3. Issues and Corrections

- Resolved test and development issues through iterative debugging.
- Investigated Stripe CLI setup and webhook forwarding.
- Checked subscription records in SQLite to verify the Pro plan and active subscription.
- Identified documentation and submission requirements that still needed verification.

## 4. Developer Verification

- Ran the automated test suite; all 12 reported tests passed.
- Tested usage recording and billing aggregation through the API.
- Verified a Pro-plan subscription record in the database.
- Used Stripe test mode rather than a live payment.

## 5. Remaining Work

- Verify all requirements against the assignment PDF.
- Confirm the `capstone.yaml` run, seed, test, base URL, and endpoint configuration.
- Review token pricing, monthly usage rollups, webhook handling, and tenant isolation.
- Complete the remaining evidence checklist and validate the GitHub submission.

## 6. Developer Reflection

AI assistance was used for explanations, implementation guidance, debugging, and documentation. The developer must review the final code, understand the implementation, and verify all assignment requirements before submission.