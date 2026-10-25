# Capstone Project: The Unofficial Guide (Extended)

**Author:** Ryan Lawton  
**Corpus:** `advice_threads`  
**Base System:** AI201 Question-Answering RAG System (The Unofficial Guide)

---

## What This Extends

This capstone project extends **The Unofficial Guide**, a retrieval-augmented generation (RAG) system built during Week 1 and Week 2. The original system uses a local Chroma vector database with `all-MiniLM-L6-v2` dense embeddings, a 0.60 distance relevance gate (`gate.py`), and a grounded generation pipeline (`generate.py`) calling Gemini (`gemini-2.5-flash-lite` / `gemini-3.5-flash-lite`) to answer college campus advice questions with thread-level source citations.

---

## The Shape

As part of this comprehensive capstone audit, this project specifies and explores **all three shapes (A, B, and C)**:

### Shape A: Deploy and Instrument
For Shape A, I am taking the command-line RAG system that previously ran only as an offline terminal script (`app.py`) and operationalizing `serve.py` into an observable, production-ready HTTP microservice. The extension is the operational and observability infrastructure: wrapping the `/ask` and `/health` endpoints with comprehensive structured JSON logging emitted to both a dedicated log stream and stdout. Every record captures a unique request UUID, ISO timestamp, input question length, retrieval duration, generation duration, total end-to-end latency, gate distance, token counts (prompt, candidate, total), and HTTP status codes. Additionally, the service provides an instrumented runtime health/readiness check verifying index integrity, paired with a clean, reproducible run path documented in `RUNNING.md`.

*Out of Scope for Shape A:*
- Deploying to a multi-node Kubernetes cluster or distributed serverless infrastructure (restricted to single-host/containerized local run).
- Integrating cloud-managed telemetry collectors (e.g., Datadog, OpenTelemetry collector daemon, AWS CloudWatch).
- Building an interactive browser frontend or chat UI.

### Shape B: Harden Against Failure
For Shape B, I am adding a single cohesive hardening layer: an **HTTP Error Handling & Graceful Degradation Middleware** for `serve.py`. Currently, any runtime anomaly—such as an upstream API timeout, missing vector collection, or malformed payload—triggers an unhandled Python exception and returns a generic 500 internal server error. This hardening layer wraps the execution pipeline with structured bad-path interceptors: it sanitizes and bounds incoming client payloads (returning structured `400 Bad Request` envelopes for empty, malformed, or oversized queries), catches database unreadiness with actionable `503 Service Unavailable` envelopes, and implements graceful degradation for upstream LLM timeouts or quota exhaustion by returning the grounded retrieved excerpts accompanied by an explicit partial-response disclaimer rather than a service failure.

*Out of Scope for Shape B:*
- Implementing automatic multi-provider LLM failover (e.g., dynamic fallbacks from Gemini to Anthropic Claude or OpenAI).
- Implementing distributed token-bucket rate limiting via external state stores like Redis.
- Modifying client-side network retry mechanics or socket keep-alive protocols.

### Shape C: Extend One Capability
For Shape C, I am adding **Hybrid Retrieval (BM25 Lexical + Dense Vector Retrieval with Reciprocal Rank Fusion)**. As diagnosed in the Week 2 post-mortem, dense semantic vector search alone struggled with vocabulary mismatches, specific keyword queries (e.g., exact course codes, policy deadlines, fee structures), and allowed near-miss queries to slip past the distance gate. The extension adds an in-memory BM25 index across the `advice_threads` corpus and implements a fusion layer that blends lexical BM25 ranks with ChromaDB dense vector cosine distances using Reciprocal Rank Fusion (RRF). This capability ensures the generator receives excerpts that have strong semantic context while strictly preserving exact keyword fidelity.

*Out of Scope for Shape C:*
- Training or deploying a heavy neural cross-encoder reranking model (e.g., `bge-reranker-large`).
- Implementing LLM-based multi-query rewriting, sub-query decomposition, or HyDE (Hypothetical Document Embeddings).
- Multi-corpus routing or cross-corpus retrieval across other course datasets.

---

## Running It

This project follows **Path B (local with logs)**.

Detailed instructions on environment setup, required dependencies, vector index generation, and the exact command to run the service are documented in [`RUNNING.md`](file:///c:/Users/rlawt/Documents/Repos/codepath/tf-weekly-assignments/AI201/2026/fall/The%20Capstone/base_project_docs/RUNNING.md).

Quick start:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python serve.py
```

---

## Instrumentation

### Schema
Each structured log record is formatted as single-line JSON with the following fields:
- `timestamp`: ISO 8601 UTC timestamp
- `request_id`: Unique UUIDv4 string
- `client_ip`: Remote client IP address
- `endpoint`: HTTP path called (`/ask`, `/health`)
- `status_code`: HTTP status code returned
- `latency_ms`: Total request duration in milliseconds
- `retrieval_ms`: Time spent querying vector / BM25 index
- `generation_ms`: Time spent calling the LLM
- `question`: Normalized query text
- `refused`: Boolean indicating gate refusal
- `best_distance`: Top match distance / score
- `prompt_tokens`: Tokens sent in the prompt
- `output_tokens`: Tokens generated by the model
- `error`: Error classification or null

### Pasted Log Entries
*(At least 10 sample structured log entries from live runs will be pasted here upon running Milestone 3)*

```json
{"timestamp": "2026-10-24T22:30:00Z", "request_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d", "endpoint": "/ask", "status_code": 200, "latency_ms": 1120.4, "retrieval_ms": 42.1, "generation_ms": 1078.3, "question": "How much RAM do I need for CS courses?", "refused": false, "best_distance": 0.257, "prompt_tokens": 482, "output_tokens": 58, "error": null}
```

---

## What It Costs

*(To be measured across 10 non-cached evaluation queries in Milestone 3 & Milestone 7)*

- **Average Latency per Run:** TBD ms
- **Average Prompt Tokens:** TBD tokens
- **Average Output Tokens:** TBD tokens
- **Measured Cost per Run:** $TBD
- **100 Queries / Day Arithmetic:**
  - `100 queries * $cost_per_query = $total_per_day`

---

## Run Log and Verdicts

| # | Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|---|
| 1 | *(Criterion 1)* | | | | | |
| 2 | *(Criterion 2)* | | | | | |
| 3 | *(Criterion 3)* | | | | | |
| 4 | *(Criterion 4)* | | | | | |
| 5 | *(Criterion 5)* | | | | | |

### Diagnoses of Misses
*(Detailed stage and mechanism analysis for any unmet criteria)*

---

## The Improvement

- **What I Changed:** TBD
- **Why I Picked It:** TBD

### Run Log — After Improvement

| # | Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|---|
| 1 | *(Criterion 1)* | | | | | |
| 2 | *(Criterion 2)* | | | | | |
| 3 | *(Criterion 3)* | | | | | |
| 4 | *(Criterion 4)* | | | | | |
| 5 | *(Criterion 5)* | | | | | |

**Did it help?** TBD

---

## What's Still Broken

- **Remaining Misses:** TBD
- **Next Steps:** TBD

---

## How I Used AI

1. **Prompt & Context:** TBD
2. **Result & Modification:** TBD
