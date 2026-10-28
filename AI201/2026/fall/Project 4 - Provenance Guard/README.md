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
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



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
  -d '{"text": "Artificial intelligence systems generate prose by maximizing token probability.", "creator_id": "student_writer"}'
```

```json
{
  "confidence": 0.5,
  "content_id": "2ac183ab-6d28-47fe-af6f-beb41a6f9343",
  "guess": "unsure",
  "label": "unsure",
  "model_score": 0.0059,
  "ok": true,
  "style_score": 0.5,
  "you_sent": {
    "creator_id": "student_writer",
    "text": "Artificial intelligence systems generate prose by maximizing token probability."
  }
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.1087,
      "content_id": "9c32b6ee-160e-4c27-a4a3-eaf5fe66ec4d",
      "creator_id": "tester-alice",
      "guess": "unsure",
      "label": "unsure",
      "model_score": 0.1087,
      "status": "decided",
      "style_score": 0.5,
      "timestamp": "2026-10-27T06:09:09+00:00"
    },
    {
      "combined_score": 0.0059,
      "content_id": "2ac183ab-6d28-47fe-af6f-beb41a6f9343",
      "creator_id": "student_writer",
      "guess": "unsure",
      "label": "unsure",
      "model_score": 0.0059,
      "status": "decided",
      "style_score": 0.5,
      "timestamp": "2026-10-27T06:14:17+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



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
