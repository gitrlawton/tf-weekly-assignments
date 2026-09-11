# Daily Workflow

This guide details the daily commands needed to start, stop, and maintain your local development environment.

## Startup Workflow
Whenever you want to start development:

1. **Start backing services** (PostgreSQL, Redis, ChromaDB):
   ```bash
   docker compose up -d
   ```
2. **Start the application servers** (starts the FastAPI backend on port `8000` and Vite React frontend on port `5173` concurrently):
   ```bash
   make run
   ```
3. **Open the dashboard** in your browser at http://localhost:5173.

---

## Shutdown Workflow
When you are done developing:

1. **Stop the development servers:** Press `Ctrl + C` in the Git Bash terminal where `make run` is running.
2. **Stop the background docker services** (frees up RAM and system resources):
   ```bash
   docker compose down
   ```

---

## Utility Commands

* **Format & Lint checks:** Run the linter, formatter, and typechecker before making commits:
  ```bash
  make check
  ```
* **Run unit tests:** Run backend unit tests:
  ```bash
  make test-unit
  ```
* **Reset Database:** Wipe the local database and re-seed it with test users (`user1@example.com`, etc.):
  ```bash
  make reset-db
  ```
