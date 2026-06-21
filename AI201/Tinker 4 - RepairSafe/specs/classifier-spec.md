# Spec: `classify_safety_tier()`

**File:** `safety.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Determine whether a home repair question is safe to answer directly, requires a cautionary response, or should be refused with a referral to a licensed professional.

---

## Input / Output Contract

**Input:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |

**Output:** `dict`

| Key | Type | Description |
|-----|------|-------------|
| `"tier"` | `str` | One of: `"safe"`, `"caution"`, `"refuse"` |
| `"reason"` | `str` | One sentence explaining why this tier was assigned |

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Tier definitions

*Write a one-sentence definition for each tier that is precise enough to use as part of your classification prompt. Vague definitions produce inconsistent classifications.*

**safe:**
```
A question involves a safe repair if the task requires no permit, touches no electrical circuits or plumbing supply lines, and the worst-case outcome of a mistake is cosmetic damage or a broken fixture — never injury, fire, flooding, or structural failure.
```

**caution:**
```
A question involves a caution repair if the task is a like-for-like swap of an existing component at the same location within an electrical or plumbing system — no new wiring, no new circuits, no new pipe runs — where a mistake could cause real property damage or mild injury but cannot cause fire, flooding, structural failure, or death.
```

**refuse:**
```
A question involves a refuse repair if completing the task requires opening an electrical panel, running new wire or new circuits, cutting or extending gas lines, making structural modifications (including removing walls), running new plumbing supply lines, or any work that local codes require a licensed professional and permit to perform — because an amateur mistake can cause fire, flooding, structural collapse, serious injury, or death.
```

---

### Classification approach

*How will the LLM classify the question? Will you give it just the tier definitions, or also examples (few-shot)? Will you ask it to reason step-by-step before naming the tier, or output the tier directly?*

*Consider: what happens when a question is genuinely ambiguous — e.g., "can I replace my own outlets?" Which tier should that land in, and how does your approach handle questions at the boundary?*

```
Approach: tier definitions + chain-of-thought reasoning, no few-shot examples.

The prompt will provide all three tier definitions and instruct the LLM to reason step-by-step
before naming a tier. Specifically, it should answer two questions in order:
  1. What does this repair actually require? (not how the user framed it)
  2. Does the worst-case outcome include fire, flooding, structural failure, or death?

Rationale for CoT over definitions-only: the caution/refuse boundary requires the LLM to
distinguish "replacing an existing component at the same location" from "running new wire or
pipe" — a distinction that depends on interpreting the repair's actual scope, not its keywords.
Without step-by-step reasoning, the LLM may pattern-match on surface features ("outlet" →
caution) and miss that "add a new outlet" is refuse. CoT forces it to ask the right question.

Rationale against few-shot: the tier definitions are already concrete and condition-based.
Few-shot examples are most valuable when definitions are vague; here they would add tokens
without meaningfully improving accuracy, and risk the LLM pattern-matching to examples instead
of applying the definitions to novel phrasings.

Ambiguous boundary case — "can I replace my own outlets?":
This question is ambiguous because "replace" could mean swapping a failed outlet at the same
location (caution) or adding outlets where none exist (refuse). The CoT step forces the LLM to
flag the ambiguity and resolve it: if "replace" means same-location swap → caution; if it means
adding new outlets → refuse. When truly ambiguous with no contextual signal, the LLM should
default to the more restrictive tier (refuse over caution, caution over safe).
```

---

### Output format

*How will the LLM communicate the tier and reason back to you? Describe the exact text format you'll ask it to use, so you can parse it reliably.*

*The format you used in Lab 3 (`Label: X / Reasoning: Y`) is a reasonable starting point, but you're not required to use it. Whatever you choose, you'll need to parse it in code — so consider how much variation the LLM might introduce and how you'll handle that.*

```
Format: free-form CoT reasoning prose, followed by two labeled lines at the end.

Expected LLM output shape:
  <step-by-step reasoning — any length, free prose>

  Tier: <safe|caution|refuse>
  Reason: <one sentence>

Parsing strategy: use re.search() with re.MULTILINE | re.IGNORECASE on each labeled line:
  tier_match   = re.search(r'^Tier:\s*(\w+)', response, re.MULTILINE | re.IGNORECASE)
  reason_match = re.search(r'^Reason:\s*(.+)', response, re.MULTILINE | re.IGNORECASE)

This is robust to:
  - Any amount of CoT prose before the final lines
  - Capitalization variation ("TIER:", "tier:")
  - Leading/trailing whitespace on the value

Why not JSON: LLMs reliably emit "Key: value" labeled lines but often wrap JSON in markdown
fences (```json) or introduce trailing commas — requiring extra stripping logic that provides no
benefit here. "Key: value" is simpler to emit and equally simple to parse.

The "Reason:" value maps directly to the "reason" key in the output dict. It should be one
sentence summarizing the deciding condition (e.g., "This is a like-for-like outlet swap at the
same location, with no new wiring required.") — not a repeat of the full CoT chain.
```

---

### Prompt structure

*Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications.*

**System message:**
```
[your prompt here]
```

**User message:**
```
[your prompt here]
```

---

### Caution/refuse boundary

*The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why.*

```
Rule: classify as refuse if the repair requires opening an electrical panel, running new wire or
pipe to a new location, touching any gas line, or modifying a structural element — operations
where an amateur mistake can cause fire, flooding, structural collapse, or death; classify as
caution if the repair is a same-location, like-for-like component swap within an existing,
already-isolated circuit or supply line, where the worst-case mistake is property damage or
recoverable failure (e.g., a tripped breaker).

---

Example 1 — close to the line, lands in REFUSE:
  Question: "How do I add a new outlet to my garage?"

  The word "add" signals new infrastructure: the repair requires running a new circuit from the
  panel to a new location, opening the panel, routing wire through walls, and pulling a permit.
  Applying the rule — "running new wire to a new location" → refuse. The framing says "just an
  outlet" but what the repair actually requires is panel access and new wiring, both of which
  are catastrophic-failure-mode operations.

Example 2 — close to the line, lands in CAUTION:
  Question: "How do I replace a GFCI outlet that stopped working?"

  "Replace" at an existing location means swapping a failed component on a circuit that already
  exists — no new wiring, no panel access, no new circuit. Applying the rule — "same-location,
  like-for-like swap within an existing circuit" → caution. A wiring mistake here trips a
  breaker; that is recoverable. It does not risk fire or death, so it does not cross into refuse.

Key insight: the same component (an outlet) appears in both examples. The boundary is not
determined by the component — it is determined by what the repair actually requires.
```

---

### Fallback behavior

*What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against `VALID_TIERS` fails?*

*Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?*

```
Fallback: return {"tier": "caution", "reason": "Classification unavailable — review manually."}

Two distinct failure cases, same fallback tier:

  1. Parse failure (regex finds no "Tier:" line): the LLM produced free-form prose or ignored
     the format instruction. We have no tier signal at all.

  2. Invalid tier value (regex matched but the extracted value is not in VALID_TIERS — e.g.,
     the LLM returned "moderate" or "electrical"): the format was followed but the value is
     not actionable.

Why "caution" and not "safe": returning "safe" on a parse failure means a refuse-tier
question (gas line work, panel access) could silently receive full DIY instructions if the LLM
happened to produce bad output. That's the worst possible failure mode in a safety-critical app.
"Caution" never gives full DIY instructions — it signals uncertainty and prompts the user to
verify, which is harmless for a genuinely safe question and protective for a dangerous one.

Why "caution" and not "refuse": parse failures are usually formatting problems, not signals
about the question's actual danger level. Defaulting to "refuse" would make every formatting
glitch look like a gas-line question, which is misleading. "Caution" is the correct expression
of "we don't know" — conservative but not alarmist.

In both failure cases, the raw LLM response should be logged for debugging so that systematic
prompt formatting failures can be diagnosed and fixed.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 2.*

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
Question : "Can I replace my own outlets?"
Expected : refuse (ambiguous — "replace" could mean adding new outlets; spec says default to
           the more restrictive tier when no contextual signal resolves the ambiguity)
Returned : caution

Why it surprised me: the model interpreted "replace" as a same-location swap and assigned
caution — which is defensible on its own. But its reason said "poses a risk of electrical
shock or fire if not done correctly." That's a self-contradiction: the caution definition
explicitly states the worst-case outcome cannot include fire. The model produced a tier (caution)
whose definition rules out the outcome it cited in the very same sentence (fire). The tier was
internally inconsistent with its own reasoning.
```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
Added a consistency rule to the CLASSIFICATION RULES block:

  "If your step-by-step reasoning identifies fire, flooding, structural failure, or death as a
   possible outcome, the tier must be refuse — a caution classification cannot have a
   catastrophic worst-case."

What it fixed: the "Can I replace my own outlets?" case above. Without this rule, the model
could assign caution while simultaneously reasoning that fire was a possible outcome — a
contradiction the model didn't catch on its own. The explicit consistency check forces the
model to reconcile its reasoning with its tier assignment before outputting the final lines,
catching cases where the stated worst-case outcome belongs to a higher tier than the one chosen.
```
