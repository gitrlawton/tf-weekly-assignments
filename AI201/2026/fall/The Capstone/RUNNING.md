# Running The Unofficial Guide (Capstone HTTP Service)

This document describes how to set up, initialize, and run the Capstone HTTP service (**Path B: Local with Logs**).

---

## 1. Environment Requirements

- **Python Version:** Python 3.10 to 3.12 (Tested on Python 3.11/3.12 Windows & Linux)
- **Dependencies:** Listed in [`requirements.txt`](file:///c:/Users/rlawt/Documents/Repos/codepath/tf-weekly-assignments/AI201/2026/fall/The%20Capstone/requirements.txt)
- **Local Embedding Model:** `all-MiniLM-L6-v2` (ONNX format, ~80 MB downloaded automatically by Chroma on first run from AWS CDN to local cache)
- **LLM API Provider:** Google Gemini API (`GEMINI_API_KEY` required in `.env`)

---

## 2. Setup Instructions (Clean Checkout)

### Step 1: Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env` and paste your Gemini API key:
```bash
# Windows PowerShell:
Copy-Item .env.example .env

# macOS / Linux:
cp .env.example .env
```
Ensure `.env` contains:
```ini
GEMINI_API_KEY=your_gemini_api_key_here
AI201_CORPUS=advice_threads
```

### Step 4: Build the Search Index (One-Time Setup)
Before starting the HTTP service, build the Chroma vector index from the corpus:
```bash
python app.py index
```

---

## 3. The Run Command (Single Documented Start Command)

To run the deployed service locally:

### Windows:
```powershell
python serve.py
```

### macOS / Linux (Production WSGI):
```bash
gunicorn serve:app --bind 0.0.0.0:5000
```

The service will start listening on `http://0.0.0.0:5000`.

---

## 4. Querying the Endpoints

### Health and Readiness Check
Verify index integrity and API configuration:
```bash
curl http://localhost:5000/health
```
Expected response:
```json
{
  "status": "ready",
  "corpus": "advice_threads",
  "index_ready": true,
  "chunk_count": 25,
  "api_key_configured": true,
  "detail": "System healthy and ready to answer queries"
}
```

### Ask a Question
Submit a query payload to `/ask`:
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How much RAM do I need for CS courses?"}'
```

### Operational Metrics & Stats
View live aggregated latency, token usage, and request counters:
```bash
curl http://localhost:5000/stats
```

---

## 5. Automated Evaluation & Live Logging Test

To run the benchmark test suite across all questions and trials over HTTP:
```bash
python tools/eval_http.py --url http://localhost:5000 --runs 3
```

All requests automatically stream to console stdout and append machine-readable JSON records to `logs/requests.jsonl`.

---

## 6. Testing Failure Scenarios & Bad Paths (Shape B)

The service includes an automated multi-trial fault-testing suite to verify bad-path resilience without altering code between runs:

```bash
python tools/eval_faults.py --url http://localhost:5000 --trials 3
```

### Tested Failure Surfaces:
| Scenario | Trigger / Payload | Expected Status | Error / Behavior Code |
|---|---|---|---|
| **Oversized Query** | Query text > 1,000 characters | `400 Bad Request` | `PAYLOAD_TOO_LARGE` |
| **Empty Query** | Missing question or whitespace only | `400 Bad Request` | `EMPTY_QUESTION` |
| **Non-JSON Payload** | Bad `Content-Type` / unparseable body | `400 Bad Request` | `INVALID_CONTENT_TYPE` |
| **Missing Index** | Header `X-Simulate-Fault: index_error` | `503 Service Unavailable` | `INDEX_UNAVAILABLE` |
| **Upstream Timeout (Graceful)** | Header `X-Simulate-Fault: timeout` | `200 OK (Degraded)` | Returns raw excerpts + notice |
| **Upstream Timeout (Strict)** | Headers `X-Simulate-Fault: timeout` & `X-Fail-Strict: true` | `504 Gateway Timeout` | `UPSTREAM_TIMEOUT` |

