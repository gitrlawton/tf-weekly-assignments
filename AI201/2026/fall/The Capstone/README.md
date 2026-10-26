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

Detailed instructions on environment setup, required dependencies, vector index generation, and the exact command to run the service are documented in [`RUNNING.md`](file:///c:/Users/rlawt/Documents/Repos/codepath/tf-weekly-assignments/AI201/2026/fall/The%20Capstone/RUNNING.md).

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
- `hybrid`: Boolean indicating whether hybrid retrieval was requested
- `rrf_score`: Reciprocal Rank Fusion top score (or null if dense-only)
- `prompt_tokens`: Tokens sent in the prompt
- `output_tokens`: Tokens generated by the model
- `error`: Error classification or null

### Pasted Log Entries
The following 12 structured JSON log records were generated during a live HTTP evaluation session across `/health`, `/ask` (in-scope and gate-refused queries), and `/stats`:

```json
{"request_id": "85924732-0864-4c91-bae7-cb9b931d80ab", "client_ip": "127.0.0.1", "endpoint": "/health", "method": "GET", "status_code": 200, "latency_ms": 1181.81, "retrieval_ms": 0.0, "gate_ms": 0.0, "generation_ms": 0.0, "question": null, "refused": false, "best_distance": null, "prompt_tokens": 0, "output_tokens": 0, "error": null, "timestamp": "2026-10-25T06:14:47.890984+00:00"}
{"request_id": "769f3968-f280-4288-b611-9bf80ce1c9aa", "client_ip": "127.0.0.1", "endpoint": "/ask", "method": "POST", "status_code": 200, "latency_ms": 325.0, "retrieval_ms": 317.62, "gate_ms": 0.01, "generation_ms": 0.29, "question": "How much RAM do I need for CS courses?", "refused": false, "best_distance": 0.257, "prompt_tokens": 0, "output_tokens": 0, "error": null, "timestamp": "2026-10-25T06:14:50.254928+00:00"}
{"request_id": "e67bae35-1622-456a-8413-d21ecde5282d", "client_ip": "127.0.0.1", "endpoint": "/ask", "method": "POST", "status_code": 200, "latency_ms": 3261.83, "retrieval_ms": 41.03, "gate_ms": 0.01, "generation_ms": 3220.54, "question": "When is the deadline to change your meal plan tier?", "refused": false, "best_distance": 0.3216, "prompt_tokens": 972, "output_tokens": 24, "error": null, "timestamp": "2026-10-25T06:14:55.542347+00:00"}
{"request_id": "a828a4ce-de39-4605-8fbd-e8dd594bb2ea", "client_ip": "127.0.0.1", "endpoint": "/ask", "method": "POST", "status_code": 200, "latency_ms": 872.77, "retrieval_ms": 40.58, "gate_ms": 0.01, "generation_ms": 831.92, "question": "Is a bike worth it for a 20 minute commute?", "refused": false, "best_distance": 0.3224, "prompt_tokens": 937, "output_tokens": 56, "error": null, "timestamp": "2026-10-25T06:14:58.922596+00:00"}
{"request_id": "09b06938-06ff-440b-aa15-98bb17d30d81", "client_ip": "127.0.0.1", "endpoint": "/ask", "method": "POST", "status_code": 200, "latency_ms": 695.85, "retrieval_ms": 40.02, "gate_ms": 0.01, "generation_ms": 655.61, "question": "What is the first step if you have a roommate conflict?", "refused": false, "best_distance": 0.3478, "prompt_tokens": 932, "output_tokens": 38, "error": null, "timestamp": "2026-10-25T06:15:02.068749+00:00"}
{"request_id": "e59e495c-4ebb-48e8-b933-0c5ae46d5a6e", "client_ip": "127.0.0.1", "endpoint": "/ask", "method": "POST", "status_code": 200, "latency_ms": 673.44, "retrieval_ms": 40.93, "gate_ms": 0.01, "generation_ms": 632.28, "question": "What happens if you turn in an assignment late?", "refused": false, "best_distance": 0.4128, "prompt_tokens": 1004, "output_tokens": 46, "error": null, "timestamp": "2026-10-25T06:15:05.238799+00:00"}
{"request_id": "6db24793-1b23-48a3-a25a-b7888defbff9", "client_ip": "127.0.0.1", "endpoint": "/ask", "method": "POST", "status_code": 200, "latency_ms": 40.86, "retrieval_ms": 40.66, "gate_ms": 0.01, "generation_ms": 0.0, "question": "What is the capital of Mongolia?", "refused": true, "best_distance": 0.9479, "prompt_tokens": 0, "output_tokens": 0, "error": null, "timestamp": "2026-10-25T06:15:07.764657+00:00"}
{"request_id": "3fbf1aeb-d179-40a5-9db6-eec174ac0ee6", "client_ip": "127.0.0.1", "endpoint": "/ask", "method": "POST", "status_code": 200, "latency_ms": 41.35, "retrieval_ms": 41.14, "gate_ms": 0.01, "generation_ms": 0.0, "question": "How do I change the oil in a diesel engine?", "refused": true, "best_distance": 0.9299, "prompt_tokens": 0, "output_tokens": 0, "error": null, "timestamp": "2026-10-25T06:15:10.286279+00:00"}
{"request_id": "a4a844af-d43f-4b70-bc5b-0a9033e09eae", "client_ip": "127.0.0.1", "endpoint": "/ask", "method": "POST", "status_code": 200, "latency_ms": 40.9, "retrieval_ms": 40.71, "gate_ms": 0.01, "generation_ms": 0.0, "question": "Who won the 1994 World Cup?", "refused": true, "best_distance": 0.9517, "prompt_tokens": 0, "output_tokens": 0, "error": null, "timestamp": "2026-10-25T06:15:12.701178+00:00"}
{"request_id": "fe8f1507-108c-4f35-ae0b-65530c618a7f", "client_ip": "127.0.0.1", "endpoint": "/ask", "method": "POST", "status_code": 200, "latency_ms": 41.93, "retrieval_ms": 41.7, "gate_ms": 0.01, "generation_ms": 0.0, "question": "What is the recommended dosage of ibuprofen for a headache?", "refused": true, "best_distance": 0.828, "prompt_tokens": 0, "output_tokens": 0, "error": null, "timestamp": "2026-10-25T06:15:15.251737+00:00"}
{"request_id": "b5c75057-b55f-461b-8422-261335fa9a5d", "client_ip": "127.0.0.1", "endpoint": "/ask", "method": "POST", "status_code": 200, "latency_ms": 40.43, "retrieval_ms": 40.23, "gate_ms": 0.01, "generation_ms": 0.0, "question": "How do I write a for loop in Rust?", "refused": true, "best_distance": 0.8712, "prompt_tokens": 0, "output_tokens": 0, "error": null, "timestamp": "2026-10-25T06:15:17.327755+00:00"}
{"request_id": "f7bb6791-3c39-45c4-a486-71b3369eab6c", "client_ip": "127.0.0.1", "endpoint": "/stats", "method": "GET", "status_code": 200, "latency_ms": 6.84, "retrieval_ms": 0.0, "gate_ms": 0.0, "generation_ms": 0.0, "question": null, "refused": false, "best_distance": null, "prompt_tokens": 0, "output_tokens": 0, "error": null, "timestamp": "2026-10-25T06:15:19.359837+00:00"}
```

---

## What It Costs

Cost was measured empirically across **10 non-cached queries** covering 10 distinct topics from the `advice_threads` corpus using `tools/measure_cost.py`. Prompts and responses were evaluated with caching disabled (`cache=False`), capturing actual token counts returned by Google Gemini API metadata and timing local stage execution (retrieval vs. generation).

### Measurement Summary (10 Non-Cached Runs)

- **Average Latency per Run:** 1,407.33 ms (Retrieval: 140.54 ms, Generation: 1,027.56 ms)
- **Average Prompt Tokens:** 937.3 tokens
- **Average Output Tokens:** 40.7 tokens
- **Average Total Tokens:** 978.0 tokens
- **Pricing Basis:** Google Gemini Developer API ($0.075 / 1M prompt tokens, $0.30 / 1M output tokens)
- **Measured Cost per Run:** **$0.000083 USD** (~$0.083 per 1,000 queries)

### 100 Queries / Day Arithmetic
- **Daily Token Volume:** `100 queries * 978.0 tokens = 97,800 tokens/day`
- **Daily API Spend:** `100 queries * $0.0000825 = $0.0083 USD/day` (under 1 cent per day)
- **30-Day Monthly Projection:** `$0.00825 * 30 days = $0.2475 USD/month` (~25 cents per month)

### Granular 10-Run Breakdown

| Run | Question | Total Latency | Stage Latency (Ret / Gen) | Tokens (In / Out) | Cost (USD) |
|---|---|---|---|---|---|
| 1 | How much RAM do I need for CS courses? | 6,509.4 ms | 1,032.2 ms / 5,477.2 ms | 869 / 20 (889 tot) | $0.000071 |
| 2 | When is the deadline to change your meal plan tier? | 663.2 ms | 41.2 ms / 621.9 ms | 972 / 24 (996 tot) | $0.000080 |
| 3 | Is a bike worth it for a 20 minute commute? | 981.4 ms | 41.5 ms / 939.8 ms | 937 / 84 (1,021 tot) | $0.000095 |
| 4 | What is the first step if you have a roommate conflict? | 639.0 ms | 40.7 ms / 598.2 ms | 932 / 43 (975 tot) | $0.000083 |
| 5 | What happens if you turn in an assignment late? | 629.9 ms | 41.1 ms / 588.7 ms | 1,004 / 63 (1,067 tot) | $0.000094 |
| 6 | Is the campus printing quota enough for the semester? | 936.4 ms | 41.9 ms / 894.4 ms | 914 / 53 (967 tot) | $0.000084 |
| 7 | Can freshmen bring a car and park on campus? | 852.3 ms | 42.1 ms / 810.1 ms | 955 / 31 (986 tot) | $0.000081 |
| 8 | What is the best time to do laundry in dorms? | 1,615.2 ms | 42.5 ms / 1,572.6 ms | 907 / 34 (941 tot) | $0.000078 |
| 9 | Where are the quietest study spots during finals week? | 647.2 ms | 41.8 ms / 605.3 ms | 896 / 24 (920 tot) | $0.000074 |
| 10 | When should you use the pass/fail grading option? | 599.3 ms | 42.4 ms / 556.8 ms | 987 / 31 (1,018 tot) | $0.000083 |
| **Avg** | **10 Distinct In-Scope Queries** | **1,407.3 ms** | **140.5 ms / 1,027.6 ms** | **937.3 / 40.7 (978.0 tot)** | **$0.000083** |

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
