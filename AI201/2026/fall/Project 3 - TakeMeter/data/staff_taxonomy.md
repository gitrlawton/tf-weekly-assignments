# The staff set — taxonomy and rules

**Read this before you label. It is the whole instruction set.**

The 30 posts in `data/staff_posts.csv` come from the same fictional running
forum as `data/practice_labels.csv`. Staff labelled them under the three
definitions below.

**Label the 30 posts under *these* definitions, not your own.** That is the
point of the exercise, and it is different from what you did in unit 5. Your
own taxonomy was yours to design; this one is somebody else's to apply. What is
being measured is whether you can take a written rule you did not write and
apply it the same way its authors did — which is exactly the skill that decides
whether your own 200 labels were consistent.

If your project happens to use these three labels too, that is a coincidence.
Use the definitions on this page either way.

---

## The three labels

**`analysis`** — makes an argument backed by a specific, checkable fact. A
stat, a date, a time, a quote, a named comparison. The fact has to do work in
the argument.

**`hot_take`** — a confident claim with no support offered. It might be true.
It isn't argued. Strength of feeling is not support.

**`reaction`** — an immediate response to something that just happened.
Feeling rather than argument. Usually about the writer's own experience, in the
last few hours.

---

## The decision rules

These exist because the boundaries are where labelling falls apart. Staff
applied all three.

**1. `analysis` vs `hot_take` — does the fact carry the argument?**

A post is `analysis` only if the checkable fact is load-bearing. If the number
is decoration on a conclusion the writer had already reached, it is a
`hot_take` with a statistic in it.

> *"Super shoes have ruined racing, times are down 3% since 2017."* → `hot_take`.
> The 3% is offered as a flourish, not as the reason.

> *"Times are down 3% since 2017, and the shoe rule changed in 2017. That's the
> most likely single cause."* → `analysis`. The number is the argument.

**2. `reaction` vs `hot_take` — is it about a claim or about the writer?**

Both are unsupported. `reaction` reports what just happened to the writer and
how it felt. `hot_take` asserts something general about the world.

> *"That finish was unbelievable, I'm shaking."* → `reaction`.
> *"That was the best race of the decade."* → `hot_take`.

A post can be heated and still be `hot_take` if it is making a general claim.

**3. `reaction` vs `analysis` — recency does not outrank evidence.**

A post written minutes after a race is still `analysis` if it argues from a
checkable fact. Immediacy is not the deciding feature; the presence of a
load-bearing fact is.

**4. When two labels are still defensible, pick the one the post spends most of
its words on.** This is a tie-break, not a licence — reach for it only after
rules 1 to 3.

---

## What to produce

A CSV called `my_staff_labels.csv` with a `text` column and a `label` column,
30 rows, the text pasted **exactly** as it appears in `staff_posts.csv`.
`agreement.py` matches on the text, so a retyped or trimmed post won't match
and the script will tell you which.

Then, and only then, ask your TF for `data/staff_labels.csv` and run:

```bash
python agreement.py
```

---

## A note on what the rate means

Staff picked several of these 30 posts **because** they are genuinely
ambiguous. A rate in the 70s is normal and expected. It is not a mark out of
100 and it is not graded.

What is graded is the adjudication: for every disagreement, a written call
saying who you think is right and why, argued from the definitions on this
page. "Staff is right" every time earns nothing — some of these you should
win.
