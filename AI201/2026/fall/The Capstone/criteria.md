# Acceptance Criteria — The Unofficial Guide (Capstone Extended)

This document establishes the formal acceptance criteria for **The Unofficial Guide** capstone project across all three implemented shapes:
- **Shape A:** Deploy and Instrument (Operational HTTP Service & Observability)
- **Shape B:** Harden Against Failure (Edge-Case Defense & Graceful Degradation)
- **Shape C:** Extend One Capability (Hybrid BM25 + Dense RRF Retrieval)

Every criterion below defines an unambiguous, empirically measurable target written before evaluation results were finalized. No criterion turns on subjective words like *"works"*, *"reliable"*, *"good"*, or *"fast"*.

---

# Shape A: Deploy and Instrument

## 1. End-to-End HTTP Service Response Latency
For at least **4 of the 5** benchmark in-scope test questions, the deployed `/ask` endpoint returns a complete, grounded answer with HTTP status `200 OK` in under **3.5 seconds** total end-to-end latency.

**Why this target:**
- **System reference:** Under local execution (Path B), local Chroma vector retrieval requires 35ms to 120ms, while Google Gemini Flash generation requires 600ms to 2,500ms depending on generation length and API pacing.
- **Why not stricter:** A stricter threshold (e.g., 1.5 seconds) would artificially fail on thorough, multi-sentence answers or minor network jitter, even when retrieval and generation are working correctly.
- **Why not looser:** A looser threshold (e.g., 8.0 or 10.0 seconds) would mask serious pipeline regressions such as connection pooling hangs, retry thrashing, or inefficient token generation.
- **Cost of being wrong:** If latency exceeds 3.5s, the system feels sluggish for interactive use and wastes server worker concurrency.

---

## 2. 100% Request Traceability via Structured JSON Logging
**10 of 10** consecutive HTTP requests to `/health`, `/stats`, or `/ask` produce a valid single-line JSON log record in `logs/requests.jsonl` containing all required schema fields: `timestamp`, `request_id`, `endpoint`, `status_code`, `latency_ms`, and `retrieval_ms`.

**Why this target:**
- **System reference:** Shape A establishes operational observability. Log capture is handled by an unconditional `@app.after_request` hook in `serve.py` writing to `logs/requests.jsonl`.
- **Why not stricter:** 10 of 10 (100%) is already the strictest standard.
- **Why not looser:** A looser standard (e.g., 8 of 10) is unacceptable for production audit logs. Missing logs mean "blind spots" where silent failures cannot be debugged post-hoc.
- **Cost of being wrong:** If requests fail to generate log entries, operators cannot verify system health, diagnose customer complaints, or detect unauthorized traffic.

---

## 3. Operational Health and Readiness Probe Accuracy
A `GET /health` request returns HTTP `200 OK` with `"status": "ready"` and `"index_ready": true` when the vector database is initialized and `GEMINI_API_KEY` is present, and returns HTTP `503 Service Unavailable` with `"status": "not_ready"` and actionable remediation guidance if the collection is missing or the API key is unset.

**Why this target:**
- **System reference:** Container orchestrators and load balancers rely on `/health` probes to decide whether to direct user traffic to an instance.
- **Why not stricter:** Binary readiness (200 when ready, 503 when unready) is the exact industry standard for Kubernetes readiness probes.
- **Why not looser:** A loose probe that returns `200 OK` whenever the Flask web server is listening (regardless of database index state) would cause 100% of user queries to fail with unhandled 500 errors after deployment.
- **Cost of being wrong:** Traffic would be routed to unready containers, causing immediate service degradation.

---

# Shape B: Harden Against Failure

## 4. Inbound Payload Boundary Defense and Validation
In **3 of 3** independent trials, submitting an empty query (`{"question": ""}`), a non-JSON body, or an oversized payload (>1,000 characters) to `POST /ask` returns `HTTP 400 Bad Request` with a standardized JSON error envelope (`error`, `message`, `code`, `request_id`) and consumes exactly **0 LLM tokens**.

**Why this target:**
- **System reference:** Boundary defense is implemented in `serve.py` prior to invoking Chroma retrieval or Gemini generation.
- **Why not stricter:** 3 of 3 is already a deterministic 100% pass requirement.
- **Why not looser:** Allowing even 1 of 3 malformed requests to reach the LLM pipeline wastes costly API tokens and risks crashing the downstream chunk assembly logic.
- **Cost of being wrong:** Vulnerability to denial-of-service, runaway API billing from massive prompt injection attempts, and noisy 500 internal server crash logs.

---

## 5. Graceful Degradation on Upstream Model Timeout
When an upstream Gemini API call times out or encounters network unreachability (simulated via header `X-Simulate-Fault: timeout`), the service returns `HTTP 200 OK` with `"degraded": true`, an informative `error_detail` string, and an answer containing the top 3 raw retrieved excerpts from the corpus in **3 of 3** trials.

**Why this target:**
- **System reference:** Upstream provider outages and rate limits occur in real-world environments. The pipeline wraps model generation in a `ThreadPoolExecutor` timeout handler with fallback to `format_degraded_fallback(results)`.
- **Why not stricter:** 3 of 3 deterministic recovery is the highest standard.
- **Why not looser:** A looser target that permits unhandled exceptions or returns an empty 500 error leaves campus students with zero guidance during an API outage.
- **Cost of being wrong:** Complete outage for users despite relevant student advice threads already being successfully retrieved and available in memory.

---

## 6. Vector Store Unreachability Protection
In **3 of 3** independent trials where vector store unreachability is intercepted (or simulated via header `X-Simulate-Fault: index_error`), the endpoint returns `HTTP 503 Service Unavailable` with machine-readable error code `INDEX_UNAVAILABLE` and actionable recovery guidance (`"Run python app.py index"`), without emitting an unhandled server stack trace.

**Why this target:**
- **System reference:** Chroma index unreachability occurs when vector collections are unindexed, locked, or corrupted. Intercepted by `VectorStoreUnavailableError`.
- **Why not stricter:** 3 of 3 deterministic trials.
- **Why not looser:** Allowing unhandled Chroma database exceptions to bubble up as generic `500 Internal Server Error` prevents client automated retries and hides the root cause from system administrators.
- **Cost of being wrong:** Operators have to comb through raw Python tracebacks rather than receiving an actionable instruction to re-index the corpus.

---

# Shape C: Extend One Capability

## 7. Lexical BM25 Ranking Integration via Reciprocal Rank Fusion
For term-specific keyword queries (e.g., queries specifying exact hardware specs, policy deadlines, or acronyms like "RAM", "RA", or "pass/fail"), running with `--hybrid` produces an RRF fusion score for every candidate chunk, and places a chunk containing the exact keyword at rank 1 or 2 in at least **4 of 5** test queries.

**Why this target:**
- **System reference:** Dense semantic vector embeddings prioritize abstract topic similarity and frequently struggle with exact token matches or rare acronyms. In-memory `BM25Okapi` indexing scores exact term frequency and blends ranks using Reciprocal Rank Fusion ($k_{\text{rrf}} = 60$).
- **Why not stricter:** Requiring rank 1 in 5 of 5 queries is overly rigid because multiple relevant chunks in the thread often contain the keyword, making rank 2 equally valid.
- **Why not looser:** Allowing rank 3 or lower (e.g., 2 of 5) would mean BM25 lexical boosting is too weak to influence the LLM context window.
- **Cost of being wrong:** Users querying for specific technical terms receive generalized advice rather than the specific reply containing the exact policy or spec.

---

## 8. Relevance Gate Preservation Under Hybrid Retrieval
When hybrid retrieval is enabled (`--hybrid` or `"hybrid": true`), the system maintains **100% refusal fidelity** on out-of-scope questions, successfully refusing at least **4 of the 5** standard benchmark out-of-scope questions in `OUT_OF_SCOPE` by preserving underlying cosine distance checks alongside RRF fusion scores.

**Why this target:**
- **System reference:** A primary risk of lexical BM25 retrieval is that incidental stop-word overlaps or accidental token matches can falsely inflate the score of irrelevant documents.
- **Why not stricter:** 4 of 5 matches the foundational Week 1 relevance gate rubric.
- **Why not looser:** Refusing 3 or fewer out-of-scope questions would represent a severe safety regression, allowing off-topic queries into the generator.
- **Cost of being wrong:** The system hallucinates authoritative-sounding campus answers to out-of-domain questions (e.g., medical advice, car repair, international sports).

---

## 9. Hybrid Retrieval Latency Overhead Bound
The retrieval stage latency overhead introduced by BM25 tokenization and Reciprocal Rank Fusion calculation remains under **35 milliseconds on average** across 10 evaluation queries when compared to dense-only vector search.

**Why this target:**
- **System reference:** The `advice_threads` corpus contains 23 documents (averaging 543 characters). In-memory BM25 index scoring and reciprocal rank fusion should be computationally lightweight compared to network calls.
- **Why not stricter:** A stricter threshold (e.g., 5ms) could be breached by Python garbage collection spikes or OS process scheduling jitter on Windows.
- **Why not looser:** A looser threshold (e.g., 150ms) would indicate un-cached BM25 re-indexing or inefficient quadratic fusion loops.
- **Cost of being wrong:** Adding hybrid retrieval would double or triple retrieval latency, degrading overall query responsiveness.

---

# Milestone 4 Criteria Self-Check Audit Matrix

| # | Criterion Summary | Concrete Measurable Target | Stricter vs. Looser Justification | Failure / Bad Path? | Falsifiability ("What would make it fail?") |
|---|---|---|---|---|---|
| **1** | HTTP Latency | 4 of 5 in-scope queries answer in < 3.5s | 1.5s fails valid long text; 10s masks hangs | Normal Path | LLM API throttling or Chroma vector search timeout |
| **2** | Logging Traceability | 10 of 10 requests emit complete JSON record | 100% required; missing logs create blind spots | Bad + Good Paths | Logger disk write error or unhandled exception bypassing hook |
| **3** | Health Probe Accuracy | 200 on ready, 503 on missing index/key | Binary 200/503 aligns with orchestration standards | Bad Path (Unready) | Probe returns 200 even when collection does not exist |
| **4** | Boundary Defense | 3 of 3 malformed inputs get 400 + 0 tokens | Permitting even 1 of 3 risks DoS & token waste | **Bad Path (Input)** | Empty query reaches Gemini API or crashes with 500 |
| **5** | Graceful Degradation | 3 of 3 timeouts return 200 + excerpts | Unhandled crash leaves user with zero info | **Bad Path (Timeout)**| Service crashes with unhandled 500 on Gemini timeout |
| **6** | Vector Store Intercept | 3 of 3 index errors return 503 + guidance | Prevents cryptic stack traces; gives operator fix | **Bad Path (Storage)**| Unhandled Chroma error bubbles up as generic 500 |
| **7** | BM25 RRF Rank Boost | Exact keyword chunk at rank 1 or 2 in 4 of 5 | 5 of 5 ignores multi-chunk ties; 2 of 5 is ineffective | Normal Path | BM25 weight too weak; rank-1 chunk lacks keyword |
| **8** | Gate Refusal Fidelity | Refuses $\ge$ 4 of 5 out-of-scope questions | Refusing $\le$ 3 allows dangerous off-topic answers | **Bad Path (OOS)** | BM25 keyword overlap punctures distance gate |
| **9** | Hybrid Latency Bound | Overhead < 35ms avg across 10 queries | 5ms hits OS jitter; 150ms indicates re-indexing bug | Normal Path | Inefficient fusion algorithm or un-cached BM25 corpus rebuild |
