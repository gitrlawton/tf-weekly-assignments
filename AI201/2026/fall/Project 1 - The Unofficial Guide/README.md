# The Unofficial Guide

Ryan Lawton, advice_threads

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none, because the grader can't
> read it.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Week 1

## What This Does

I modified a retrieval-augmented question-answering system using the `advice_threads` corpus to answer practical college questions on dorms, academics, and campus life. The system retrieves relevant student discussions via semantic vector search and provides concise, cited answers while refusing queries outside the corpus.

## Chunking Strategy

**Chunk size:** 1000
**Overlap:** 0

I chose a chunk size of 1000 and 0 overlap because every document in `advice_threads` is a short forum thread under 815 characters. Keeping each thread intact prevents mid-sentence cuts and ensures the model always sees the thread title and all student replies together.

## Sample Chunks

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::split_documents`

```text
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.

--- reply 3 (22 votes) ---
Both true. I keep a cheap bike for September to November and walk the rest of the year. Total cost was about $120 for the bike and I don't care what happens to it.

--- reply 4 (5 votes) ---
If you do get one, the campus does free registration and it's the only reason I got mine back after it was taken.
```

**Chunk 2** — source: `thread_first_gen.txt#0` — produced by: `chunker.py::split_documents`

```text
THREAD: Anything specific for first-generation students?

--- reply 1 (33 votes) ---
The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.

--- reply 2 (41 votes) ---
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.

--- reply 3 (16 votes) ---
Emergency fund for textbooks and travel exists and is not means-tested beyond a short form.
```

**Chunk 3** — source: `thread_laptop_specs.txt#0` — produced by: `chunker.py::split_documents`

```text
THREAD: How much laptop do I actually need for CS courses?

--- reply 1 (31 votes) ---
Less than the recommended spec page says. 16GB of RAM is the one number worth paying for; everything else you'll never notice.

--- reply 2 (18 votes) ---
Adding: the lab machines exist and are better than anything you'll buy. For the heavy assignments people just use those.

--- reply 3 (12 votes) ---
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.
```

**Chunk 4** — source: `thread_office_hours_etiquette.txt#0` — produced by: `chunker.py::split_documents`

```text
THREAD: Is it weird to go to office hours with no specific question?

--- reply 1 (44 votes) ---
No, and this is the single most common thing first years get wrong. 'I'm following the lectures but I don't feel like I understand the shape of it' is a completely normal thing to say.

--- reply 2 (29 votes) ---
They're usually empty. You are doing the instructor a favour by turning up.

--- reply 3 (18 votes) ---
If it helps, treat it as a standing appointment. Go every week for a month and it stops feeling like a thing.
```

**Chunk 5** — source: `thread_professor_email.txt#0` — produced by: `chunker.py::split_documents`

```text
THREAD: Do professors actually answer email?

--- reply 1 (21 votes) ---
Varies enormously. General rule I've found: if the syllabus states a response window, it's honoured. If it doesn't, assume 48 hours and don't panic before then.

--- reply 2 (33 votes) ---
Office hours are dramatically more effective than email for anything that takes more than two sentences to answer. They're also usually empty.

--- reply 3 (15 votes) ---
Empty office hours is the biggest unused resource here and I say that having wasted a year not going.
```

## Sample Answer

**Question:** How much RAM do I need for CS courses?

**Answer:**

```text
  (best distance 0.257, cutoff 0.6)

You need 16GB of RAM for CS courses. 

Source: `thread_laptop_specs.txt`

Sources retrieved: thread_first_gen.txt, thread_laptop_specs.txt, thread_pass_fail.txt, thread_printing.txt, thread_professor_email.txt
```

**My relevance cutoff:** 0.60

I set my relevance cutoff to 0.60 because my five in-scope questions clustered tightly between 0.257 and 0.413, while all five out-of-scope questions were 0.828 or higher. Placing the cutoff at 0.60 sits right inside this 0.415 gap, allowing conversational variations of campus questions through while completely blocking unrelated topics.

| Question | In corpus? | Best distance |
|---|---|---|
| How much RAM do I need for CS courses? | Yes | 0.257 |
| When is the deadline to change your meal plan tier? | Yes | 0.322 |
| Is a bike worth it for a 20 minute commute? | Yes | 0.322 |
| What is the first step if you have a roommate conflict? | Yes | 0.348 |
| What happens if you turn in an assignment late? | Yes | 0.413 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.828 |
| How do I write a for loop in Rust? | No | 0.871 |
| How do I change the oil in a diesel engine? | No | 0.930 |
| What is the capital of Mongolia? | No | 0.948 |
| Who won the 1994 World Cup? | No | 0.952 |

## How I Used AI

**1.** I asked AI to test fixed window chunking at 350 characters, but seeing mid-sentence cutoffs and orphan headers led me to switch to 1000-character chunks to preserve entire discussion threads.

**2.** I asked AI to measure distance gaps for relevance cutoff tuning, and when near-miss campus queries slipped past the 0.60 gate, I added a second-layer grounding prompt in `generate.py` to enforce explicit refusals.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Week 2


## Run Log — Before


| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks start/end on complete thoughts | 8 of 10 | 10 of 10 | 10 of 10 | 10 of 10 | MET |
| 5. Top distance <= 0.30 | 4 of 5 | 1 of 5 | 1 of 5 | 1 of 5 | MISSED |

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer (target: 4 of 5) | MET | I checked the retrieved sources across all 15 runs and confirmed that every single run returned the exact source thread containing the answer. |
| 2 | Every answer names a source (target: 5 of 5) | MET | I read all 15 generated responses and verified that each answer explicitly named its source document filename. |
| 3 | Gate stops out-of-corpus questions (target: 4 of 5) | MET | I verified that all 5 out-of-scope questions had distances above 0.82 and were cleanly refused by the gate with zero model calls. |
| 4 | Chunks start/end on complete thoughts (target: 8 of 10) | MET | I inspected sample chunks from `app.py chunks` and found that keeping 1000-character chunks ensured 10 of 10 chunks were full discussion threads with zero split sentences. |
| 5 | Top distance <= 0.30 (target: 4 of 5) | MISSED | I looked at the actual best distances in the run log and found that only 1 of my 5 questions scored <= 0.30 (0.257), while the other four ranged from 0.322 to 0.413. |

> **Revision for Criterion 5:**
> - **Revised in week 2:** For at least 4 of 5 test questions, the rank-1 retrieved chunk is the correct document containing the answer, and its distance is at least 0.15 below the 0.60 relevance cutoff.
> - **Why revised:** Measuring an absolute distance target of <= 0.30 penalized natural phrasing variations rather than retrieval accuracy; questions like late work retrieved the exact right document at rank 1 with 100% correct facts, but scored 0.413 simply because of query phrasing and length.

## Diagnoses

**Missed Criterion 5: Top distance <= 0.30 (scored 1 of 5)**

- **Stage:** **Chunking & Embedding**
- **Mechanism:** Because I configured chunk size to 1000 characters to keep each advice thread intact as a single chunk, each chunk contains the thread title along with 3 to 4 distinct student replies and vote counts. The embedding model (`all-MiniLM-L6-v2`) produces a dense vector that represents the blended semantic average of the whole discussion. When a user asks a short, specific question targeting one individual detail (like the 10-day deadline in `thread_meal_plan_tier.txt`), matching a short query against an 800-character multi-reply thread dilutes the cosine similarity, floating distances into the `0.32` to `0.41` range even though the retrieved document is 100% correct.
- **Pattern across misses:** All four misses followed the exact same pattern: the query asked about a specific detail contained in a single reply within a larger thread chunk. The only question that scored <= 0.30 was the CS RAM question (`0.2570`), where the query vocabulary mirrored the thread title and primary reply almost verbatim.

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
