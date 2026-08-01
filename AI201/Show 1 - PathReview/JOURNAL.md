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

## Week 9 — Solution building & PR submission

**Branch:** docs/117-api-curl-examples

**What you built:**
I updated `docs/API.md` to include comprehensive, copy-pasteable `curl` examples, HTTP headers, request payloads, and response JSON formats. I also added documentation for previously undocumented endpoints such as `PUT /profiles/{profile_id}` and `GET /reviews/{review_id}/status`.

**Tests added or updated:**
No test files were touched or added as this is a documentation-only change.

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes

**Draft PR feedback received from:** "none"

## Week 10 — Iteration & reflection

### Reflection

**What was harder than you expected?**
Mapping out the exact request structures and formats for the endpoints was harder than expected because some active endpoints (like `PUT /profiles/{profile_id}` and `GET /reviews/{review_id}/status`) were completely missing from the existing documentation. I had to carefully inspect the FastAPI route decorators and Pydantic schemas in the backend codebase to construct accurate request bodies, query parameters, and path variables.

**What did you learn about working in a large codebase?**
I learned that even for a documentation-only task, reading and understanding the controller, schema, and routing code is vital to ensure you don't document outdated API behavior. It's not enough to trust existing docs. Cross-referencing implementation details (like headers, dependency injection, and parameter types) is key to making sure everything is correct.

**How did AI tools help — and where did they fall short?**
AI tools were excellent for fast file searches and translating Python Pydantic models into sample request/response JSON examples. However, they occasionally struggled with distinguishing between content types, such as standard JSON payloads versus FastAPI's Form parameters (used in `POST /auth/login` and `POST /profiles`). I had to manually review the source code to correct the arguments in the `curl` examples.

**What would you do differently if you started over?**
If I started over, I would launch the API locally and inspect the `/docs` (Swagger UI) first. Having that interactive UI or importing the raw OpenAPI JSON into a tool like Postman would have speeded up the discovery of missing endpoints and parameter types, rather than scanning the individual python files manually.

**What are you most proud of from this module?**
I am most proud of writing documentation that is complete and robust. Instead of just creating quick placeholder commands, I detailed the exact authentication setups, headers, content types, and sample JSON request/response bodies, including previously undocumented endpoints, making it extremely easy for future developers to verify their setup.