#!/usr/bin/env python3
"""
Comparative Evaluation Client: Dense vs. Hybrid Retrieval (Shape C).

Sends paired requests over HTTP to the running server comparing:
  1. Dense-Only Retrieval (ChromaDB cosine semantic search)
  2. Hybrid Retrieval (BM25 Lexical + ChromaDB Dense via Reciprocal Rank Fusion)

Measures:
  • Source retrieval agreement & ranking shifts
  • Retrieval stage latency (BM25 overhead vs dense embedding)
  • Preservation of refusal gates on out-of-scope questions
  • RRF fusion scores and distance metrics
"""

import argparse
import json
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import questions as qs

# Additional keyword-sensitive queries to evaluate lexical vs semantic strengths
KEYWORD_QUESTIONS = [
    {
        "question": "What are the laptop and RAM recommendations for computer science?",
        "keyword": "RAM",
        "description": "Term-specific hardware query",
    },
    {
        "question": "Who should you talk to first about roommate conflict resolution?",
        "keyword": "RA",
        "description": "Housing policy keyword query",
    },
]


def send_http_request(url: str, payload: dict | None = None, method: str = "POST") -> dict:
    """Send an HTTP request and parse response with telemetry."""
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    start = time.perf_counter()

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            body = resp.read().decode("utf-8")
            return {
                "status": resp.status,
                "elapsed_ms": round(elapsed_ms, 2),
                "headers": dict(resp.headers),
                "data": json.loads(body) if body else {},
                "error": None,
            }
    except urllib.error.HTTPError as exc:
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"raw": body}
        return {
            "status": exc.code,
            "elapsed_ms": round(elapsed_ms, 2),
            "headers": dict(exc.headers),
            "data": parsed,
            "error": exc.reason,
        }
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        return {
            "status": 0,
            "elapsed_ms": round(elapsed_ms, 2),
            "headers": {},
            "data": {},
            "error": str(exc),
        }


def run_comparative_eval(base_url: str):
    base_url = base_url.rstrip("/")
    print(f"\nEvaluating Dense vs. Hybrid Retrieval on: {base_url}")
    print("=" * 72)

    # 1. Health Probe
    health_resp = send_http_request(f"{base_url}/health", method="GET")
    if health_resp["status"] != 200:
        print(f"[FAIL] Server health check failed: {health_resp}")
        sys.exit(1)
    print(f"[OK] Server is ready (corpus: {health_resp['data'].get('corpus')})\n")

    test_suite = []
    # Benchmark in-scope questions
    for item in qs.QUESTIONS:
        test_suite.append({
            "question": item["question"],
            "type": "in_scope",
            "expects": item["expects"],
        })
    # Out-of-scope questions
    for item in qs.OUT_OF_SCOPE:
        q_text = item["question"] if isinstance(item, dict) else str(item)
        test_suite.append({
            "question": q_text,
            "type": "out_of_scope",
            "expects": None,
        })
    # Keyword-specific queries
    for item in KEYWORD_QUESTIONS:
        test_suite.append({
            "question": item["question"],
            "type": "keyword",
            "expects": item["keyword"],
        })

    dense_latencies = []
    hybrid_latencies = []
    dense_retrieval_ms_list = []
    hybrid_retrieval_ms_list = []
    top_source_agreements = 0
    total_comparisons = 0

    in_scope_dense_pass = 0
    in_scope_hybrid_pass = 0
    in_scope_total = 0

    oos_dense_refused = 0
    oos_hybrid_refused = 0
    oos_total = 0

    print(f"{'#':<3} {'Type':<12} {'Question':<40} {'Dense Top-1':<18} {'Hybrid Top-1':<18} {'RRF':<8}")
    print("-" * 105)

    for i, test in enumerate(test_suite, 1):
        q = test["question"]
        q_type = test["type"]
        short_q = (q[:37] + "...") if len(q) > 40 else q

        # Run Dense Query
        resp_dense = send_http_request(f"{base_url}/ask", {"question": q, "hybrid": False})
        data_dense = resp_dense.get("data", {})
        timing_dense = data_dense.get("timing_ms", {})
        retrieval_d = timing_dense.get("retrieval", 0.0)
        total_d = resp_dense.get("elapsed_ms", 0.0)
        sources_d = data_dense.get("sources", [])
        top_d = sources_d[0] if sources_d else ("REFUSED" if data_dense.get("refused") else "NONE")

        # Run Hybrid Query
        resp_hybrid = send_http_request(f"{base_url}/ask", {"question": q, "hybrid": True})
        data_hybrid = resp_hybrid.get("data", {})
        timing_hybrid = data_hybrid.get("timing_ms", {})
        retrieval_h = timing_hybrid.get("retrieval", 0.0)
        total_h = resp_hybrid.get("elapsed_ms", 0.0)
        sources_h = data_hybrid.get("sources", [])
        top_h = sources_h[0] if sources_h else ("REFUSED" if data_hybrid.get("refused") else "NONE")
        rrf_score = data_hybrid.get("rrf_score")
        rrf_str = f"{rrf_score:.4f}" if isinstance(rrf_score, (int, float)) else "N/A"

        dense_latencies.append(total_d)
        hybrid_latencies.append(total_h)
        dense_retrieval_ms_list.append(retrieval_d)
        hybrid_retrieval_ms_list.append(retrieval_h)

        if top_d == top_h:
            top_source_agreements += 1
        total_comparisons += 1

        if q_type in ("in_scope", "keyword"):
            in_scope_total += 1
            if not data_dense.get("refused", False):
                in_scope_dense_pass += 1
            if not data_hybrid.get("refused", False):
                in_scope_hybrid_pass += 1
        elif q_type == "out_of_scope":
            oos_total += 1
            if data_dense.get("refused", False):
                oos_dense_refused += 1
            if data_hybrid.get("refused", False):
                oos_hybrid_refused += 1

        print(f"{i:<3} {q_type:<12} {short_q:<40} {top_d[:17]:<18} {top_h[:17]:<18} {rrf_str:<8}")

    print("=" * 105)
    print("\nSummary & Statistical Comparison:")
    print("-" * 50)
    avg_dense_retrieval = sum(dense_retrieval_ms_list) / len(dense_retrieval_ms_list) if dense_retrieval_ms_list else 0
    avg_hybrid_retrieval = sum(hybrid_retrieval_ms_list) / len(hybrid_retrieval_ms_list) if hybrid_retrieval_ms_list else 0
    retrieval_overhead = avg_hybrid_retrieval - avg_dense_retrieval

    avg_dense_total = sum(dense_latencies) / len(dense_latencies) if dense_latencies else 0
    avg_hybrid_total = sum(hybrid_latencies) / len(hybrid_latencies) if hybrid_latencies else 0

    agreement_pct = (top_source_agreements / total_comparisons * 100.0) if total_comparisons > 0 else 0

    print(f"Total Questions Evaluated:       {total_comparisons}")
    print(f"Top-1 Source Agreement Rate:     {agreement_pct:.1f}% ({top_source_agreements}/{total_comparisons})")
    print(f"Avg Retrieval Latency (Dense):   {avg_dense_retrieval:.2f} ms")
    print(f"Avg Retrieval Latency (Hybrid):  {avg_hybrid_retrieval:.2f} ms (overhead: +{retrieval_overhead:.2f} ms)")
    print(f"Avg Total Request Time (Dense):  {avg_dense_total:.2f} ms")
    print(f"Avg Total Request Time (Hybrid): {avg_hybrid_total:.2f} ms")
    print(f"In-Scope Answer Rate (Dense):    {in_scope_dense_pass}/{in_scope_total} ({(in_scope_dense_pass/in_scope_total)*100:.1f}%)")
    print(f"In-Scope Answer Rate (Hybrid):   {in_scope_hybrid_pass}/{in_scope_total} ({(in_scope_hybrid_pass/in_scope_total)*100:.1f}%)")
    print(f"Out-of-Scope Refusal (Dense):    {oos_dense_refused}/{oos_total} ({(oos_dense_refused/oos_total)*100:.1f}%)")
    print(f"Out-of-Scope Refusal (Hybrid):   {oos_hybrid_refused}/{oos_total} ({(oos_hybrid_refused/oos_total)*100:.1f}%)")

    # Fetch stats endpoint to verify metric counter increment
    stats_resp = send_http_request(f"{base_url}/stats", method="GET")
    stats_data = stats_resp.get("data", {})
    hybrid_count = stats_data.get("hybrid_queries", 0)
    print(f"\nServer Observability Verification:")
    print(f"  Hybrid Queries Logged in /stats: {hybrid_count}")

    all_passed = (
        in_scope_hybrid_pass == in_scope_total
        and oos_hybrid_refused == oos_total
        and hybrid_count > 0
    )

    if all_passed:
        print("\n[SUCCESS] Shape C Hybrid Retrieval evaluation passed all validation criteria!")
        return 0
    else:
        print("\n[WARNING] Some criteria did not meet expected thresholds.")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Evaluate Dense vs. Hybrid Retrieval")
    parser.add_argument(
        "--url",
        default="http://localhost:5000",
        help="Base URL of running server (default: http://localhost:5000)",
    )
    args = parser.parse_args()
    code = run_comparative_eval(args.url)
    sys.exit(code)


if __name__ == "__main__":
    main()
