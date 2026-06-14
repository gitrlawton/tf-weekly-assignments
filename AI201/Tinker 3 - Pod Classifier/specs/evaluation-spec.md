# Evaluation Spec — Pod Classifier

Complete this spec **before** writing any code for Milestone 3.

Use Plan or Ask mode to think through each blank field. When you're done,
your answers here become the blueprint for `compute_accuracy()` and
`compute_per_class_accuracy()` in `evaluate.py`.

---

## Background: What is evaluation?

After building a classifier, we need to know how well it works. Evaluation answers:
- **Overall:** What fraction of episodes did we classify correctly?
- **Per-class:** Are we better at some labels than others?

Both functions take the same inputs: a list of predicted labels and a list of
ground-truth labels, in the same order.

---

## compute_accuracy(predictions, ground_truth)

### What it does
Returns the fraction of predictions that exactly match the ground truth.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `predictions` | `list[str]` | Labels predicted by `classify_episode()`, one per episode. |
| `ground_truth` | `list[str]` | The correct labels, in the same order as `predictions`. |

### Output

| Return value | Type | Description |
|---|---|---|
| accuracy | `float` | A value between 0.0 and 1.0. |

---

### Spec fields — fill these in before writing code

**Formula:**

```
accuracy = number of positions where predictions[i] == ground_truth[i]
           ÷ total number of predictions

"Correct" means the predicted label exactly matches the ground-truth label at
the same index. Divide by the length of the list (total episodes evaluated).
```

---

**Step-by-step logic:**

```
1. If both lists are empty, return 0.0.
2. Count the number of indices where predictions[i] == ground_truth[i].
3. Divide that count by len(predictions) and return the result as a float.
```

---

**Edge case — what if both lists are empty?**

```
Return 0.0. There are no episodes to evaluate, so there are no correct
predictions. Returning 0.0 also avoids a ZeroDivisionError from dividing
by len([]).
```

---

**Worked example:**

```
predictions  = ["interview", "solo", "panel", "interview"]
ground_truth = ["interview", "solo", "solo",  "narrative"]

Index 0: "interview" == "interview" ✓
Index 1: "solo"      == "solo"      ✓
Index 2: "panel"     != "solo"      ✗
Index 3: "interview" != "narrative" ✗

correct = 2, total = 4
accuracy = 2 / 4 = 0.5
```

---

## compute_per_class_accuracy(predictions, ground_truth)

### What it does
Returns accuracy broken down by each label. For each label in `VALID_LABELS`,
reports how many episodes with that ground-truth label were classified correctly.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `predictions` | `list[str]` | Labels predicted by `classify_episode()`. |
| `ground_truth` | `list[str]` | Correct labels, in the same order. |

### Output

A `dict` keyed by label. Each value is a dict with three keys:

```python
{
    "interview": {"correct": int, "total": int, "accuracy": float},
    "solo":      {"correct": int, "total": int, "accuracy": float},
    "panel":     {"correct": int, "total": int, "accuracy": float},
    "narrative": {"correct": int, "total": int, "accuracy": float},
}
```

---

### Spec fields — fill these in before writing code

**What does "correct" mean for a given class?**

```
An episode counts as correct for class X when ground_truth[i] == X AND
predictions[i] == X. Both must be true: the episode actually belongs to
class X, and the model predicted X for it.
```

---

**What does "total" mean for a given class?**

```
Total for class X = the number of episodes where ground_truth[i] == X.
It is the count of episodes that actually belong to that class, regardless
of what the model predicted. It is NOT the total number of all predictions.
```

---

**Step-by-step logic:**

```
1. Initialize a dict for each label in VALID_LABELS with correct=0, total=0.
2. Loop over zip(predictions, ground_truth) to get each (predicted, truth) pair.
3. For each pair: increment total[truth] by 1; if predicted == truth, also
   increment correct[truth] by 1.
4. After the loop, compute accuracy for each label: correct / total if total > 0,
   else 0.0.
5. Return the dict with all four labels populated.
```

---

**Edge case — what if a class has no examples in ground_truth (total == 0)?**

```
Set accuracy to 0.0. Dividing correct / total would be a ZeroDivisionError,
and None would break any downstream comparison. 0.0 signals "no data" without
crashing — the caller can check total == 0 if they need to distinguish it from
a class that was always wrong.
```

---

**Worked example:**

```
predictions  = ["interview", "interview", "solo", "panel", "panel"]
ground_truth = ["interview", "solo",      "solo", "panel", "narrative"]

Pair-by-pair:
  (interview, interview) → interview total+1, interview correct+1
  (interview, solo)      → solo total+1       (predicted wrong, no correct++)
  (solo,      solo)      → solo total+1, solo correct+1
  (panel,     panel)     → panel total+1, panel correct+1
  (panel,     narrative) → narrative total+1  (predicted wrong, no correct++)

label       correct  total  accuracy
----------  -------  -----  --------
interview      1       1      1.0
solo           1       2      0.5
panel          1       1      1.0
narrative      0       1      0.0
```

---

## Reflection questions (discuss at the checkpoint)

1. Your overall accuracy might be decent even if one class has very low accuracy.
   Why is per-class accuracy a more informative metric than overall accuracy alone?

2. If `panel` episodes consistently get misclassified as `interview`, what does
   that tell you about your training labels or your prompt?

3. You labeled 20 training episodes and evaluated on 20 test episodes (5 per class).
   How might the evaluation results change if you had labeled 100 training episodes?
   What if you had 200 test episodes?
