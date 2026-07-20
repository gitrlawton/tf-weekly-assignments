## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/117

**Issue title:** API docs don't include example curl commands #117

**Issue Description:**
docs/API.md describes each endpoint but has no example invocations. Developers setting up the project for the first time can't quickly verify the API is working.

Relevant files: docs/API.md

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The current `docs/API.md` file outlines the backend endpoints but lacks practical usage examples. This makes it difficult for new developers to quickly verify that their API is functioning correctly from the command line after initial setup. Providing sample `curl` requests (such as for health checking, registering, logging in, and creating reviews) will give developers a clear reference for interacting with the backend directly.

**Branch name:** docs/117-api-curl-examples

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** N/A (documentation issue, no reproduction steps needed)

**Reproduction summary:**
I inspected `docs/API.md` and verified that it lacks request payloads, header details, and executable `curl` command examples. Additionally, by cross-referencing with `api/routes/`, I observed that endpoints such as `PUT /profiles/{profile_id}` and `GET /reviews/{review_id}/status` are missing entirely from the documentation.

**PLAN.md link:** [link to PLAN.md](https://github.com/gitrlawton/tf-weekly-assignments/blob/main/AI201/Show%201%20-%20PathReview/PLAN.md)

**Blockers or open questions:**
None. I have mapped the API routes, parameter types (JSON for register/reviews, urlencoded form-data for login, multipart form-data for profile creation, and path variables), and authorization headers needed to construct comprehensive `curl` examples.