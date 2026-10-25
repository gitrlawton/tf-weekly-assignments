#!/usr/bin/env python3
"""
The Unofficial Guide — Resilient & Observable HTTP Service (Shape A + B + C).

    python serve.py                          run it locally on port 5000
    gunicorn serve:app --bind 0.0.0.0:5000   run it in production (Linux/POSIX)

Operational Features (Shape A):
  • Structured single-line JSON logging for every request (logs/requests.jsonl + stdout)
  • End-to-end and granular stage latency tracking (retrieval_ms, gate_ms, generation_ms)
  • Per-request token consumption accounting (prompt_tokens, output_tokens)
  • Traceable Request IDs via UUIDv4 and X-Request-ID response headers
  • Comprehensive readiness and liveness health checks on GET /health
  • In-memory aggregated observability metrics on GET /stats

Hardening & Resilience Features (Shape B):
  • Inbound payload validation & boundary defense (400 Bad Request on empty, malformed, or >1000 char queries)
  • Vector store unreachability interception (503 Service Unavailable with remediation guidance)
  • Upstream model timeout protection & graceful degradation (returning retrieved excerpts on Gemini outage)
  • Deterministic fault simulation headers (X-Simulate-Fault, X-Fail-Strict) for automated evaluation
  • Machine-readable standardized JSON error envelopes

Capability Enhancement (Shape C):
  • Hybrid Retrieval combining BM25 keyword matching with Chroma vector semantic search
  • Reciprocal Rank Fusion (RRF) combining dense & sparse scores with tunable k_rrf parameter
  • Request-level feature toggle ("hybrid": true) on POST /ask
"""

import os
import time
import uuid

from flask import Flask, g, jsonify, request

import config
from exceptions import (
    CapstoneError,
    PayloadValidationError,
    UpstreamModelTimeoutError,
    VectorStoreUnavailableError,
    make_error_envelope,
)
from logger import log_request, read_recent_logs

app = Flask(__name__)

# In-memory operational metrics
_metrics = {
    "total_requests": 0,
    "successful_answers": 0,
    "refused_queries": 0,
    "degraded_answers": 0,
    "hybrid_queries": 0,
    "errors": 0,
    "total_latency_ms": 0.0,
    "total_prompt_tokens": 0,
    "total_output_tokens": 0,
}


@app.before_request
def before_request_hook():
    """Initialize request-scoped tracing context."""
    g.start_time = time.perf_counter()
    g.request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    g.log_extra = {
        "question": None,
        "refused": False,
        "degraded": False,
        "hybrid": False,
        "rrf_score": None,
        "best_distance": None,
        "retrieval_ms": 0.0,
        "gate_ms": 0.0,
        "generation_ms": 0.0,
        "prompt_tokens": 0,
        "output_tokens": 0,
        "error": None,
    }


@app.after_request
def after_request_hook(response):
    """Record duration, update headers, and emit structured JSON log."""
    elapsed_ms = (time.perf_counter() - getattr(g, "start_time", time.perf_counter())) * 1000.0
    elapsed_ms = round(elapsed_ms, 2)
    request_id = getattr(g, "request_id", str(uuid.uuid4()))

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time-MS"] = str(elapsed_ms)

    extra = getattr(g, "log_extra", {})
    status_code = response.status_code

    # Update in-memory metrics
    _metrics["total_requests"] += 1
    _metrics["total_latency_ms"] += elapsed_ms
    _metrics["total_prompt_tokens"] += extra.get("prompt_tokens", 0)
    _metrics["total_output_tokens"] += extra.get("output_tokens", 0)

    if extra.get("hybrid", False):
        _metrics["hybrid_queries"] += 1

    if status_code >= 400:
        _metrics["errors"] += 1
    elif extra.get("degraded", False):
        _metrics["degraded_answers"] += 1
    elif extra.get("refused", False):
        _metrics["refused_queries"] += 1
    else:
        _metrics["successful_answers"] += 1

    record = {
        "request_id": request_id,
        "client_ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "endpoint": request.path,
        "method": request.method,
        "status_code": status_code,
        "latency_ms": elapsed_ms,
        "retrieval_ms": extra.get("retrieval_ms", 0.0),
        "gate_ms": extra.get("gate_ms", 0.0),
        "generation_ms": extra.get("generation_ms", 0.0),
        "question": extra.get("question"),
        "refused": extra.get("refused", False),
        "degraded": extra.get("degraded", False),
        "hybrid": extra.get("hybrid", False),
        "rrf_score": extra.get("rrf_score"),
        "best_distance": extra.get("best_distance"),
        "prompt_tokens": extra.get("prompt_tokens", 0),
        "output_tokens": extra.get("output_tokens", 0),
        "error": extra.get("error"),
    }
    log_request(record)

    return response


# ─── Error Handlers (Shape B Middleware) ──────────────────────────────────────


@app.errorhandler(PayloadValidationError)
def handle_payload_validation_error(exc: PayloadValidationError):
    """Client input error (400 Bad Request)."""
    req_id = getattr(g, "request_id", None)
    g.log_extra["error"] = f"{exc.code}: {exc.message}"
    envelope = make_error_envelope(
        error="Bad Request",
        message=exc.message,
        code=exc.code,
        status_code=400,
        request_id=req_id,
    )
    return jsonify(envelope), 400


@app.errorhandler(VectorStoreUnavailableError)
def handle_vector_store_error(exc: VectorStoreUnavailableError):
    """Vector database unavailable or unindexed (503 Service Unavailable)."""
    req_id = getattr(g, "request_id", None)
    g.log_extra["error"] = f"{exc.code}: {exc.message}"
    envelope = make_error_envelope(
        error="Service Unavailable",
        message=exc.message,
        code=exc.code,
        status_code=503,
        request_id=req_id,
    )
    return jsonify(envelope), 503


@app.errorhandler(UpstreamModelTimeoutError)
def handle_timeout_error(exc: UpstreamModelTimeoutError):
    """Generative AI timeout when strict failure mode is enabled (504 Gateway Timeout)."""
    req_id = getattr(g, "request_id", None)
    g.log_extra["error"] = f"{exc.code}: {exc.message}"
    envelope = make_error_envelope(
        error="Gateway Timeout",
        message=exc.message,
        code=exc.code,
        status_code=504,
        request_id=req_id,
    )
    return jsonify(envelope), 504


@app.errorhandler(CapstoneError)
def handle_generic_capstone_error(exc: CapstoneError):
    req_id = getattr(g, "request_id", None)
    g.log_extra["error"] = f"{exc.code}: {exc.message}"
    envelope = make_error_envelope(
        error="Internal Server Error",
        message=exc.message,
        code=exc.code,
        status_code=exc.status_code,
        request_id=req_id,
    )
    return jsonify(envelope), exc.status_code


@app.errorhandler(404)
def handle_not_found(exc):
    req_id = getattr(g, "request_id", None)
    envelope = make_error_envelope(
        error="Not Found",
        message=f"Endpoint '{request.path}' does not exist on this server.",
        code="ENDPOINT_NOT_FOUND",
        status_code=404,
        request_id=req_id,
    )
    return jsonify(envelope), 404


# ─── Endpoints ───────────────────────────────────────────────────────────────


@app.get("/health")
def health():
    """Operational readiness and liveness probe."""
    from store import index_exists, _client

    has_index = index_exists(config.CORPUS)
    doc_count = 0
    if has_index:
        try:
            col = _client().get_collection(config.collection_name(config.CORPUS))
            doc_count = col.count()
        except Exception:
            pass

    has_key = bool(os.getenv("GEMINI_API_KEY", "").strip())
    ready = has_index and has_key

    status_payload = {
        "status": "ready" if ready else "not_ready",
        "corpus": config.CORPUS,
        "index_ready": has_index,
        "chunk_count": doc_count,
        "api_key_configured": has_key,
        "detail": (
            "System healthy and ready to answer queries"
            if ready
            else (
                "Index missing — run `python app.py index`"
                if not has_index
                else "GEMINI_API_KEY is not set"
            )
        ),
    }

    return jsonify(status_payload), (200 if ready else 503)


@app.get("/stats")
def stats():
    """Aggregated in-memory operational metrics."""
    avg_latency = (
        round(_metrics["total_latency_ms"] / _metrics["total_requests"], 2)
        if _metrics["total_requests"] > 0
        else 0.0
    )
    return jsonify(
        {
            "corpus": config.CORPUS,
            "total_requests": _metrics["total_requests"],
            "successful_answers": _metrics["successful_answers"],
            "refused_queries": _metrics["refused_queries"],
            "degraded_answers": _metrics["degraded_answers"],
            "hybrid_queries": _metrics["hybrid_queries"],
            "errors": _metrics["errors"],
            "average_latency_ms": avg_latency,
            "total_prompt_tokens": _metrics["total_prompt_tokens"],
            "total_output_tokens": _metrics["total_output_tokens"],
            "recent_log_count": len(read_recent_logs(10)),
        }
    )


@app.post("/ask")
def ask():
    """One question in, resilient answer with telemetry out."""
    from app import ask_pipeline
    from store import index_exists

    # 1. Input Validation & Boundary Defense (Shape B)
    if not request.is_json:
        raise PayloadValidationError(
            "Request Content-Type must be 'application/json' with a valid JSON body.",
            code="INVALID_CONTENT_TYPE",
        )

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise PayloadValidationError(
            "Request payload must be a JSON object containing a 'question' key.",
            code="INVALID_PAYLOAD_STRUCTURE",
        )

    if "question" not in payload:
        raise PayloadValidationError(
            "Missing required field 'question' in request body.",
            code="MISSING_QUESTION_FIELD",
        )

    raw_question = payload.get("question")
    if not isinstance(raw_question, str):
        raise PayloadValidationError(
            f"Field 'question' must be a string, got {type(raw_question).__name__}.",
            code="INVALID_QUESTION_TYPE",
        )

    question = raw_question.strip()
    if not question:
        raise PayloadValidationError(
            "Question cannot be empty or whitespace only.",
            code="EMPTY_QUESTION",
        )

    MAX_QUESTION_LENGTH = 1000
    if len(question) > MAX_QUESTION_LENGTH:
        raise PayloadValidationError(
            f"Question exceeds maximum allowed length of {MAX_QUESTION_LENGTH} characters (received {len(question)}).",
            code="PAYLOAD_TOO_LARGE",
        )

    # Shape C capability toggle
    hybrid = bool(payload.get("hybrid", False))

    g.log_extra["question"] = question
    g.log_extra["hybrid"] = hybrid

    # 2. Vector Store Readiness Guard (Shape B)
    if not index_exists(config.CORPUS):
        raise VectorStoreUnavailableError(
            f"Vector index for corpus '{config.CORPUS}' is uninitialized or missing. "
            f"Run `python app.py index` to build the collection."
        )

    # 3. Deterministic Fault-Injection Simulation (For Testing / Milestone 5)
    sim_fault = (request.headers.get("X-Simulate-Fault") or "").strip().lower()
    fail_strict = (
        request.headers.get("X-Fail-Strict", "").strip().lower() in ("1", "true", "yes")
    )

    if sim_fault == "index_error":
        raise VectorStoreUnavailableError("Simulated vector index corruption or unreachability.")
    elif sim_fault == "timeout" and fail_strict:
        raise UpstreamModelTimeoutError("Simulated upstream Gemini API timeout (strict mode).")

    # 4. Pipeline Execution with Graceful Fallback
    try:
        outcome = ask_pipeline(
            question,
            corpus=config.CORPUS,
            hybrid=hybrid,
            fallback_degradation=not fail_strict,
            timeout=0.0001 if sim_fault == "timeout" else None,
        )
    except UpstreamModelTimeoutError as exc:
        raise exc
    except Exception as exc:  # noqa: BLE001
        g.log_extra["error"] = f"{type(exc).__name__}: {exc}"
        envelope = make_error_envelope(
            error="Internal Server Error",
            message=f"{type(exc).__name__}: {exc}",
            code="PIPELINE_ERROR",
            status_code=500,
            request_id=getattr(g, "request_id", None),
        )
        return jsonify(envelope), 500

    timing = outcome.get("timing", {})
    tokens = outcome.get("tokens", {})

    g.log_extra["refused"] = outcome["refused"]
    g.log_extra["degraded"] = outcome.get("degraded", False)
    g.log_extra["hybrid"] = outcome.get("hybrid", False)
    g.log_extra["rrf_score"] = outcome.get("rrf_score")
    g.log_extra["best_distance"] = round(outcome["best_distance"], 4)
    g.log_extra["retrieval_ms"] = timing.get("retrieval_ms", 0.0)
    g.log_extra["gate_ms"] = timing.get("gate_ms", 0.0)
    g.log_extra["generation_ms"] = timing.get("generation_ms", 0.0)
    g.log_extra["prompt_tokens"] = tokens.get("prompt", 0)
    g.log_extra["output_tokens"] = tokens.get("output", 0)
    if outcome.get("degraded"):
        g.log_extra["error"] = outcome.get("error_detail")

    return jsonify(
        {
            "question": question,
            "answer": outcome["answer"],
            "refused": outcome["refused"],
            "degraded": outcome.get("degraded", False),
            "hybrid": outcome.get("hybrid", False),
            "rrf_score": outcome.get("rrf_score"),
            "error_detail": outcome.get("error_detail"),
            "sources": outcome["sources"],
            "best_distance": round(outcome["best_distance"], 4),
            "threshold": outcome["threshold"],
            "corpus": config.CORPUS,
            "timing_ms": {
                "retrieval": timing.get("retrieval_ms", 0.0),
                "gate": timing.get("gate_ms", 0.0),
                "generation": timing.get("generation_ms", 0.0),
            },
            "tokens": tokens,
        }
    )


def main():
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"Serving The Unofficial Guide on http://localhost:{port}")
    print(f"Corpus: {config.CORPUS}    (Ctrl-C to stop)\n")
    print("Available Routes:")
    print(f"  GET  http://localhost:{port}/health")
    print(f"  GET  http://localhost:{port}/stats")
    print(f"  POST http://localhost:{port}/ask\n")

    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
