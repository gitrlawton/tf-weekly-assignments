#!/usr/bin/env python3
"""
Automated Fault-Injection Evaluation Suite for The Unofficial Guide (Shape B).

Runs multi-trial evaluations against bad paths and failure handling layers:
  1. Oversized Query (>1000 chars) -> HTTP 400 PAYLOAD_TOO_LARGE
  2. Empty / Whitespace Query -> HTTP 400 EMPTY_QUESTION
  3. Non-JSON / Bad Content-Type -> HTTP 400 INVALID_CONTENT_TYPE
  4. Vector Store Unreachability -> HTTP 503 INDEX_UNAVAILABLE
  5. Upstream Gemini Timeout -> HTTP 200 Graceful Degradation (excerpts + notice)
  6. Upstream Gemini Timeout (Strict) -> HTTP 504 Gateway Timeout

Outputs formatted run tables ready for Milestone 5 / criteria verification.
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


def send_http(
    url: str,
    payload: dict | str | None = None,
    headers: dict | None = None,
    method: str = "POST",
) -> dict:
    """Send an HTTP request and capture response metadata."""
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)

    if isinstance(payload, dict):
        data = json.dumps(payload).encode("utf-8")
    elif isinstance(payload, str):
        data = payload.encode("utf-8")
    else:
        data = None

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    start = time.perf_counter()

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            body = resp.read().decode("utf-8")
            return {
                "status": resp.status,
                "elapsed_ms": round(elapsed_ms, 2),
                "data": json.loads(body) if body else {},
                "headers": dict(resp.headers),
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
            "data": parsed,
            "headers": dict(exc.headers),
            "error": exc.reason,
        }
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        return {
            "status": 0,
            "elapsed_ms": round(elapsed_ms, 2),
            "data": {},
            "headers": {},
            "error": str(exc),
        }


def run_fault_evaluation(base_url: str, trials: int = 3):
    base_url = base_url.rstrip("/")
    ask_url = f"{base_url}/ask"

    print(f"Running Shape B Fault Injection Evaluation against: {base_url}")
    print("=" * 75)

    scenarios = [
        {
            "name": "1. Oversized Query (>1000 chars)",
            "payload": {"question": "What is the policy for " + "dorm " * 250},
            "headers": {},
            "expected_status": 400,
            "expected_code": "PAYLOAD_TOO_LARGE",
            "validate": lambda r: r["status"] == 400 and r["data"].get("code") == "PAYLOAD_TOO_LARGE",
        },
        {
            "name": "2. Empty / Whitespace Query",
            "payload": {"question": "   \n\t  "},
            "headers": {},
            "expected_status": 400,
            "expected_code": "EMPTY_QUESTION",
            "validate": lambda r: r["status"] == 400 and r["data"].get("code") == "EMPTY_QUESTION",
        },
        {
            "name": "3. Non-JSON Content-Type",
            "payload": "raw unformatted text string",
            "headers": {"Content-Type": "text/plain"},
            "expected_status": 400,
            "expected_code": "INVALID_CONTENT_TYPE",
            "validate": lambda r: r["status"] == 400 and r["data"].get("code") == "INVALID_CONTENT_TYPE",
        },
        {
            "name": "4. Vector Store Unreachability",
            "payload": {"question": "How much RAM do I need for CS?"},
            "headers": {"X-Simulate-Fault": "index_error"},
            "expected_status": 503,
            "expected_code": "INDEX_UNAVAILABLE",
            "validate": lambda r: r["status"] == 503 and r["data"].get("code") == "INDEX_UNAVAILABLE",
        },
        {
            "name": "5. Upstream Timeout (Graceful Degradation)",
            "payload": {"question": "How much RAM do I need for CS?"},
            "headers": {"X-Simulate-Fault": "timeout"},
            "expected_status": 200,
            "expected_code": "DEGRADED_OK",
            "validate": lambda r: (
                r["status"] == 200
                and r["data"].get("degraded") is True
                and len(r["data"].get("sources", [])) > 0
                and "NOTICE" in r["data"].get("answer", "")
            ),
        },
        {
            "name": "6. Upstream Timeout (Strict Mode)",
            "payload": {"question": "How much RAM do I need for CS?"},
            "headers": {"X-Simulate-Fault": "timeout", "X-Fail-Strict": "true"},
            "expected_status": 504,
            "expected_code": "UPSTREAM_TIMEOUT",
            "validate": lambda r: r["status"] == 504 and r["data"].get("code") == "UPSTREAM_TIMEOUT",
        },
    ]

    results_table = []

    for sc in scenarios:
        print(f"\nScenario: {sc['name']}")
        trial_outcomes = []
        sample_resp = None

        for t in range(1, trials + 1):
            resp = send_http(ask_url, payload=sc["payload"], headers=sc["headers"])
            passed = sc["validate"](resp)
            status_code = resp["status"]
            code = resp["data"].get("code") or ("DEGRADED_OK" if resp["data"].get("degraded") else "N/A")
            latency = resp["elapsed_ms"]

            trial_outcomes.append(passed)
            sample_resp = resp
            result_str = "PASS" if passed else "FAIL"
            print(f"  Run {t}: [{result_str}] HTTP {status_code} ({code}) in {latency}ms")

        success_count = sum(trial_outcomes)
        results_table.append(
            {
                "scenario": sc["name"],
                "target": f"{trials} of {trials}",
                "runs": [f"Run {i+1}: {'PASS' if p else 'FAIL'}" for i, p in enumerate(trial_outcomes)],
                "verdict": "MET" if success_count == trials else "MISSED",
                "sample": sample_resp,
            }
        )

    print("\n" + "=" * 75)
    print("SHAPE B RUN LOG SUMMARY")
    print("=" * 75)
    print(f"{'Criterion / Scenario':<42} | {'Target':<8} | {'Run 1':<6} | {'Run 2':<6} | {'Run 3':<6} | {'Verdict'}")
    print("-" * 75)

    for row in results_table:
        r1 = "PASS" if "PASS" in row["runs"][0] else "FAIL"
        r2 = "PASS" if "PASS" in row["runs"][1] else "FAIL"
        r3 = "PASS" if "PASS" in row["runs"][2] else "FAIL"
        print(f"{row['scenario']:<42} | {row['target']:<8} | {r1:<6} | {r2:<6} | {r3:<6} | {row['verdict']}")

    print("=" * 75)


def main():
    parser = argparse.ArgumentParser(description="Evaluate Shape B failure resilience.")
    parser.add_argument("--url", default="http://localhost:5000", help="Base URL of service")
    parser.add_argument("--trials", type=int, default=3, help="Number of trials per scenario")
    args = parser.parse_args()

    run_fault_evaluation(args.url, trials=args.trials)


if __name__ == "__main__":
    main()
