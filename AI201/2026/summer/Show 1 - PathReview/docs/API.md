# PathReview API Reference

This document provides a detailed reference for all PathReview backend API endpoints.

**Base URL:** `http://localhost:8000`

---

## Authentication Flow

Protected endpoints require a JSON Web Token (JWT) passed in the `Authorization` header:

```bash
Authorization: Bearer <your_access_token>
```

To make testing easier with `curl`, you can register or login, copy the returned `access_token`, and export it as an environment variable in your terminal:

```bash
export TOKEN="your_jwt_access_token_here"
```

You can then use `$TOKEN` in subsequent requests: `-H "Authorization: Bearer $TOKEN"`.

---

## Endpoints

### Health

#### `GET /` — Root Status

Returns a basic greeting showing that the API service is running.

- **Authentication:** None
- **cURL Example:**
  ```bash
  curl -X GET http://localhost:8000/
  ```
- **Response Example (`200 OK`):**
  ```json
  {
    "message": "PathReview API is running",
    "version": "1.0.0"
  }
  ```

#### `GET /health` — Dependency Health Status

Checks the status of the PostgreSQL database, Redis, and the Vector Database.

- **Authentication:** None
- **cURL Example:**
  ```bash
  curl -X GET http://localhost:8000/health
  ```
- **Response Example (`200 OK`):**
  ```json
  {
    "status": "healthy",
    "dependencies": {
      "postgres": "healthy",
      "redis": "healthy",
      "vector_db": "healthy"
    },
    "safety_events_last_hour": 0,
    "timestamp": "2026-07-25T23:30:46.123456"
  }
  ```
- **Response Example (`503 Service Unavailable`):**
  Returned if any critical dependency is down.
  ```json
  {
    "detail": {
      "status": "unhealthy",
      "dependencies": {
        "postgres": "unhealthy",
        "redis": "healthy",
        "vector_db": "healthy"
      },
      "safety_events_last_hour": 0,
      "timestamp": "2026-07-25T23:30:46.123456"
    }
  }
  ```

---

### Authentication

#### `POST /auth/register` — Create a New Account

Creates a new user account and returns a JWT access token.

- **Authentication:** None
- **Request Body:** JSON
  - `email` (string, required): A valid email address.
  - `password` (string, required): Password between 8 and 128 characters.
- **cURL Example:**
  ```bash
  curl -X POST http://localhost:8000/auth/register \
    -H "Content-Type: application/json" \
    -d '{
      "email": "user@example.com",
      "password": "securepassword123"
    }'
  ```
- **Response Example (`200 OK`):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer"
  }
  ```
- **Response Example (`400 Bad Request`):**
  Returned if the email is already registered.
  ```json
  {
    "detail": "Email already registered"
  }
  ```

#### `POST /auth/login` — Obtain Access Token

Authenticates a user and returns a JWT access token.

- **Authentication:** None
- **Request Body:** `application/x-www-form-urlencoded`
  - `username` (string, required): The registered email address.
  - `password` (string, required): The password.
- **cURL Example:**
  ```bash
  curl -X POST http://localhost:8000/auth/login \
    -d "username=user@example.com&password=securepassword123"
  ```
- **Response Example (`200 OK`):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer"
  }
  ```
- **Response Example (`401 Unauthorized`):**
  Returned if login fails.
  ```json
  {
    "detail": "Invalid email or password"
  }
  ```

---

### Profiles

#### `POST /profiles` — Create Profile

Creates a profile with an optional resume file and GitHub integration.

- **Authentication:** Required (Bearer Token)
- **Request Body:** `multipart/form-data`
  - `github_username` (string, optional): GitHub username.
  - `portfolio_url` (string, optional): Personal website or portfolio URL.
  - `resume_file` (file, optional): PDF, Markdown, or text file.
- **cURL Example:**
  ```bash
  curl -X POST http://localhost:8000/profiles \
    -H "Authorization: Bearer $TOKEN" \
    -F "github_username=octocat" \
    -F "portfolio_url=https://github.com/octocat" \
    -F "resume_file=@/path/to/resume.pdf"
  ```
- **Response Example (`200 OK`):**
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "user_id": "987f6543-e21b-32d1-b654-219914173999",
    "github_username": "octocat",
    "portfolio_url": "https://github.com/octocat",
    "created_at": "2026-07-25T23:30:46.123456",
    "resume_filename": "resume.pdf"
  }
  ```

#### `GET /profiles/{profile_id}` — Retrieve Profile

Retrieves the profile information by its UUID.

- **Authentication:** Required (Bearer Token)
- **Path Parameters:**
  - `profile_id` (UUID, required): The UUID of the profile.
- **cURL Example:**
  ```bash
  curl -X GET http://localhost:8000/profiles/123e4567-e89b-12d3-a456-426614174000 \
    -H "Authorization: Bearer $TOKEN"
  ```
- **Response Example (`200 OK`):**
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "user_id": "987f6543-e21b-32d1-b654-219914173999",
    "github_username": "octocat",
    "portfolio_url": "https://github.com/octocat",
    "created_at": "2026-07-25T23:30:46.123456",
    "resume_filename": "resume.pdf"
  }
  ```

#### `PUT /profiles/{profile_id}` — Update Profile

Updates profile settings (GitHub username or portfolio URL).

- **Authentication:** Required (Bearer Token)
- **Path Parameters:**
  - `profile_id` (UUID, required): The UUID of the profile.
- **Request Body:** JSON
  - `github_username` (string, optional): Updated GitHub username.
  - `portfolio_url` (string, optional): Updated portfolio URL.
- **cURL Example:**
  ```bash
  curl -X PUT http://localhost:8000/profiles/123e4567-e89b-12d3-a456-426614174000 \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "github_username": "octocat-updated",
      "portfolio_url": "https://github.com/octocat-updated"
    }'
  ```
- **Response Example (`200 OK`):**
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "user_id": "987f6543-e21b-32d1-b654-219914173999",
    "github_username": "octocat-updated",
    "portfolio_url": "https://github.com/octocat-updated",
    "created_at": "2026-07-25T23:30:46.123456",
    "resume_filename": "resume.pdf"
  }
  ```

#### `DELETE /profiles/{profile_id}` — Delete Profile

Deletes a profile along with all associated reviews and ingested data.

- **Authentication:** Required (Bearer Token)
- **Path Parameters:**
  - `profile_id` (UUID, required): The UUID of the profile to delete.
- **cURL Example:**
  ```bash
  curl -X DELETE http://localhost:8000/profiles/123e4567-e89b-12d3-a456-426614174000 \
    -H "Authorization: Bearer $TOKEN"
  ```
- **Response Example (`204 No Content`):**
  *Empty response body.*

---

### Reviews

#### `POST /reviews` — Request Portfolio Review

Triggers the ingestion pipeline and AI orchestrator asynchronously to review a profile.

- **Authentication:** Required (Bearer Token)
- **Request Body:** JSON
  - `profile_id` (UUID, required): The profile UUID to review.
- **cURL Example:**
  ```bash
  curl -X POST http://localhost:8000/reviews \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "profile_id": "123e4567-e89b-12d3-a456-426614174000"
    }'
  ```
- **Response Example (`200 OK`):**
  Returns immediately with `pending` status while processing runs in the background.
  ```json
  {
    "id": "888e4567-e89b-12d3-a456-426614174888",
    "profile_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "pending",
    "sections": null,
    "overall_score": null,
    "error_message": null,
    "created_at": "2026-07-25T23:30:46.123456",
    "updated_at": "2026-07-25T23:30:46.123456"
  }
  ```

#### `GET /reviews/{review_id}/status` — Check Review Status

Gets current status and completion progress percentage of the background review task.

- **Authentication:** Required (Bearer Token)
- **Path Parameters:**
  - `review_id` (UUID, required): The UUID of the review.
- **cURL Example:**
  ```bash
  curl -X GET http://localhost:8000/reviews/888e4567-e89b-12d3-a456-426614174888/status \
    -H "Authorization: Bearer $TOKEN"
  ```
- **Response Example (`200 OK`):**
  ```json
  {
    "review_id": "888e4567-e89b-12d3-a456-426614174888",
    "status": "processing",
    "progress_pct": 50
  }
  ```

#### `GET /reviews/{review_id}` — Retrieve Completed Review

Retrieves a detailed, completed portfolio review containing section scores and suggestion details.

- **Authentication:** Required (Bearer Token)
- **Path Parameters:**
  - `review_id` (UUID, required): The UUID of the review.
- **cURL Example:**
  ```bash
  curl -X GET http://localhost:8000/reviews/888e4567-e89b-12d3-a456-426614174888 \
    -H "Authorization: Bearer $TOKEN"
  ```
- **Response Example (`200 OK`):**
  ```json
  {
    "id": "888e4567-e89b-12d3-a456-426614174888",
    "profile_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "completed",
    "sections": [
      {
        "section_name": "GitHub Activity",
        "content": "Strong recent commits in Python and TypeScript.",
        "confidence": 0.95,
        "suggestions": [
          "Add more documentation to your repositories."
        ]
      }
    ],
    "overall_score": 8.5,
    "error_message": null,
    "created_at": "2026-07-25T23:30:46.123456",
    "updated_at": "2026-07-25T23:30:50.654321"
  }
  ```

#### `GET /reviews` — List Reviews

Lists portfolio reviews created by the authenticated user with pagination.

- **Authentication:** Required (Bearer Token)
- **Query Parameters:**
  - `page` (integer, optional, default: 1): Page number.
  - `page_size` (integer, optional, default: 20, max: 100): Reviews per page.
- **cURL Example:**
  ```bash
  curl -X GET "http://localhost:8000/reviews?page=1&page_size=5" \
    -H "Authorization: Bearer $TOKEN"
  ```
- **Response Example (`200 OK`):**
  ```json
  {
    "items": [
      {
        "id": "888e4567-e89b-12d3-a456-426614174888",
        "profile_id": "123e4567-e89b-12d3-a456-426614174000",
        "status": "completed",
        "sections": [
          {
            "section_name": "GitHub Activity",
            "content": "Strong recent commits in Python and TypeScript.",
            "confidence": 0.95,
            "suggestions": [
              "Add more documentation to your repositories."
            ]
          }
        ],
        "overall_score": 8.5,
        "error_message": null,
        "created_at": "2026-07-25T23:30:46.123456",
        "updated_at": "2026-07-25T23:30:50.654321"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 5
  }
  ```

---

## Interactive Docs

When the API is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
