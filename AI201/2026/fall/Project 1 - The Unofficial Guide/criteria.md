# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in week 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next week costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**

I picked 4 of 5 because while four of my questions target common, heavily-discussed topics in the threads, one is about a specific detail mentioned in only a single reply, making it much easier for retrieval to miss. Expecting 5 of 5 before tuning the chunking feels overly optimistic, but getting fewer than 4 would mean retrieval is failing on obvious thread topics.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**


I am requiring all 5 answers to cite a source because the system prompt explicitly passes the filename alongside each retrieved reply. If the model answers without naming a thread, it means it is ignoring prompt instructions or hallucinating general advice instead of grounding its response in what students actually posted.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**

I chose 4 of 5 because four of the out-of-scope questions (like car maintenance or world history) have zero conceptual overlap with college forum threads, but one might share common vocabulary with campus life. Setting a looser goal like 3 of 5 would allow too many unrelated queries through to the generator.

<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

---

## 4. Chunks

Across a sample of 10 chunks, at least 8 of them start and end on complete sentences rather than mid-sentence cuts.
(test with `python app.py chunks -n 10`)


**Why this target:**

The advice_threads corpus is organized into short, discrete replies separated by vote count headers. I chose 8 of 10 because each chunk needs to hold the substantive student advice rather than cutting off halfway through a reply or capturing an empty header, while leaving a small allowance for rare longer replies that might span across chunk boundaries.

---

## 5. Maximum distance

For at least 4 of my 5 test questions, the closest retrieved chunk is 0.30 or lower.



**Why this target:**

Because the advice threads use conversational student phrasing that closely mirrors how someone would ask a question, the vector embedder should find very tight semantic matches for direct queries.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     WEEK 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in week 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
