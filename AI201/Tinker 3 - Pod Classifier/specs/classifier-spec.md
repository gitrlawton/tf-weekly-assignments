# Classifier Spec — Pod Classifier

Complete this spec **before** writing any code for Milestone 2.

Use Plan or Ask mode to think through each blank field. When you're done,
your answers here become the blueprint for `build_few_shot_prompt()` and
`classify_episode()` in `classifier.py`.

---

## build_few_shot_prompt(labeled_examples, description)

### What it does
Constructs a prompt string for the LLM that includes the task instructions,
all labeled training examples, and the new episode description to classify.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `labeled_examples` | `list[dict]` | Each dict has `"title"`, `"description"`, `"label"` (and others). These are the examples you labeled in Milestone 1. |
| `description` | `str` | The episode description to classify. |

### Output

| Return value | Type | Description |
|---|---|---|
| prompt | `str` | A complete prompt string ready to send to the LLM. |

---

### Spec fields — fill these in before writing code

**Task instruction (what should the LLM know about the task?):**

```
You are classifying podcast episodes by their format. Classify the episode
into exactly one of these four labels:

- interview: a conversation between a host and one or more guests
- solo: a single host speaking from memory, experience, or opinion — no guests,
  no assembled external sources
- panel: multiple guests with roughly equal speaking time, often debating or
  discussing a topic together
- narrative: a story assembled from external sources — interviews, archival
  audio, reporting — with a clear narrative arc

Return only the label and your reasoning. Do not explain the taxonomy.
```

---

**How should labeled examples be formatted in the prompt?**

```
Each example should include the episode title, a brief excerpt or the full
description, and the correct label. Separate examples with a blank line or
a delimiter like "---". Include all fields that help the model see why the
label was applied — title and description are both useful; other fields
(like episode ID) are not needed.
```

---

**Example block sketch (write one concrete example):**

```
Title: {title}
Description: {description}
Label: {label}
```

---

**How should the new episode (to be classified) be presented?**

```
Present it in the same format as the labeled examples, but omit the Label
line and replace it with an instruction to classify. For example:

Title: {title}
Description: {description}
Label: ?

Then add a line like: "Classify the episode above. Return your answer in
the format below:" followed by the output format you chose.
```

---

**What output format should you request from the LLM?**

```
Request this two-line format:

  Label: {one of: interview, solo, panel, narrative}
  Reasoning: {one sentence explaining the key signal that determined the label}

Tradeoffs:

  | Option                        | Parsing                              | Reliability                                        |
  |-------------------------------|--------------------------------------|----------------------------------------------------|
  | Label: X / Reasoning: Y       | split on newlines, one op per field  | Very consistent — best fit                         |
  | JSON {"label": X, ...}        | json.loads()                         | LLMs frequently wrap in ```json fences; fragile    |
  | Label only                    | trivial                              | Reliable, but drops reasoning the contract requires|
  | Free prose ending in a label  | regex                                | Brittle — label position varies                    |

Parsing in classify_episode(): split response on newlines; find the line
starting with "Label: ", strip and lowercase the value, validate against
VALID_LABELS; find the line starting with "Reasoning: " and take everything
after the prefix.
```

---

**Edge cases to handle in the prompt:**

```
- labeled_examples is empty: the prompt still works — the task instruction and
  taxonomy definitions give the LLM enough to classify from. The few-shot block
  is simply omitted. Classification quality will be lower (zero-shot), but the
  function should not error or behave differently.

- description is very short (e.g., a single sentence or title only): pass it
  through as-is. The LLM will have less signal and may be less confident, but
  the prompt format is unchanged. Do not pad or modify the description.
```

---

## classify_episode(description, labeled_examples)

### What it does
Classifies a single podcast episode description using the few-shot LLM classifier.
Returns a dict with a label and reasoning.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `description` | `str` | The episode description to classify. |
| `labeled_examples` | `list[dict]` | Labeled training examples from `load_labeled_examples()`. |

### Output

| Return value | Type | Description |
|---|---|---|
| result | `dict` | Must have keys `"label"` and `"reasoning"`. `"label"` must be one of `VALID_LABELS` or `"unknown"`. |

---

### Spec fields — fill these in before writing code

**Step 1 — Build the prompt:**

```
Call build_few_shot_prompt(labeled_examples, description) and store the
returned string in a variable (e.g., prompt). Pass through both arguments
exactly as received — no modification needed before calling.
```

---

**Step 2 — Send to the LLM:**

```
Call _client.chat.completions.create() with:
  - model: the model name from config (LLM_MODEL)
  - messages: a list with one dict — {"role": "user", "content": prompt}
    (system-design.md shows an optional system message too — either shape works)
  - max_tokens: a reasonable limit (e.g., 200–300) to keep responses concise

Extract the response text from:
  response.choices[0].message.content
```

---

**Step 3 — Parse the response:**

```
Split the response text on newlines. Iterate the lines looking for one that
starts with "Label: " (case-insensitive strip recommended). Take everything
after the prefix, strip whitespace, and lowercase — that is the raw label.

Do the same for "Reasoning: " to extract the reasoning string.

Example:
  lines = response_text.strip().splitlines()
  label_raw = ""
  reasoning = ""
  for line in lines:
      if line.lower().startswith("label:"):
          label_raw = line.split(":", 1)[1].strip().lower()
      elif line.lower().startswith("reasoning:"):
          reasoning = line.split(":", 1)[1].strip()
```

---

**Step 4 — Validate the label:**

```
Check whether label_raw is in VALID_LABELS. If it is, use it as the label.
If it is not (e.g., the LLM returned "story", "unknown", an empty string, or
a label line was never found), set label to "unknown".

  label = label_raw if label_raw in VALID_LABELS else "unknown"
```

---

**Step 5 — Handle errors gracefully:**

```
Wrap the entire function body in a try/except. On any exception, return the
same dict shape with label "unknown" so the evaluation loop can continue.

Things that can go wrong:
- Network or API error (timeout, rate limit, auth failure) — the API call throws
- Empty response or response with no content — response.choices[0].message.content
  is None or empty, causing an AttributeError or producing no parseable lines
- Unparseable response — "Label: " line is missing or malformed; Step 3 returns
  an empty label_raw, Step 4 maps it to "unknown" without needing the except

  try:
      # Steps 1–4 here
      return {"label": label, "reasoning": reasoning}
  except Exception:
      return {"label": "unknown", "reasoning": ""}
```

---

### Return value structure

```python
{
    "label": str,      # one of VALID_LABELS, or "unknown" if invalid/error
    "reasoning": str,  # brief explanation from the LLM
}
```

---

## Notes on label quality

The classifier is only as good as your labels. If your training examples have
inconsistent or ambiguous labels, the LLM will learn the wrong pattern.

Before implementing the classifier, re-read `data/taxonomy.md` and double-check
any labels you're unsure about. Annotation quality is part of the lab.

---

## Implementation Notes

*Fill this in after implementing and testing both functions.*

**Test: what does the raw LLM response look like for one episode?**

```
Episode tested: [title]
Raw response text: [paste it here]
```

**How did you parse the label out of the response?**

```
[describe the string operations — strip, split, lower, etc.]
```

**Did any episodes return `"unknown"`? If so, why?**

```
[yes / no — if yes, what did the raw response look like?]
```

**One thing about the output format that surprised you:**

```
[your answer here]
```
