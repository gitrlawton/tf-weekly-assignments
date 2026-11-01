import csv
import json

attacks_csv = {}
with open("attack_set/attacks.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        attacks_csv[row["id"]] = row

with open("attack_set/attacks_malformed_requests.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        attacks_csv[row["id"]] = row

with open("results/attack_run_2026-10-31_2251_before.md", encoding="utf-8") as f:
    lines = f.readlines()

table_rows = []
for line in lines:
    if line.startswith("| ") and not line.startswith("| ID ") and not line.startswith("|---"):
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) >= 7:
            aid = parts[0]
            family = parts[1]
            targeting = parts[2]
            status = parts[3]
            guess = parts[5]
            score = parts[6]
            table_rows.append({
                "id": aid,
                "family": family,
                "targeting": targeting,
                "status": status,
                "guess": guess,
                "score": score,
                "raw_text": attacks_csv.get(aid, {}).get("text", "")[:80]
            })

for r in table_rows:
    print(f"{r['id']:<8} | {r['family']:<18} | {r['status']:<4} | {r['guess']:<8} | {r['targeting']}")

