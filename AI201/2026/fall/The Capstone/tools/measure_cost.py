#!/usr/bin/env python3
"""
Cost & Performance Measurement Tool for The Unofficial Guide.

Runs 10 distinct, authentic non-cached queries through the pipeline, measuring:
  • Granular stage latencies (retrieval, gate, generation, end-to-end)
  • Exact token consumption per run (prompt tokens, output tokens)
  • Measured API financial cost per run based on Google Gemini pricing
  • Daily operational projections (100 queries/day)

Usage:
    python tools/measure_cost.py
    python tools/measure_cost.py --url http://localhost:5000
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

import config

# Pricing per million tokens for Gemini Flash / Flash-Lite:
# Input: $0.075 / 1M tokens ($0.000000075 / token)
# Output: $0.30 / 1M tokens ($0.00000030 / token)
COST_PER_INPUT_TOKEN = 0.075 / 1_000_000.0
COST_PER_OUTPUT_TOKEN = 0.30 / 1_000_000.0

TEN_DISTINCT_QUESTIONS = [
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


def run_via_library():
    """Run directly using app.ask_pipeline with cache=False."""
    from app import ask_pipeline

    records = []
    print("\nRunning 10 non-cached queries directly via Python pipeline...")
    print("=" * 75)

    for i, q in enumerate(TEN_DISTINCT_QUESTIONS, 1):
        t0 = time.perf_counter()
        outcome = ask_pipeline(q, corpus=config.CORPUS, cache=False, hybrid=False)
        total_ms = (time.perf_counter() - t0) * 1000.0

        timing = outcome.get("timing", {})
        tokens = outcome.get("tokens", {})
        p_tokens = tokens.get("prompt", 0)
        o_tokens = tokens.get("output", 0)
        tot_tokens = tokens.get("total", p_tokens + o_tokens)

        cost = (p_tokens * COST_PER_INPUT_TOKEN) + (o_tokens * COST_PER_OUTPUT_TOKEN)

        record = {
            "run": i,
            "question": q,
            "refused": outcome.get("refused", False),
            "sources": outcome.get("sources", []),
            "retrieval_ms": timing.get("retrieval_ms", 0.0),
            "gate_ms": timing.get("gate_ms", 0.0),
            "generation_ms": timing.get("generation_ms", 0.0),
            "total_latency_ms": round(total_ms, 2),
            "prompt_tokens": p_tokens,
            "output_tokens": o_tokens,
            "total_tokens": tot_tokens,
            "cost_usd": cost,
            "answer_preview": (outcome.get("answer") or "")[:60].replace("\n", " "),
        }
        records.append(record)
        print(
            f"Run {i:2d}: {q[:38]:<40} | Latency: {total_ms:6.1f}ms | "
            f"Tokens: {tot_tokens:4d} ({p_tokens:4d} in, {o_tokens:2d} out) | "
            f"Cost: ${cost:.6f}"
        )

    return records


def run_via_http(base_url: str):
    """Run via HTTP POST /ask with cache: False."""
    base_url = base_url.rstrip("/")
    records = []
    print(f"\nRunning 10 non-cached queries via HTTP against {base_url}...")
    print("=" * 75)

    for i, q in enumerate(TEN_DISTINCT_QUESTIONS, 1):
        payload = json.dumps({"question": q, "cache": False, "hybrid": False}).encode("utf-8")
        req = urllib.request.Request(
            f"{base_url}/ask",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        t0 = time.perf_counter()
        with urllib.request.urlopen(req, timeout=30) as resp:
            total_ms = (time.perf_counter() - t0) * 1000.0
            data = json.loads(resp.read().decode("utf-8"))

        timing = data.get("timing_ms", {})
        tokens = data.get("tokens", {})
        p_tokens = tokens.get("prompt", 0)
        o_tokens = tokens.get("output", 0)
        tot_tokens = tokens.get("total", p_tokens + o_tokens)

        cost = (p_tokens * COST_PER_INPUT_TOKEN) + (o_tokens * COST_PER_OUTPUT_TOKEN)

        record = {
            "run": i,
            "question": q,
            "refused": data.get("refused", False),
            "sources": data.get("sources", []),
            "retrieval_ms": timing.get("retrieval", 0.0),
            "gate_ms": timing.get("gate", 0.0),
            "generation_ms": timing.get("generation", 0.0),
            "total_latency_ms": round(total_ms, 2),
            "prompt_tokens": p_tokens,
            "output_tokens": o_tokens,
            "total_tokens": tot_tokens,
            "cost_usd": cost,
            "answer_preview": (data.get("answer") or "")[:60].replace("\n", " "),
        }
        records.append(record)
        print(
            f"Run {i:2d}: {q[:38]:<40} | Latency: {total_ms:6.1f}ms | "
            f"Tokens: {tot_tokens:4d} ({p_tokens:4d} in, {o_tokens:2d} out) | "
            f"Cost: ${cost:.6f}"
        )

    return records


def summarize_and_print(records: list[dict]):
    n = len(records)
    avg_latency = sum(r["total_latency_ms"] for r in records) / n
    avg_retrieval = sum(r["retrieval_ms"] for r in records) / n
    avg_generation = sum(r["generation_ms"] for r in records) / n
    avg_prompt_tokens = sum(r["prompt_tokens"] for r in records) / n
    avg_output_tokens = sum(r["output_tokens"] for r in records) / n
    avg_total_tokens = sum(r["total_tokens"] for r in records) / n
    avg_cost = sum(r["cost_usd"] for r in records) / n

    daily_cost_100 = avg_cost * 100.0
    daily_tokens_100 = avg_total_tokens * 100.0
    monthly_cost_3000 = daily_cost_100 * 30.0

    print("\n" + "=" * 75)
    print("COST & PERFORMANCE MEASUREMENT SUMMARY (10 RUNS)")
    print("=" * 75)
    print(f"Number of Measured Runs:       {n}")
    print(f"Average Total Latency:         {avg_latency:6.2f} ms")
    print(f"Average Retrieval Time:        {avg_retrieval:6.2f} ms")
    print(f"Average Generation Time:       {avg_generation:6.2f} ms")
    print(f"Average Prompt Tokens:         {avg_prompt_tokens:6.1f} tokens")
    print(f"Average Output Tokens:         {avg_output_tokens:6.1f} tokens")
    print(f"Average Total Tokens:          {avg_total_tokens:6.1f} tokens")
    print(f"Measured Cost per Run:         ${avg_cost:.6f} USD")
    print("-" * 75)
    print("100 Queries / Day Arithmetic:")
    print(f"  • Daily Token Volume:        {daily_tokens_100:,.0f} tokens/day")
    print(f"  • Daily API Cost:            ${daily_cost_100:.4f} USD/day")
    print(f"  • 30-Day Monthly Projection: ${monthly_cost_3000:.4f} USD/month")
    print("=" * 75)

    return {
        "avg_latency": avg_latency,
        "avg_retrieval": avg_retrieval,
        "avg_generation": avg_generation,
        "avg_prompt_tokens": avg_prompt_tokens,
        "avg_output_tokens": avg_output_tokens,
        "avg_total_tokens": avg_total_tokens,
        "avg_cost": avg_cost,
        "daily_cost_100": daily_cost_100,
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser(description="Measure cost and token usage across 10 runs")
    parser.add_argument("--url", help="Base URL of running server (e.g. http://localhost:5000)")
    args = parser.parse_args()

    if args.url:
        records = run_via_http(args.url)
    else:
        records = run_via_library()

    summary = summarize_and_print(records)

    # Save measurement JSON artifact to results/cost_measurement.json
    results_dir = ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    out_file = results_dir / "cost_measurement.json"
    out_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nWrote detailed measurement record to: {out_file.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
