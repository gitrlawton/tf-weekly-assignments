#!/usr/bin/env python3
"""
The Unofficial Guide — Instrumented HTTP Service (Shape A).

    python serve.py                          run it locally on port 5000
    gunicorn serve:app --bind 0.0.0.0:5000   run it in production (Linux/POSIX)

Operational Features (Shape A):
  • Structured single-line JSON logging for every request (logs/requests.jsonl + stdout)
  • End-to-end and granular stage latency tracking (retrieval_ms, gate_ms, generation_ms)
  • Per-request token consumption accounting (prompt_tokens, output_tokens)
  • Traceable Request IDs via UUIDv4 and X-Request-ID response headers
  • Comprehensive readiness and liveness health checks on GET /health
  • In-memory aggregated observability metrics on GET /stats
"""

import os
import time
import uuid

from flask import Flask, g, jsonify, request

import config
from logger import log_request, read_recent_logs

app = Flask(__name__)

# In-memory operational metrics
_metrics = {
    "total_requests": 0,
    "successful_answers": 0,
    "refused_queries": 0,
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

    if status_code >= 400:
        _metrics["errors"] += 1
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
        "best_distance": extra.get("best_distance"),
        "prompt_tokens": extra.get("prompt_tokens", 0),
        "output_tokens": extra.get("output_tokens", 0),
        "error": extra.get("error"),
    }
    log_request(record)

    return response


@app.get("/health")
def health():
    """Operational readiness and liveness probe.

    Checks:
      1. ChromaDB vector index existence and item count
      2. GEMINI_API_KEY environment presence
    """
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
            "errors": _metrics["errors"],
            "average_latency_ms": avg_latency,
            "total_prompt_tokens": _metrics["total_prompt_tokens"],
            "total_output_tokens": _metrics["total_output_tokens"],
            "recent_log_count": len(read_recent_logs(10)),
        }
    )


@app.post("/ask")
def ask():
    """One question in, grounded answer with telemetry out."""
    from app import ask_pipeline

    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").strip()

    if not question:
        g.log_extra["error"] = "Empty or missing question"
        return (
            jsonify(
                {
                    "error": "Send JSON with a question in it, like "
                    '{"question": "is the housing lottery random?"}'
                }
            ),
            400,
        )

    g.log_extra["question"] = question

    try:
        outcome = ask_pipeline(question, corpus=config.CORPUS)
    except Exception as exc:  # noqa: BLE001
        g.log_extra["error"] = f"{type(exc).__name__}: {exc}"
        return jsonify({"error": f"{type(exc).__name__}: {exc}"}), 500

    timing = outcome.get("timing", {})
    tokens = outcome.get("tokens", {})

    g.log_extra["refused"] = outcome["refused"]
    g.log_extra["best_distance"] = round(outcome["best_distance"], 4)
    g.log_extra["retrieval_ms"] = timing.get("retrieval_ms", 0.0)
    g.log_extra["gate_ms"] = timing.get("gate_ms", 0.0)
    g.log_extra["generation_ms"] = timing.get("generation_ms", 0.0)
    g.log_extra["prompt_tokens"] = tokens.get("prompt", 0)
    g.log_extra["output_tokens"] = tokens.get("output", 0)

    return jsonify(
        {
            "question": question,
            "answer": outcome["answer"],
            "refused": outcome["refused"],
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
    print("Example cURL test:")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"question\": \"is the housing lottery random?\"}}'\n"
    )

    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
