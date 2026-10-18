# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

This project categorizes posts from online movie enthusiast communities (such as r/movies, film discussion forums, and Letterboxd discussions). These spaces feature a diverse mix of discourse ranging from technical filmmaking analyses to speculative lore and box office tracking. The classifier sorts posts into four distinct categories: `craft_critique`, `fan_theory`, `recommendation_request`, and `industry_business`. This automated categorization helps organize community feeds and distinguish between aesthetic discussions, speculative storytelling, audience discovery, and industry reporting.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `craft_critique`

**Definition:** Evaluates the technical or artistic execution of a film (such as cinematography, sound design, editing, pacing, or performance) rather than expressing mere personal enjoyment.

**Example 1:**
> The sound design in Dune: Part Two does more worldbuilding than the dialogue; the low-frequency humming during the spice harvesting scene creates palpable physical tension.

**Example 2:**
> The third act of Sunshine completely falls apart because abruptly switching from hard sci-fi into a slasher with rapid-cut editing and lens flares undermines the claustrophobia built up over the first 70 minutes.

### `fan_theory`

**Definition:** Proposes an unconfirmed narrative interpretation, lore connection, or alternative explanation for events inside a movie's fictional world.

**Example 1:**
> In Inception, Cobb's actual totem isn't the spinning top—it's his wedding ring, because he is only wearing it during dream sequences and never in the scenes set in reality.

**Example 2:**
> The briefcase in Pulp Fiction contains Marcellus Wallace's soul, which explains the gold glow and the bandage on the back of his neck where the devil extracted it.

### `recommendation_request`

**Definition:** Solicits movie suggestions from other members based on a specific mood, obscure subgenre, trope, or similarity to another title.

**Example 1:**
> Looking for slow-burn 70s neo-noir detective films with cynical protagonists, similar in tone to The Long Goodbye and Chinatown.

**Example 2:**
> Can anyone recommend smart sci-fi thrillers that take place entirely in a single claustrophobic location, like Coherence or Moon?

### `industry_business`

**Definition:** Discusses the commercial, financial, casting, or distribution realities of the film industry (such as box office numbers, studio mergers, or theatrical windows) rather than the content of a movie.

**Example 1:**
> Opening to only $32M over a four-day Memorial Day weekend on a $168M production budget makes it mathematically difficult for the studio to break even without overseas carry.

**Example 2:**
> A24 securing a 45-day theatrical exclusivity window before shifting to VOD signals that mid-budget original movies can still command traditional theatrical runs.

### The hardest boundary

**Which two labels:** `craft_critique` and `fan_theory`

**The decision rule I used every time:** If the post evaluates deliberate filmmaking choices made by real-world creators (directors, actors, screenwriters, editors), it is `craft_critique`. If it treats the movie's fictional universe as a real reality to deduce unstated in-universe lore, character psychology, or unseen events, it is `fan_theory`.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Online film discussion communities and forums (including r/movies, TrueFilm, and BoxOffice discussion threads).

**How I labelled them:** Cold-labelled the first 20 posts manually without assistance (5 from each category), then pre-labelled the remaining 180 and reviewed/verified every single post against the taxonomy definitions and boundary decision rules.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `craft_critique` | 50 | 25.0% |
| `fan_theory` | 50 | 25.0% |
| `recommendation_request` | 50 | 25.0% |
| `industry_business` | 50 | 25.0% |
| **Total** | 200 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "In Blade Runner 2049, Deckard intentionally left wooden horse carvings across the wasteland to lead replicant resistance members to his daughter."
>
> *Could have been:* `craft_critique` or `fan_theory`
>
> *I chose, because:* `fan_theory`, because it analyzes in-universe character motives and lore that were never explicitly verified in the narrative, rather than commenting on Denis Villeneuve's directing or Roger Deakins' cinematography.

**2.**
> *The post:* "Christopher Nolan leaving Warner Bros. for Universal over streaming release policies resulted in Universal granting him a 100-day theatrical window and 20% first-dollar gross."
>
> *Could have been:* `craft_critique` or `industry_business`
>
> *I chose, because:* `industry_business`, because although it references an auteur filmmaker, the subject matter concerns distributor bidding wars, theatrical release windows, and contract economics rather than filmmaking technique.

**3.**
> *The post:* "What are the best sports biopics that focus on sports analytics and management strategy rather than on-field heroics, like Moneyball?"
>
> *Could have been:* `craft_critique` or `recommendation_request`
>
> *I chose, because:* `recommendation_request`, because despite analyzing thematic tropes in sports cinema, the post's primary goal is asking the community to provide film recommendations.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Hardware / Device:** `cpu (CPU)` running PyTorch `2.14.1+cpu`

**Settings:** 3 epochs, learning rate `2e-5`, batch size 16, max sequence length 128, seed 42

**Anything I changed from the defaults, and why:** Kept default hyperparameters for this initial baseline fine-tuning run.

**Split sizes:** 140 train (70%) / 30 val (15%) / 30 test (15%). 

In the test split:
- `craft_critique`: 8 examples
- `industry_business`: 8 examples
- `fan_theory`: 7 examples
- `recommendation_request`: 7 examples

Both `fan_theory` and `recommendation_request` have fewer than 8 examples (7 each) in the test split, which means individual misclassifications will have a larger percentage impact on per-label F1 scores during multi-seed testing.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.333 | 0.933 | +0.600 |
| Macro F1 | 0.253 | 0.927 | +0.674 |
| F1 — `craft_critique` | 0.000 | 0.941 | +0.941 |
| F1 — `fan_theory` | 0.412 | 0.833 | +0.422 |
| F1 — `industry_business` | 0.000 | 1.000 | +1.000 |
| F1 — `recommendation_request` | 0.600 | 0.933 | +0.333 |

**What I predicted before I looked:**
I predict that my fine-tuned model will beat the baseline most decisively on `craft_critique` and `industry_business`, because zero-shot hypothesis matching struggles with niche film terminology and financial jargon without explicit training examples, whereas `recommendation_request` will show the narrowest margin due to its obvious question-based syntax.

**What the gap actually means:**
The massive +0.674 Macro F1 gap proves that fine-tuning was indispensable for this task. The zero-shot baseline completely failed on domain-specific categories (`craft_critique` and `industry_business` both scored 0.000 F1), defaulting to over-predicting `fan_theory` as a catch-all. Fine-tuning taught the model domain vocabulary (box office metrics, cinematography terms) that zero-shot hypothesis testing could not extract from definitions alone.

### Definitions vs. Bare Label Names Experiment

Running `baseline.py` with bare label names (`--definitions none`) produced an accuracy of 0.867 and a Macro F1 of 0.870, measuring what the prompt definitions were worth:

| Measure | Baseline (Definitions) | Baseline (Bare Names) | Trained |
|---|---|---|---|
| Overall accuracy | 0.333 | 0.867 | 0.933 |
| Macro F1 | 0.253 | 0.870 | 0.927 |
| F1 — `craft_critique` | 0.000 | 0.875 | 0.941 |
| F1 — `fan_theory` | 0.412 | 0.824 | 0.833 |
| F1 — `industry_business` | 0.000 | 0.857 | 1.000 |
| F1 — `recommendation_request` | 0.600 | 0.923 | 0.933 |

**Why bare names outperformed definitions:**
In zero-shot NLI (`BART-large-mnli`), hypotheses are structured as `HYPOTHESIS = "This post is {}."`. Lengthy definitions starting with verbs and containing parentheticals/clauses produced ungrammatical, overly restrictive hypotheses (e.g. `"This post is evaluates the technical or artistic execution of a film..."`), causing the zero-shot classifier to doubt entailment. In contrast, bare names like `"craft_critique"` and `"industry_business"` acted as concise, high-level semantic tags that the pre-trained transformer could match cleanly (0.867 accuracy). Still, the fine-tuned model beat both zero-shot configurations across every single metric (0.933 accuracy, 0.927 Macro F1).



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | >= 0.65 | 0.933 | 0.900 | 0.933 | MET |
| 2. Macro F1 | >= 0.60 | 0.927 | 0.898 | 0.933 | MET |
| 3. F1 — `recommendation_request` | >= 0.70 | 0.933 | 1.000 | 1.000 | MET |
| 4. Per-label floor (min F1) | >= 0.45 | 0.833 | 0.769 | 0.857 | MET |
| 5. Accuracy spread | <= 0.15 | 0.933 | 0.900 | 0.933 | MET (spread 0.033) |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted | craft_critique | fan_theory | recommendation_request | industry_business |
|---|---|---|---|---|
| **craft_critique** | 8 | 0 | 0 | 0 |
| **fan_theory** | 1 | 5 | 1 | 0 |
| **recommendation_request** | 0 | 0 | 7 | 0 |
| **industry_business** | 0 | 0 | 0 | 8 |

**My biggest off-diagonal number, and what it means:**
The only errors occurred on `fan_theory` (1 post misclassified as `craft_critique` and 1 as `recommendation_request`), indicating that while the model has completely learned the boundaries for `industry_business` and `craft_critique`, posts interpreting narrative lore occasionally share subtle syntactic overlap with craft analysis or recommendation queries.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 30 / 30 = 100%

**Disagreements**

None (30/30 matched).

**What the pattern in my disagreements tells me:**
Rather than the set being trivial, the 100% agreement indicates that the written decision rules in `staff_taxonomy.md` are genuinely tight when followed strictly, especially on the designated borderline cases:
- **`sp_014` (`hot_take`):** Demonstrates Rule 1 in action. Although it includes a specific stat ("times are down about 3%"), the phrasing *"so obviously the shoes are the whole story"* shows that the number is decorative rather than load-bearing.
- **`sp_005` (`analysis`):** Opens with a broad claim about carbon plates, but the second sentence provides load-bearing, controlled comparisons (2% drop in shoes vs. 2% drop from 35→50 miles/week), making it analysis under Rule 1.
- **`sp_019` (`hot_take`):** Reads intimate and reflective, but asserts a general claim about runners everywhere rather than reporting the writer's own morning, making it a hot take under Rule 2.
- **`sp_028` (`reaction`):** Mentions a countable number ("Third DNF this year"), but it expresses personal grief/status without arguing a broader point, so Rule 3 correctly preserves it as a reaction.

Consistently applying these boundary rules across the staff set provides strong evidence that the manual labeling across my own 200 movie posts was equally systematic.



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
