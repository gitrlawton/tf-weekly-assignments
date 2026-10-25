"""
Structured JSON Logger for The Unofficial Guide.

Emits structured single-line JSON logs to:
1. logs/requests.jsonl (persistent file)
2. sys.stdout (console stream for Docker / process managers)
"""

import datetime as dt
import json
import logging
from pathlib import Path
import sys

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "requests.jsonl"

_logger = logging.getLogger("capstone.structured")
_logger.setLevel(logging.INFO)
_logger.propagate = False

if not _logger.handlers:
    # 1. File handler writing JSON lines
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(file_handler)

    # 2. Console stream handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("[JSON LOG] %(message)s"))
    _logger.addHandler(console_handler)


def log_request(record: dict) -> None:
    """Write a structured record as a single JSON line.

    Guaranteed never to raise an exception: observability should never
    fail the operation it is observing.
    """
    try:
        if "timestamp" not in record:
            record["timestamp"] = (
                dt.datetime.now(dt.timezone.utc).isoformat()
            )
        line = json.dumps(record, ensure_ascii=False)
        _logger.info(line)
        for h in _logger.handlers:
            h.flush()
    except Exception as exc:  # noqa: BLE001
        print(f"[logger fallback error] Failed to serialize log: {exc}", file=sys.stderr)


def read_recent_logs(n: int = 10) -> list[dict]:
    """Read the last n JSON records from logs/requests.jsonl."""
    if not LOG_FILE.exists():
        return []
    records = []
    try:
        lines = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
        for line in reversed(lines):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
            if len(records) >= n:
                break
        records.reverse()
    except Exception as exc:  # noqa: BLE001
        print(f"[logger error] Failed to read log file: {exc}", file=sys.stderr)
    return records
