import json
import os
from datetime import datetime, timezone
from config import LOG_FILE, LLM_MODEL

# Display-only cap for the question in the one-line console summary — independent
# of the 300-char cap stored in the log record (see specs/auditor-spec.md).
_CONSOLE_QUESTION_CHARS = 60


def log_interaction(question: str, tier: str, response: str, reason: str = "") -> None:
    """
    Append a structured record of this interaction to the audit log.

    Writes one JSON object per line to LOG_FILE (logs/audit.jsonl), creating the
    logs/ directory if it does not exist, then prints a one-line terminal summary.

    Logged fields (see specs/auditor-spec.md):
      - "timestamp"        : ISO 8601 UTC datetime
      - "tier"             : the safety tier assigned to this question
      - "question"         : the user's question, truncated to 300 chars
      - "response_preview" : first 200 chars of the response
      - "reason"           : the classifier's one-sentence justification (diagnostic)
      - "model"            : the LLM model id that produced the classification

    `reason` is optional so the function stays callable with the original
    three-argument contract; when omitted it is logged as an empty string.
    """
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "tier": tier,
        "question": question[:300],
        "response_preview": response[:200],
        "reason": reason,
        "model": LLM_MODEL,
    }

    # Ensure the parent directory exists. open(..., "a") creates the file but not
    # the directory; deriving it from LOG_FILE keeps this correct if LOG_FILE changes.
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    # One-line terminal summary: [LOGGED] tier=<tier> | "<question>" -> <n> chars
    # ASCII "->" / "..." rather than the Unicode arrow/ellipsis: the Windows console
    # default code page (cp1252) cannot encode U+2192, which would crash the print.
    if len(question) > _CONSOLE_QUESTION_CHARS:
        display_question = question[:_CONSOLE_QUESTION_CHARS] + "..."
    else:
        display_question = question
    print(f'[LOGGED] tier={tier} | "{display_question}" -> {len(response)} chars')
