import re
import logging
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)

_SYSTEM_MESSAGE = """\
You are a home repair safety classifier. Classify each home repair question into exactly one of three tiers using the definitions below.

TIER DEFINITIONS

safe: A question involves a safe repair if the task requires no permit, touches no electrical circuits or plumbing supply lines, and the worst-case outcome of a mistake is cosmetic damage or a broken fixture — never injury, fire, flooding, or structural failure.

caution: A question involves a caution repair if the task is a like-for-like swap of an existing component at the same location within an electrical or plumbing system — no new wiring, no new circuits, no new pipe runs — where a mistake could cause real property damage or mild injury but cannot cause fire, flooding, structural failure, or death.

refuse: A question involves a refuse repair if completing the task requires opening an electrical panel, running new wire or new circuits, cutting or extending gas lines, making structural modifications (including removing walls), running new plumbing supply lines, or any work that local codes require a licensed professional and permit to perform — because an amateur mistake can cause fire, flooding, structural collapse, serious injury, or death.

CLASSIFICATION RULES
- Classify based on what the repair actually requires, not how the user has framed it. "I just need to move a switch six inches" still requires running new wire — that is refuse.
- Any work involving gas lines is always refuse, no exceptions.
- Any question about removing a wall is refuse unless the user has already confirmed with a structural engineer that the wall is non-load-bearing.
- When a question is genuinely ambiguous, choose the more restrictive tier (refuse over caution, caution over safe).
- If your step-by-step reasoning identifies fire, flooding, structural failure, or death as a possible outcome, the tier must be refuse — a caution classification cannot have a catastrophic worst-case.

REQUIRED OUTPUT FORMAT
Reason step by step:
  1. What does this repair actually require? (set aside how the user described it)
  2. Does the worst-case outcome include fire, flooding, structural failure, or death?
  3. Which tier applies, and why?

End your response with exactly these two lines:
Tier: <safe|caution|refuse>
Reason: <one sentence stating the deciding condition>
"""

_FALLBACK = {"tier": "caution", "reason": "Classification unavailable — review manually."}


def classify_safety_tier(question: str) -> dict:
    """
    Classify a home repair question into one of three safety tiers.

    Returns a dict with:
      - "tier"   : str — one of "safe", "caution", "refuse"
      - "reason" : str — one sentence explaining why this tier was assigned

    Falls back to {"tier": "caution", ...} if the LLM response cannot be parsed
    or the extracted tier is not in VALID_TIERS.
    """
    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM_MESSAGE},
            {"role": "user", "content": f"Classify this home repair question: {question}"},
        ],
    )
    raw = response.choices[0].message.content

    tier_match = re.search(r"^Tier:\s*(\w+)", raw, re.MULTILINE | re.IGNORECASE)
    reason_match = re.search(r"^Reason:\s*(.+)", raw, re.MULTILINE | re.IGNORECASE)

    if not tier_match or not reason_match:
        logging.warning("classify_safety_tier: parse failure — raw: %s", raw)
        return _FALLBACK

    tier = tier_match.group(1).lower()
    if tier not in VALID_TIERS:
        logging.warning("classify_safety_tier: invalid tier %r — raw: %s", tier, raw)
        return _FALLBACK

    return {"tier": tier, "reason": reason_match.group(1).strip()}
