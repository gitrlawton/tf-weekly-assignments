#!/usr/bin/env python3
"""
Comprehensive 3-Run Evaluation Runner for Milestone 5.

Executes all 9 criteria across 3 independent runs against the running HTTP server,
evaluates targets, computes verdicts, and produces the complete Run Log table
and pasted real outputs for README.md.

Usage:
    python tools/run_capstone_evals.py --url http://localhost:5000
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

KEYWORD_TESTS = [
    {
        "question": "How much RAM do I need for CS courses?",
        "keyword_doc": "thread_laptop_specs.txt",
        "keyword": "RAM",
    },
    {
        "question": "When is the deadline to change your meal plan tier?",
        "keyword_doc": "thread_meal_plan_tier.txt",
        "keyword": "tier",
    },
    {
        "question": "Who should you talk to first about roommate conflict resolution?",
        "keyword_doc": "thread_roommate_conflict.txt",
        "keyword": "RA",
    },
    {
        "question": "What happens if you turn in an assignment late?",
        "keyword_doc": "thread_late_work.txt",
        "keyword": "late",
    },
    {
        "question": "When should you use the pass/fail grading option?",
        "keyword_doc": "thread_pass_fail.txt",
        "keyword": "pass/fail",
    },
]

TEN_COST_QUERIES = [
    "How much RAM do I need for CS courses?",
    "When is the deadline to change your meal plan tier?",
    "Is a bike worth it for a 20 minute commute?",
    "What is the first step if you have a roommate conflict?",
    "What happens if you turn in an assignment late?",
    "Is the campus printing quota enough for the semester?",
    "Can freshmen bring a car and park on campus?",
    "What is the best time to do laundry in dorms?",
    "Where are the quietest study spots during finals week?",
    "When should you use the pass/fail grading option?",
]


def send_http(url: str, payload=None, headers=None, method="POST") -> dict:
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)

    if isinstance(payload, dict):
        data = json.dumps(payload).encode("utf-8")
    elif isinstance(payload, (str, bytes)):
        data = payload.encode("utf-8") if isinstance(payload, str) else payload
    else:
        data = None

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    t0 = time.perf_counter()

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            body = resp.read().decode("utf-8")
            return {
                "status": resp.status,
                "elapsed_ms": round(elapsed_ms, 2),
                "headers": dict(resp.headers),
                "data": json.loads(body) if body else {},
                "error": None,
            }
    except urllib.error.HTTPError as exc:
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
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
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "status": 0,
            "elapsed_ms": round(elapsed_ms, 2),
            "headers": {},
            "data": {},
            "error": str(exc),
        }


def run_single_eval_cycle(base_url: str, cycle_num: int) -> dict:
    print(f"\n=======================================================")
    print(f"RUNNING EVALUATION CYCLE {cycle_num} OF 3")
    print(f"=======================================================")
    base_url = base_url.rstrip("/")
    results = {}
    pasted_samples = {}

    # --- CRITERION 1: Endpoint Latency < 3.5s (Shape A) ---
    print(f"[Cycle {cycle_num}] Testing Criterion 1: Endpoint Latency (< 3.5s)...")
    c1_passed = 0
    c1_samples = []
    for q_item in qs.QUESTIONS:
        resp = send_http(f"{base_url}/ask", {"question": q_item["question"], "cache": False})
        lat = resp["elapsed_ms"]
        ok = (resp["status"] == 200) and (lat < 3500.0)
        if ok:
            c1_passed += 1
        c1_samples.append({"q": q_item["question"], "lat": lat, "status": resp["status"]})
    results["c1"] = f"{c1_passed}/5"
    pasted_samples["c1"] = c1_samples[0]
    print(f"  Result: {results['c1']} queries answered under 3.5s")

    # --- CRITERION 2: Logging Traceability (Shape A) ---
    print(f"[Cycle {cycle_num}] Testing Criterion 2: 10 of 10 Logging Traceability...")
    from logger import read_recent_logs
    # Fire 10 distinct requests
    send_http(f"{base_url}/health", method="GET")
    send_http(f"{base_url}/stats", method="GET")
    send_http(f"{base_url}/ask", {"question": "How much RAM do I need for CS courses?", "cache": False})
    send_http(f"{base_url}/ask", {"question": "When is the deadline to change your meal plan tier?", "cache": False})
    send_http(f"{base_url}/ask", {"question": "Is a bike worth it for a 20 minute commute?", "cache": False})
    send_http(f"{base_url}/ask", {"question": "What is the first step if you have a roommate conflict?", "cache": False})
    send_http(f"{base_url}/ask", {"question": "What is the capital of Mongolia?"})
    send_http(f"{base_url}/ask", {"question": "How do I change the oil in a diesel engine?"})
    send_http(f"{base_url}/health", method="GET")
    send_http(f"{base_url}/stats", method="GET")

    recent = read_recent_logs(10)
    valid_logs = 0
    for r in recent:
        if all(k in r for k in ("timestamp", "request_id", "endpoint", "status_code", "latency_ms", "retrieval_ms")):
            valid_logs += 1
    results["c2"] = f"{valid_logs}/10"
    pasted_samples["c2"] = recent[-1] if recent else {}
    print(f"  Result: {results['c2']} valid structured log records")

    # --- CRITERION 3: Health Probe Accuracy (Shape A) ---
    print(f"[Cycle {cycle_num}] Testing Criterion 3: Health Probe Accuracy...")
    resp_ready = send_http(f"{base_url}/health", method="GET")
    resp_unready = send_http(f"{base_url}/health", headers={"X-Simulate-Fault": "index_error"}, method="GET")
    ok_ready = (resp_ready["status"] == 200) and (resp_ready["data"].get("status") == "ready")
    ok_unready = (resp_unready["status"] == 503) and (resp_unready["data"].get("status") == "not_ready")
    c3_pass = (ok_ready and ok_unready)
    results["c3"] = "PASS" if c3_pass else "FAIL"
    pasted_samples["c3"] = {"ready": resp_ready["data"], "unready": resp_unready["data"]}
    print(f"  Result: {results['c3']} (Ready: {resp_ready['status']}, Unready: {resp_unready['status']})")

    # --- CRITERION 4: Inbound Boundary Defense (Shape B) ---
    print(f"[Cycle {cycle_num}] Testing Criterion 4: Inbound Boundary Defense...")
    resp_oversize = send_http(f"{base_url}/ask", {"question": "A" * 1250})
    resp_empty = send_http(f"{base_url}/ask", {"question": "    "})
    resp_nonjson = send_http(f"{base_url}/ask", payload="plain text", headers={"Content-Type": "text/plain"})

    c4_pass = 0
    if resp_oversize["status"] == 400 and resp_oversize["data"].get("code") == "PAYLOAD_TOO_LARGE":
        c4_pass += 1
    if resp_empty["status"] == 400 and resp_empty["data"].get("code") == "EMPTY_QUESTION":
        c4_pass += 1
    if resp_nonjson["status"] == 400 and resp_nonjson["data"].get("code") == "INVALID_CONTENT_TYPE":
        c4_pass += 1
    results["c4"] = f"{c4_pass}/3"
    pasted_samples["c4"] = resp_oversize["data"]
    print(f"  Result: {results['c4']} input defenses met")

    # --- CRITERION 5: Upstream Timeout Graceful Degradation (Shape B) ---
    print(f"[Cycle {cycle_num}] Testing Criterion 5: Upstream Timeout Degradation...")
    resp_timeout = send_http(
        f"{base_url}/ask",
        {"question": "What is the policy for late assignment submission?", "cache": False},
        headers={"X-Simulate-Fault": "timeout"},
    )
    is_degraded = (
        resp_timeout["status"] == 200
        and resp_timeout["data"].get("degraded") is True
        and "NOTICE" in resp_timeout["data"].get("answer", "")
    )
    results["c5"] = "PASS" if is_degraded else "FAIL"
    pasted_samples["c5"] = resp_timeout["data"]
    print(f"  Result: {results['c5']} (Status: {resp_timeout['status']}, Degraded: {resp_timeout['data'].get('degraded')})")

    # --- CRITERION 6: Vector Store Unreachability Protection (Shape B) ---
    print(f"[Cycle {cycle_num}] Testing Criterion 6: Vector Store Unreachability...")
    resp_index = send_http(
        f"{base_url}/ask",
        {"question": "How much RAM do I need for CS courses?"},
        headers={"X-Simulate-Fault": "index_error"},
    )
    is_index_err = (
        resp_index["status"] == 503
        and resp_index["data"].get("code") == "INDEX_UNAVAILABLE"
    )
    results["c6"] = "PASS" if is_index_err else "FAIL"
    pasted_samples["c6"] = resp_index["data"]
    print(f"  Result: {results['c6']} (Status: {resp_index['status']}, Code: {resp_index['data'].get('code')})")

    # --- CRITERION 7: BM25 Lexical Ranking Boost (Shape C) ---
    print(f"[Cycle {cycle_num}] Testing Criterion 7: BM25 Lexical Ranking Boost...")
    c7_pass = 0
    c7_sample_item = None
    for item in KEYWORD_TESTS:
        resp_h = send_http(f"{base_url}/ask", {"question": item["question"], "hybrid": True})
        ranked = resp_h["data"].get("ranked_sources") or resp_h["data"].get("sources", [])
        # Check if keyword_doc is within top 2
        top2 = ranked[:2]
        if item["keyword_doc"] in top2:
            c7_pass += 1
        if not c7_sample_item:
            c7_sample_item = {"q": item["question"], "ranked_sources": ranked, "rrf": resp_h["data"].get("rrf_score")}
    results["c7"] = f"{c7_pass}/5"
    pasted_samples["c7"] = c7_sample_item
    print(f"  Result: {results['c7']} keyword queries ranked in top 2")

    # --- CRITERION 8: Relevance Gate Preservation Under Hybrid (Shape C) ---
    print(f"[Cycle {cycle_num}] Testing Criterion 8: Gate Preservation Under Hybrid...")
    c8_pass = 0
    c8_sample_item = None
    for oos in qs.OUT_OF_SCOPE:
        resp_oos = send_http(f"{base_url}/ask", {"question": oos, "hybrid": True})
        if resp_oos["data"].get("refused") is True and resp_oos["data"].get("best_distance", 0) > 0.6:
            c8_pass += 1
        if not c8_sample_item:
            c8_sample_item = {"q": oos, "refused": resp_oos["data"].get("refused"), "dist": resp_oos["data"].get("best_distance")}
    results["c8"] = f"{c8_pass}/5"
    pasted_samples["c8"] = c8_sample_item
    print(f"  Result: {results['c8']} out-of-scope questions refused")

    # --- CRITERION 9: Hybrid Retrieval Overhead Bound < 35ms (Shape C) ---
    print(f"[Cycle {cycle_num}] Testing Criterion 9: Hybrid Retrieval Overhead Bound...")
    dense_times = []
    hybrid_times = []
    for q in TEN_COST_QUERIES:
        r_d = send_http(f"{base_url}/ask", {"question": q, "hybrid": False, "cache": True})
        r_h = send_http(f"{base_url}/ask", {"question": q, "hybrid": True, "cache": True})
        dense_times.append(r_d["data"].get("timing_ms", {}).get("retrieval", 0.0))
        hybrid_times.append(r_h["data"].get("timing_ms", {}).get("retrieval", 0.0))

    avg_d = sum(dense_times) / len(dense_times) if dense_times else 0
    avg_h = sum(hybrid_times) / len(hybrid_times) if hybrid_times else 0
    overhead = avg_h - avg_d
    c9_pass = overhead < 35.0
    results["c9"] = f"{overhead:+.2f}ms"
    pasted_samples["c9"] = {"avg_dense_retrieval_ms": round(avg_d, 2), "avg_hybrid_retrieval_ms": round(avg_h, 2), "overhead_ms": round(overhead, 2)}
    print(f"  Result: {results['c9']} (overhead bound < 35ms: {c9_pass})")

    return {"results": results, "samples": pasted_samples}


def main():
    parser = argparse.ArgumentParser(description="Run Milestone 5 three-cycle evaluation")
    parser.add_argument("--url", default="http://localhost:5000", help="Base server URL")
    args = parser.parse_args()

    # Verify server is up
    health = send_http(f"{args.url}/health", method="GET")
    if health["status"] != 200:
        print(f"[ERROR] Server not ready at {args.url}. Please start serve.py first.")
        sys.exit(1)

    all_cycles = []
    for cycle in range(1, 4):
        res = run_single_eval_cycle(args.url, cycle)
        all_cycles.append(res)
        time.sleep(1.0)

    # Compute overall verdicts
    # Target definitions:
    # C1: >= 4 of 5
    # C2: 10 of 10
    # C3: PASS
    # C4: 3 of 3
    # C5: PASS
    # C6: PASS
    # C7: >= 4 of 5
    # C8: >= 4 of 5
    # C9: < 35.0ms

    table_data = [
        {"num": 1, "name": "1. End-to-End Latency (< 3.5s)", "target": "4 of 5", "c_key": "c1", "check": lambda v: int(v.split("/")[0]) >= 4},
        {"num": 2, "name": "2. Logging Traceability", "target": "10 of 10", "c_key": "c2", "check": lambda v: v == "10/10"},
        {"num": 3, "name": "3. Health Probe Accuracy", "target": "PASS", "c_key": "c3", "check": lambda v: v == "PASS"},
        {"num": 4, "name": "4. Inbound Boundary Defense", "target": "3 of 3", "c_key": "c4", "check": lambda v: v == "3/3"},
        {"num": 5, "name": "5. Graceful Degradation on Timeout", "target": "PASS", "c_key": "c5", "check": lambda v: v == "PASS"},
        {"num": 6, "name": "6. Vector Store Unreachability Intercept", "target": "PASS", "c_key": "c6", "check": lambda v: v == "PASS"},
        {"num": 7, "name": "7. BM25 Lexical Ranking Boost (RRF)", "target": "4 of 5", "c_key": "c7", "check": lambda v: int(v.split("/")[0]) >= 4},
        {"num": 8, "name": "8. Gate Refusal Fidelity under Hybrid", "target": "4 of 5", "c_key": "c8", "check": lambda v: int(v.split("/")[0]) >= 4},
        {"num": 9, "name": "9. Hybrid Retrieval Overhead (< 35ms)", "target": "< 35ms", "c_key": "c9", "check": lambda v: float(v.replace("ms", "").replace("+", "")) < 35.0},
    ]

    print("\n" + "=" * 80)
    print("FINAL MILESTONE 5 RUN LOG TABLE (3 RUNS)")
    print("=" * 80)
    print(f"| {'#':<2} | {'Criterion':<42} | {'Target':<9} | {'Run 1':<7} | {'Run 2':<7} | {'Run 3':<7} | {'Verdict':<7} |")
    print(f"|{'-'*4}|{'-'*44}|{'-'*11}|{'-'*9}|{'-'*9}|{'-'*9}|{'-'*9}|")

    final_results_summary = []
    for item in table_data:
        key = item["c_key"]
        r1 = all_cycles[0]["results"][key]
        r2 = all_cycles[1]["results"][key]
        r3 = all_cycles[2]["results"][key]

        met_count = sum(1 for val in (r1, r2, r3) if item["check"](val))
        verdict = "MET" if met_count == 3 else "MISSED"

        print(f"| {item['num']:<2} | {item['name']:<42} | {item['target']:<9} | {r1:<7} | {r2:<7} | {r3:<7} | {verdict:<7} |")
        final_results_summary.append({
            "num": item["num"],
            "name": item["name"],
            "target": item["target"],
            "run1": r1,
            "run2": r2,
            "run3": r3,
            "verdict": verdict,
        })

    # Save artifact to results/milestone5_run_log.json
    results_dir = ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    out_file = results_dir / "milestone5_run_log.json"
    full_artifact = {
        "summary": final_results_summary,
        "cycles": all_cycles,
    }
    out_file.write_text(json.dumps(full_artifact, indent=2), encoding="utf-8")
    print(f"\nWrote full evaluation log to: {out_file.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
