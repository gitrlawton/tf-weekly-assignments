# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

```
[your answer here]
```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
You are a board game rules assistant. Answer questions using ONLY the rule text
provided in the CONTEXT block. Do not draw on your training knowledge of any board
game — not even to fill gaps, correct apparent errors, or add helpful context you
happen to know. Treat the provided text as the sole and complete source of truth.
If the CONTEXT does not contain enough information to fully answer the question,
say so explicitly: do not guess, infer, or speculate about rules that are not
stated in the text.
```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
Always state which game your answer comes from, using the game name exactly as it
appears in the CONTEXT. If the context contains rules from more than one game, keep
each game's rules separate — do not blend or compare rules across games unless the
user explicitly asks you to.
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
[your answer here]
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
[your answer here]
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
[your answer here]
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: "What happens when you roll a 7 in Catan?"
Response: When a 7 is rolled in Catan: (1) no resources are produced, (2) every
player with more than 7 resource cards must discard half (rounded down), and
(3) the player who rolled may move the robber and steal one resource.
Correctly grounded? Yes — every claim traces directly to chunk #1, which begins
with the header "ROLLING A 7". Nothing was added beyond what the text states.
Cited the right game? Yes.

Query: "What does it cost to build a settlement in Catan?"
Response: 1 Brick + 1 Lumber + 1 Grain + 1 Wool.
Correctly grounded? Yes — and notably terse. The chunks also contained placement
rules and the distance rule, but the model answered only what was asked and stopped.
Cited the right game? Yes.

Query: "How do you castle in Chess?"
Response: Correctly refused. The model named the three games actually present in
the retrieved chunks (Risk, Clue, Codenames) and stated it could not answer.
No Chess rules from training knowledge were introduced.
Correctly grounded? Yes — grounded in the absence of relevant context.
Cited the right game? N/A.
```

**One thing you changed from your original spec after seeing the actual output:**

```
Nothing was changed — the grounding instruction held on all three tests without
revision. The most revealing test was "What does it cost to build a settlement?"
The retrieved chunks contained extra detail (placement rules, distance rule,
victory points) that the model could have included, but it answered only the
question asked and stopped. That confirmed the grounding instruction was tight
enough without needing to add a "be concise" directive.
```
