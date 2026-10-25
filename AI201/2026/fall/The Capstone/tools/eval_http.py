#!/usr/bin/env python3
"""
HTTP Test & Evaluation Client for The Unofficial Guide.

Sends requests over HTTP to the running server (Path B / Shape A),
collecting latency, status codes, response headers, and verifying
responses against criteria benchmarks.
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


def send_request(url: str, payload: dict | None = None, method: str = "POST") -> dict:
    """Send an HTTP request using standard library urllib."""
    full_url = url
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8") if payload is not None else None

    req = urllib.request.Request(full_url, data=data, headers=headers, method=method)
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


def run_eval(base_url: str, runs: int = 3):
    base_url = base_url.rstrip("/")
    print(f"Testing server at: {base_url}")
    print("=" * 60)

    # 1. Health check
    print("\n[1] Checking /health...")
    health_resp = send_request(f"{base_url}/health", method="GET")
    print(f"    Status: {health_resp['status']} (took {health_resp['elapsed_ms']}ms)")
    print(f"    Detail: {health_resp['data'].get('detail', 'N/A')}")
    if health_resp["status"] != 200:
        print("    Server is not healthy. Aborting evaluation.")
        return

    # 2. In-scope benchmark questions
    print(f"\n[2] Running {len(qs.QUESTIONS)} benchmark questions ({runs} trials each)...")
    results = []

    for item in qs.QUESTIONS:
        q = item["question"]
        expects = item["expects"]
        print(f"\n  Question: {q}")
        q_results = []
        for r in range(1, runs + 1):
            resp = send_request(f"{base_url}/ask", {"question": q})
            data = resp.get("data", {})
            ans = data.get("answer", "")
            req_id = resp["headers"].get("X-Request-ID", "N/A")
            latency = resp["elapsed_ms"]
            refused = data.get("refused", False)
            contains_expected = expects.lower() in ans.lower() if not refused else False

            status_str = f"Run {r}: {latency}ms | Refused: {refused} | ReqID: {req_id[:8]}"
            print(f"    {status_str}")

            q_results.append({
                "run": r,
                "latency_ms": latency,
                "status": resp["status"],
                "refused": refused,
                "contains_expected": contains_expected,
                "req_id": req_id,
                "answer": ans,
                "sources": data.get("sources", []),
            })
        results.append({"question": q, "expects": expects, "trials": q_results})

    # 3. Out-of-scope gate questions
    print(f"\n[3] Testing {len(qs.OUT_OF_SCOPE)} out-of-scope questions against the gate...")
    gate_results = []
    for q in qs.OUT_OF_SCOPE:
        resp = send_request(f"{base_url}/ask", {"question": q})
        data = resp.get("data", {})
        refused = data.get("refused", False)
        print(f"    {q[:45]:<45} -> Refused: {refused} ({resp['elapsed_ms']}ms)")
        gate_results.append({"question": q, "refused": refused, "latency_ms": resp["elapsed_ms"]})

    # 4. In-memory stats check
    print("\n[4] Querying server /stats...")
    stats_resp = send_request(f"{base_url}/stats", method="GET")
    print("    Server Metrics:", json.dumps(stats_resp["data"], indent=6))

    print("\n" + "=" * 60)
    print("Evaluation completed successfully.")


def main():
    parser = argparse.ArgumentParser(description="Evaluate deployed HTTP service.")
    parser.add_argument("--url", default="http://localhost:5000", help="Base URL of service")
    parser.add_argument("--runs", type=int, default=3, help="Number of trials per question")
    args = parser.parse_args()

    run_eval(args.url, runs=args.runs)


if __name__ == "__main__":
    main()
