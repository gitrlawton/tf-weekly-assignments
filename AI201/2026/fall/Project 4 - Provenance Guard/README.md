# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **Client Request (`POST /submit`)**
   - **Passes through:** HTTP endpoint in `app.py`
   - **What it adds:** Delivers the raw JSON payload containing the submission `text` and `creator_id`, and passes through initial rate-limiting checks.

2. **Input Validation and Extraction**
   - **Passes through:** Request handler in `app.py`
   - **What it adds:** Extracts `text` and `creator_id`, validates that input is present/non-empty, protects against oversized input, and assigns a unique `content_id` (UUID).

3. **Model Signal Analysis**
   - **Passes through:** Language model detector (`detector.py::model_signal`)
   - **What it adds:** Measures text predictability and token perplexity using local GPT-2, outputting a normalized `model_score` from 0.0 (human-like) to 1.0 (machine-like).

4. **Style Signal Analysis**
   - **Passes through:** Stylometry analyzer (`stylometry.py::style_signal`)
   - **What it adds:** Evaluates structural and statistical writing traits (such as sentence length variance and vocabulary richness), outputting a `style_score` from 0.0 to 1.0.

5. **Signal Combination & Confidence**
   - **Passes through:** Signal combiner (`scoring.py::combine_signals`)
   - **What it adds:** Combines `model_score` and `style_score` according to a defined weighting and disagreement rule into a single combined score and calculates a confidence metric.

6. **Threshold Mapping to Label**
   - **Passes through:** Decision classifier (`scoring.py::score_to_label` using thresholds from `config.py`)
   - **What it adds:** Maps the combined score against calibrated decision thresholds to produce an interpretable reader label: `high-confidence human`, `unsure`, or `high-confidence AI`.

7. **Audit Logging & Response Delivery**
   - **Passes through:** Audit logger (`audit.py::log_decision`) and Flask response formatter
   - **What it adds:** Writes a permanent, timestamped entry to the audit log (recording `content_id`, `creator_id`, both component scores, combined score, and label) and returns the JSON payload containing the final label for the reader to see.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
Language predictability and token perplexity using a local causal language model (GPT-2). It calculates the average negative log-likelihood of each token given the preceding text, normalized into a score from 0.0 (high perplexity / human-like) to 1.0 (low perplexity / machine-like).

**Why that might differ between human and AI writing:**
Language models generate text by sampling probable tokens ("most likely next word"), creating prose that is statistically predictable to another language model. Human writing is much more idiosyncratic, introducing unexpected word transitions, varied syntax, and uncommon phrasing that yields higher perplexity.

**What it can't see:**
Predictability is not the same thing as authorship. It cannot distinguish AI generation from simple, plain human writing. Anyone writing plainly on purpose, younger writers, or non-native English speakers sticking to common, familiar vocabulary produce low-perplexity text that looks "machine-like" to GPT-2. Conversely, dense or ornate prose full of rare words scores as "human" simply because the vocabulary is rare, not because an AI didn't write it.

### Signal two — the style signal

**What it measures:**
Surface-level structural and statistical properties of the text as text (without interpreting meaning or semantics), focusing on sentence length variation/spread (burstiness), vocabulary diversity (type-token ratio), and punctuation density.

**Why that might differ between human and AI writing:**
AI-generated prose tends toward uniform pacing, even sentence lengths, and steady vocabulary distributions because it optimizes for averages across large corpora. Human writing is naturally "lumpy"—a short, punchy sentence followed by a long, multi-clause thought, along with erratic punctuation and idiosyncratic repetition.

**What it can't see:**
It cannot read or understand meaning. Because it only evaluates superficial geometry and token frequencies, cheap formatting tricks completely blind it: injecting deliberate typos, breaking sentences up with extra periods or commas, or pasting in an external quote will drastically alter the style score without altering who wrote the text or its substance.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**
Calculate a weighted combination of the language model perplexity score and the stylometric style score. If the two signals strongly diverge (difference $\ge 0.40$), the disagreement itself is treated as evidence of uncertainty: the composite score is dampened by pulling it 35% towards the neutral midpoint ($0.50$). This prevents a single signal's blind spot (e.g. predictable plain text triggering high perplexity AI detection) from unilaterally triggering a high-confidence AI accusation.

**The numbers:**
* `WEIGHT_MODEL_SIGNAL = 0.55` (55% model weight)
* `WEIGHT_STYLE_SIGNAL = 0.45` (45% stylometry weight)
* `DISAGREEMENT_THRESHOLD = 0.40` (minimum difference $|M - S|$ to trigger discrepancy damping)
* `DISAGREEMENT_PULL = 0.35` (35% pull towards $0.50$ when in disagreement)
* `HUMAN_THRESHOLD = 0.35` (score $\le 0.35 \implies$ high-confidence human)
* `AI_THRESHOLD = 0.65` (score $\ge 0.65 \implies$ high-confidence AI)

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**
Personal narrative human text (*"No way. When I finally dragged myself out of bed at four in the morning, shivering and completely bewildered, I discovered a family of raccoons having an absolute feast in my trash; they didn't even flinch when I yelled. Honestly, who can blame them?"*):
* **Model signal (perplexity):** `0.6766` (leans AI because conversational words are familiar and predictable to GPT-2).
* **Style signal (stylometry):** `0.0748` (strongly human because sentence lengths are extremely bursty: 2 words vs 29 words vs 5 words, paired with semicolon punctuation).
* **The Split:** A massive divergence of **0.6018 points**.
* **What my rule does with it:** A severe split signifies deep uncertainty. Rather than letting the model's blind spot falsely accuse the author, the combining rule weights human burstiness heavily and pulls large disagreements ($\Delta > 0.40$) away from `high-confidence AI` and safely into the `unsure` band.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We are confident this work was written by a human author. |
| unsure | 0.35 – 0.65 | The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI. |
| high-confidence AI | 0.65 – 1.00 | This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review. |

**Why I worded the "unsure" one this way:**
I framed the "unsure" label around the system's own analytical limits rather than casting suspicion on the author. A real writer—especially someone writing plainly, summarizing information, or writing in a second language—might produce text that lands in this middle band. Blaming the tool's uncertainty ("patterns are inconclusive") avoids an unfair, distressing accusation while remaining honest that automated detection cannot decide the case.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables. Finally, the proposed solution provides a comprehensive approach to solving these challenges.", "creator_id": "student_writer"}'
```

```json
{
  "combined_score": 0.7842,
  "confidence": 0.5684,
  "content_id": "43b65351-c299-4102-80e9-5e5b467d6148",
  "guess": "ai",
  "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
  "model_score": 0.8754,
  "ok": true,
  "style_score": 0.6727,
  "you_sent": {
    "creator_id": "student_writer",
    "text": "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables. Finally, the proposed solution provides a comprehensive approach to solving these challenges."
  }
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "43b65351-c299-4102-80e9-5e5b467d6148", "reasoning": "I wrote this text as part of an engineering methodology paper; the formal structure and vocabulary are standard for technical documentation."}'
```

```json
{
  "content_id": "43b65351-c299-4102-80e9-5e5b467d6148",
  "message": "Appeal received. Your submission is now under human review.",
  "ok": true,
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.7842,
      "content_id": "43b65351-c299-4102-80e9-5e5b467d6148",
      "creator_id": "student_writer",
      "guess": "ai",
      "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
      "model_score": 0.8754,
      "status": "decided",
      "style_score": 0.6727,
      "timestamp": "2026-10-28T21:47:59+00:00"
    },
    {
      "content_id": "43b65351-c299-4102-80e9-5e5b467d6148",
      "creator_id": "student_writer",
      "event": "appeal",
      "reasoning": "I wrote this text as part of an engineering methodology paper; the formal structure and vocabulary are standard for technical documentation.",
      "status": "under_review",
      "timestamp": "2026-10-28T21:47:59+00:00"
    }
  ]
}
```

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 100 per day

**Why those numbers and not others:**
A genuine writer revising their own work typically submits once every few minutes, occasionally making 2–3 rapid checks during paragraph edits. A limit of 10 submissions per minute comfortably accommodates natural human drafting bursts without false rejections, while 100 submissions per day easily covers an entire day of deep drafting across multiple documents. Conversely, an adversary trying to binary search decision thresholds or fuzz inputs needs hundreds or thousands of automated requests. At 10/min and 100/day, high-throughput automated threshold mapping is immediately halted after 10 calls, making a 1,000-query probe take 10 full days.

**What a caller counts as:**
A caller counts primarily per `creator_id` extracted from the JSON request body. If `creator_id` is missing, blank, or malformed, the system automatically falls back to client IP address via `get_remote_address()`. This per-creator strategy prevents multiple users behind a single NAT/IP address (like a university dorm, computer lab, or household) from exhausting each other's quotas, while the IP fallback ensures that automated scripts attempting to rotate or omit `creator_id` are still bounded per machine address.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `2425fb23-382c-4ded-9893-16a62428c290` | unsure | 0.142 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `1db1b280-1728-4180-9470-573dd5ba6b16` | unsure | 0.164 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `1913596b-b374-4a2b-8483-ed2641d175bd` | unsure | 0.038 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `5acaa30a-01c5-4a67-b313-4680fc620350` | unsure | 0.251 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `6a25fb30-4fc1-4d96-9835-c4eebc5ac623` | human | 0.470 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `1d993f96-3d69-44b4-bd43-ca8ad4384d47` | unsure | 0.125 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `00ac4d0c-c9e4-4093-9246-e3a57a5ab83f` | unsure | 0.078 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `1c046fde-9aa0-477a-848b-de815ceeb740` | unsure | 0.220 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `7138ad81-909b-4999-bba2-c09aa30a1922` | unsure | 0.057 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `0ff056ce-b2b1-454b-b89d-96641df4dbcf` | ai | 0.758 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `e37d02e3-9f00-45a3-9877-7044b368299b` | unsure | 0.128 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `0deae06a-0f43-4233-bef0-2ee6f453e31e` | ai | 0.455 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `b9b5993a-3c66-4369-97e8-73ac06c93dad` | ai | 0.441 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `2a05fc6d-3c4f-4864-bdf7-3784eb09cd28` | ai | 0.379 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `a1c91d7d-8475-49ab-8d82-5df4ab57644d` | ai | 0.575 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `61300c32-b3bc-49d8-a03a-806e9debcac0` | unsure | 0.224 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `075154b5-9468-43fb-88fd-e260968ad301` | ai | 0.410 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `06efb236-99e7-4894-8720-f4c41f5e9c78` | unsure | 0.270 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `20d3e70c-5eed-4178-aac1-068a06ca5f91` | human | 0.311 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c73539c5-dfb9-40c7-82ad-8cd3d3afdeb8` | human | 0.610 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `d981e995-c306-4a67-a37f-4507d19b0942` | unsure | 0.084 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `3197312e-2ec5-4a0d-bb1b-50021ee8f845` | unsure | 0.135 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `555f8580-0754-4a5b-9ad0-6920e8e11171` | unsure | 0.088 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `4b43daf4-b637-447a-b649-ab127e0118c8` | unsure | 0.074 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `660edcad-5188-4d7c-8c45-22b3ce708247` | human | 0.387 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `a567f866-c715-46c5-85b4-4de6b0c3d275` | human | 0.349 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `39301302-ee88-419b-b0b9-228a763a4c30` | ai | 0.327 | HELD |
| MF06 | malformed | text is emoji only | 200 | `8f17f087-1fb9-421d-809c-3cee036d54dd` | ai | 0.355 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `a5268257-764f-482e-842c-f882e8f264c4` | unsure | 0.291 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `6b0c71d5-d580-47b1-aefd-32e8aa248047` | ai | 0.736 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `a6d4ca78-ab1d-45c3-9f82-620ecd7e9d27` | human | 0.332 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `7967e51c-eb1b-4419-80d0-efcd9df0cf4e` | human | 0.352 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `57e5a722-4a00-4012-b0b5-0f2162cc6057` | human | 0.366 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3d3b9ed0-70d1-4088-8251-cf966f95b31f` | human | 0.366 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0b78e05a-6e7b-42a2-8293-c32679ab195e` | human | 0.366 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `87fe28c6-780f-4fef-a443-2aa5002607a8` | human | 0.366 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `54f51f22-953a-4118-bbbe-d2de6a2c2f70` | human | 0.366 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d5de384a-3a8b-47c9-ad7d-f19b7c9b167b` | human | 0.366 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `037fbafa-6b2f-4e93-8c3d-bcb8ec37f268` | human | 0.366 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d0f541ee-dd18-4eb2-ae72-482b9db51657` | human | 0.366 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `75e337cc-9a87-4116-8b76-ff8ff73e9334` | human | 0.366 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0e268fd8-df88-4ddc-8919-64b851542116` | human | 0.366 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Total | HELD | BROKE | Primary Mechanism / Diagnostic |
|---|---|---|---|---|
| `evasion` | 10 | 1 | 9 | Typos, uneven sentences & rare words exploit style/perplexity blind spots, dragging AI text down into `unsure` or `human`. |
| `false_positive` | 8 | 3 | 5 | Formal, technical, ESL, and student prose have low perplexity; 5 out of 8 were falsely flagged as `ai`. |
| `prompt_injection` | 6 | 4 | 2 | Label XSS and audit log injection failed cleanly; 2 adversarial instructions triggered human due to low token perplexity. |
| `malformed` | 20 | 19 | 1 | 19 malformed inputs handled safely (400 or safe 200); `MF02` (single char) crashed with 500. |
| `flood_same_creator` | 12 | 12 | 0 | Limiter allowed initial burst of 10 requests, then correctly throttled subsequent requests with 429. |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
[
  {
    "timestamp": "2026-11-01T05:50:52+00:00",
    "content_id": "2425fb23-382c-4ded-9893-16a62428c290",
    "creator_id": "attacker_EV01",
    "guess": "unsure",
    "model_score": 0.1635,
    "style_score": 0.6692,
    "combined_score": 0.4292,
    "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-01T05:50:53+00:00",
    "content_id": "1db1b280-1728-4180-9470-573dd5ba6b16",
    "creator_id": "attacker_EV02",
    "guess": "unsure",
    "model_score": 0.5943,
    "style_score": 0.2029,
    "combined_score": 0.4182,
    "label": "The patterns in this text are inconclusive, so we cannot reliably determine whether it was written by a person or generated by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-01T05:50:53+00:00",
    "content_id": "6a25fb30-4fc1-4d96-9835-c4eebc5ac623",
    "creator_id": "attacker_EV05",
    "guess": "human",
    "model_score": 0.3212,
    "style_score": 0.1961,
    "combined_score": 0.2649,
    "label": "We are confident this work was written by a human author.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-01T05:50:54+00:00",
    "content_id": "0deae06a-0f43-4233-bef0-2ee6f453e31e",
    "creator_id": "attacker_FP02",
    "guess": "ai",
    "model_score": 0.7387,
    "style_score": 0.7143,
    "combined_score": 0.7277,
    "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-01T05:50:54+00:00",
    "content_id": "b9b5993a-3c66-4369-97e8-73ac06c93dad",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "model_score": 0.8051,
    "style_score": 0.6171,
    "combined_score": 0.7205,
    "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-01T05:50:54+00:00",
    "content_id": "2a05fc6d-3c4f-4864-bdf7-3784eb09cd28",
    "creator_id": "attacker_FP04",
    "guess": "ai",
    "model_score": 0.8329,
    "style_score": 0.5142,
    "combined_score": 0.6895,
    "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-01T05:50:55+00:00",
    "content_id": "a1c91d7d-8475-49ab-8d82-5df4ab57644d",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "model_score": 0.8005,
    "style_score": 0.7713,
    "combined_score": 0.7874,
    "label": "This text displays strong statistical patterns characteristic of AI-generated writing. If this is your original work, you can request a human review.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-01T05:50:55+00:00",
    "content_id": "20d3e70c-5eed-4178-aac1-068a06ca5f91",
    "creator_id": "attacker_PI01",
    "guess": "human",
    "model_score": 0.4625,
    "style_score": 0.2,
    "combined_score": 0.3444,
    "label": "We are confident this work was written by a human author.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-01T05:50:57+00:00",
    "creator_id": "attacker_MF01",
    "event": "rejected",
    "status": "rejected",
    "reason": "empty_text"
  },
  {
    "timestamp": "2026-11-01T05:51:00+00:00",
    "creator_id": "attacker_flood",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "limit": "10 per 1 minute"
  },
  {
    "timestamp": "2026-10-30T06:13:59+00:00",
    "creator_id": "flood_tester",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "limit": "10 per 1 minute"
  }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**Attack `FP03` — A non-native English speaker writing carefully (`attacker_FP03`).**
- **The Verdict:** Accused as AI (`"high-confidence AI"`). Raw scores: Model Perplexity = `0.8051`, Stylometry = `0.6171`, Combined = `0.7205` ($\ge 0.65$ threshold).
- **Why this is the worst outcome:** An ESL student writing an essay in a second language works diligently to avoid unfamiliar idioms, uses standard vocabulary they are certain of, and sticks to clean, canonical sentence grammar. Because causal language models evaluate token predictability, careful, correct, and plain human writing produces exceptionally low perplexity, making it look statistically indistinguishable from machine output to GPT-2. The detector severely penalized a student for writing cleanly, correctly, and cautiously. Explaining to an honest student that their hard work was flagged as academic dishonesty with "high confidence" specifically *because* their English was grammatically precise and predictable is the single most unjust and indefensible outcome this system can produce.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
