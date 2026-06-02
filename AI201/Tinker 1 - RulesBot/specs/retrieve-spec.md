# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter   | Type  | Description                                                                |
| ----------- | ----- | -------------------------------------------------------------------------- |
| `query`     | `str` | The user's natural language question                                       |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key          | Type    | Description                                                   |
| ------------ | ------- | ------------------------------------------------------------- |
| `"text"`     | `str`   | The chunk text                                                |
| `"game"`     | `str`   | The game name this chunk came from                            |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

_Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours._

---

### Query approach

_Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?_

```
[your answer here]
```

---

### Return structure

_Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?_

```
  {
      "text":     "If you roll a 7, you must move the robber to any terrain hex...",
      "game":     "Catan",
      "distance": 0.182
  }
```

---

### Handling the nested result structure

_`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists._

```
Index [0] on each field — documents[0], metadatas[0], distances[0].   Each [0] gives you a parallel list of the same length (one entry per result), then zip the corresponding elements together into the dict shape the spec requires.

Why the nesting exists:

_collection.query() is designed for batch querying — you can pass multiple query strings at once via query_texts. It always returns one inner list per query, so the outer list has one entry per query string you passed in. Since you're only ever passing a single query (query_texts=[query]), the outer list always has exactly one element, and [0] unwraps it to get the actual list of results.

The nesting is a design choice so that batch callers get a uniform shape regardless of how many queries they sent.
```

---

### Relevance threshold

_Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?_

```
Return all n_results without filtering.

For this project, the cleaner split is to return all results from retrieve() unfiltered, and let generate_response() apply a distance
threshold before building the prompt — that way retrieval and grounding are separate concerns. The system design doc even flags 0.5 as
the rough relevance boundary for all-MiniLM-L6-v2, so that's a reasonable starting cutoff to try in the generator.

The tradeoffs:

┌───────────────────────┬───────────────────────────────────────────────┬─────────────────────────────────────────────────────────┐
│       Approach        │                      Pro                      │                           Con                           │
├───────────────────────┼───────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ No threshold — return │ Simple; generate_response() can decide what   │ Passes weak chunks to the LLM, which may get confused   │
│  all n_results        │ to use; never silently drops a valid result   │ or hallucinate                                          │
├───────────────────────┼───────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ Filter above a        │ Keeps only genuinely relevant context;        │ May return fewer than n_results or even an empty list   │
│ distance cutoff (e.g. │ reduces LLM confusion                         │ for niche questions; the right cutoff is hard to pick   │
│  0.5)                 │                                               │ without testing                                         │
└───────────────────────┴───────────────────────────────────────────────┴─────────────────────────────────────────────────────────┘

```

---

### Edge cases

_How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?_

```
[your answer here]
```

---

## Implementation Notes

_Fill this in after implementing, before moving to Milestone 3._

**Test query and top result returned:**

```
Query: "What happens when you roll a 7?"
Top result game: Catan
Distance score: 0.466
Does it make sense? Yes — the top chunk begins with the header "ROLLING A 7" and
describes exactly the rule the query asks about. It was the only result below the
0.5 threshold; results 2–5 were all noise from other games (Risk, Uno, Monopoly)
with distances in the 0.60–0.63 range.

Query: "How do you win?"
Top result game: Monopoly
Distance score: 0.507
Does it make sense? Yes — the top chunk contains a "WINNING" section describing
elimination-based victory. More notably, all 5 results came from 5 different games
(Monopoly, Risk, Ticket to Ride, Uno, Catan), which is the correct behavior for a
concept that exists across every game in the collection. However, every result was
above 0.5, meaning a strict 0.5 threshold would return no context at all for this
query despite the results being genuinely relevant.
```

**One thing about the query results that surprised you:**

```
Even the correct, on-topic Catan chunk for "roll a 7" only scored 0.466 — the
right answer came back first, but its distance was uncomfortably close to the 0.5
cutoff. A slightly noisier document or a slightly different phrasing could have
pushed it above the threshold entirely.
```
