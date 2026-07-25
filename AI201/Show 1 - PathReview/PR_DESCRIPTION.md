## What changed

I updated `docs/API.md` to include comprehensive, copy-pasteable `curl` examples, HTTP headers, request payloads, and response JSON formats for all endpoints. I also documented previously undocumented active endpoints like profile updates (`PUT /profiles/{profile_id}`) and review status check (`GET /reviews/{review_id}/status`).

## Root cause

This is a documentation issue. The original `docs/API.md` only listed a subset of endpoints with brief descriptions, lacking concrete payloads, headers, or curl invocations. This made it difficult for developers to quickly query and verify endpoints after local setup.

## How to test

Reviewers can verify this by checking `docs/API.md` and comparing the documented endpoints, request parameters, and payloads against the FastAPI route implementations under the `api/routes/` directory. All curl commands are formatted to be copy-pasteable and executed directly.

## Files changed

| File | Change |
|------|--------|
| `docs/API.md` | Rewrote the reference guide to add setup instructions, curl examples, authentication details, request/response structures, and missing endpoints. |

## Tests

No test files were touched or added as this is a documentation-only change.

## Pre-existing issues (if any)

There are pre-existing ruff linting errors in the unit test files (e.g. `tests/unit/test_review_service.py`, `tests/unit/test_security.py`, etc.). Since this is a documentation-only change, my changes do not affect or introduce any linting issues.