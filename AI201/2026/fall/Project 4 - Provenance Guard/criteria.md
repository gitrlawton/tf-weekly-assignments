# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False Positives

<!-- Your criterion. It must name a number. -->
Of 10 pieces I wrote myself, at most 1 is labelled `high-confidence AI` (a false-positive rate $\le 10\%$) across all three test trials.

**Why this target:**
I allow at most 1 false positive in 10 because on a writing site a wrong accusation costs more than a missed detection. An author wrongly accused of cheating suffers immediate reputational harm, so the bar to accuse must stay high even if some AI text slips through.

---

## 2. Score Spread

<!-- Your criterion. -->
The average combined score of 5 clearly-AI text samples is at least 0.35 points higher than the average combined score of 5 clearly-human text samples (on the 0.0 to 1.0 scale).

**Why this target:**
I chose a 0.35 spread because anything tighter means the classifier is making decisions on noise rather than distinct patterns. A separation of at least 0.35 ensures human and AI populations are clearly differentiated and leaves ample room for a viable `unsure` middle band.

---

## 3. Label Coverage & Borderline Handling

<!-- Your criterion. -->
Text I judge borderline scores between 0.40 and 0.60 and receives the label `unsure` in at least 4 of 5 cases, and across 10 varied test inputs, every one of the 3 labels (`high-confidence human`, `unsure`, `high-confidence AI`) is assigned to at least 2 inputs.

**Why this target:**
I target 4 of 5 borderline pieces landing between 0.40 and 0.60 because forcing ambiguous text into binary labels guarantees false accusations. Requiring each label to appear at least twice proves that all three labels are actually reachable in real service operation.

---

## 4. The Appeal Path

<!-- Your criterion. -->
Across 5 test submissions, 5 out of 5 valid requests to `POST /appeal` with an existing `content_id` change the audit log record status from `decided` to `under_review` and return HTTP status 200.

**Why this target:**
I require a 5 of 5 (100%) success rate because an appeal is the writer's only defense against an incorrect label. If even 1 appeal fails to transition status or get recorded in the log, an author has been silenced with no recourse.

---

## 5. Bad Input Handling

<!-- Your criterion. -->
4 out of 4 malformed requests (missing `text` field, empty `text: ""`, `text: null`, and text exceeding 50,000 words) return an HTTP 400 or HTTP 413 status code with 0 unhandled HTTP 500 server crashes.

**Why this target:**
I require all 4 bad inputs to return 4xx client errors without crashing because unhandled 500 errors can mask service outages and create denial-of-service vulnerabilities. A resilient backend must reject bad data cleanly and keep running.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
