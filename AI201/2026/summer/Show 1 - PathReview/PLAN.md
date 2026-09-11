## Solution plan

**Issue:** [API docs don't include example curl commands #117](https://github.com/jamjamgobambam/pathreview/issues/117)

### Understand
What is the root cause of this issue? What behavior is expected vs. actual?
- **Root Cause**: `docs/API.md` provides high-level descriptions of backend endpoints but lacks executable `curl` command examples, expected headers (e.g., JWT `Authorization: Bearer <token>`), and explicit payload format specifications (JSON vs. form-data vs. multipart file upload). Furthermore, some endpoints implemented in code (`PUT /profiles/{profile_id}` and `GET /reviews/{review_id}/status`) are completely missing from the documentation.
- **Actual Behavior**: Developers cannot quickly test or verify endpoints from the command line after setting up the project without referring to the source code or FastAPI interactive docs.
- **Expected Behavior**: `docs/API.md` contains practical, copy-pasteable `curl` examples for every endpoint, clear instructions on passing authentication tokens, sample request payloads/parameters, and documented routes for all active endpoints.

### Map
Which files, functions, or modules are involved? List the specific files you expect to touch.
- **Files to modify**:
  - API.md: `docs/API.md` (Update documentation with detailed endpoint specifications and `curl` examples)
  - PLAN.md: `PLAN.md` (Document the solution approach and plan)
- **Reference files used to verify API contracts**:
  - auth.py: `api/routes/auth.py` (`POST /auth/register`, `POST /auth/login`)
  - profiles.py: `api/routes/profiles.py` (`POST /profiles`, `GET /profiles/{id}`, `PUT /profiles/{id}`, `DELETE /profiles/{id}`)
  - reviews.py: `api/routes/reviews.py` (`POST /reviews`, `GET /reviews/{id}`, `GET /reviews`, `GET /reviews/{id}/status`)
  - health.py: `api/routes/health.py` (`GET /health`)
  - user.py: `api/schemas/user.py`
  - profile.py: `api/schemas/profile.py`
  - review.py: `api/schemas/review.py`

### Plan
What are the steps to fix this issue? Break it into 3–5 concrete sub-tasks.
1. **Audit & Re-structure Endpoint Documentation**: Update `docs/API.md` to organize endpoints cleanly under Health, Authentication, Profiles, and Reviews, ensuring all active endpoints (including missing ones like `PUT /profiles/{profile_id}` and `GET /reviews/{review_id}/status`) are listed.
2. **Add Authentication & Setup Instructions**: Document how developers can obtain a JWT access token via registration/login and export it as an environment variable (`export TOKEN="your_jwt_token"`) for use in subsequent authenticated `curl` requests.
3. **Draft `curl` Examples for Auth & Health Endpoints**: Provide copy-pasteable `curl` invocations for `GET /health`, `POST /auth/register` (using JSON `-d`), and `POST /auth/login` (using `application/x-www-form-urlencoded` `-d "username=...&password=..."`).
4. **Draft `curl` Examples for Profile & Review Endpoints**: Provide copy-pasteable `curl` commands for all profile endpoints (demonstrating multipart form upload `-F` for `POST /profiles` with resume PDF/MD attachment) and review endpoints (including review creation, status check, detail retrieval, and paginated listing).
5. **Review & Format Verification**: Ensure markdown syntax highlighting (`bash` or `curl`), clean line breaks, readable formatting, and accurate placeholder variables (e.g., `$TOKEN`, `{profile_id}`, `{review_id}`).

### Inputs & outputs
What does your fix take as input? What should it produce or change?
- **Inputs**: Verified API route definitions and Pydantic schemas from the `api/` module.
- **Outputs**: An updated, developer-friendly `docs/API.md` with complete endpoint listings, expected payload formats, required headers, and executable `curl` commands.

### Risks & unknowns
What could go wrong? What are you still unsure about?
- **Shell / OS syntax variations**: `curl` commands formatted with POSIX shell line continuations (`\`) can sometimes require slight adjustments on Windows Command Prompt. Using clear multi-line bash examples or concise standard `curl` syntax will keep them cross-platform friendly while documenting standard Unix dev conventions.
- **Placeholder values**: Developers might execute commands without replacing dummy IDs or file paths. Using clear placeholders like `<YOUR_ACCESS_TOKEN>`, `<PROFILE_ID>`, and `@resume.pdf` with explicit notes will prevent confusion.

### Edge cases
What inputs or states should your fix handle gracefully?
- **Authentication Headers**: Protected endpoints require `-H "Authorization: Bearer $TOKEN"`. The docs must highlight when an endpoint requires authentication vs. when it is public (like `/health`, `/auth/register`, `/auth/login`).
- **Different Content Types**:
  - `POST /auth/register` takes `-H "Content-Type: application/json"`.
  - `POST /auth/login` takes standard form fields (`OAuth2PasswordRequestForm`).
  - `POST /profiles` takes `multipart/form-data` via `-F` to support file upload (`resume_file=@/path/to/file.pdf`).
  - `POST /reviews` takes JSON payload with `profile_id`.