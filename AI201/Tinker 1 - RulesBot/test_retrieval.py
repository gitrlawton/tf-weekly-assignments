"""
Quick retrieval smoke test — run directly:
    python test_retrieval.py

Tests two query types:
  1. Specific (single-game anchor): "What happens when you roll a 7?"
  2. Cross-game: "How do you win?"

For each query, prints results with distance scores and a relevance read.
Also prints a sample of raw chunks so you can judge whether chunk size
is carrying enough semantic signal.
"""

from retriever import _collection, retrieve

# ── Diagnostics: raw chunk sample ────────────────────────────────────────────

total = _collection.count()
print(f"Collection has {total} chunk(s) total.\n")

if total == 0:
    print("Collection is empty — run ingest first (python app.py, then option 1).")
    raise SystemExit(1)

sample = _collection.get(limit=5, include=["documents", "metadatas"])
print("-- Sample chunks (first 5 in collection) ----------------------------------")
for doc, meta in zip(sample["documents"], sample["metadatas"]):
    print(f"  [{meta['game']}] {doc[:120]!r}")
print()


# ── Helper ────────────────────────────────────────────────────────────────────

def run_query(label, query, n=5):
    print(f"-- Query: {label!r} {'=' * 50}")
    print(f"   \"{query}\"\n")
    chunks = retrieve(query, n_results=n)
    if not chunks:
        print("  (no results)\n")
        return
    for i, chunk in enumerate(chunks, 1):
        relevant = "  " if chunk["distance"] < 0.5 else "??"
        print(f"  {relevant} #{i} [{chunk['game']}] dist={chunk['distance']:.3f}")
        print(f"       {chunk['text'][:160]}")
        if len(chunk["text"]) > 160:
            print(f"       ...({len(chunk['text'])} chars total)")
        print()
    games = [c["game"] for c in chunks]
    unique_games = list(dict.fromkeys(games))
    print(f"  Games returned: {games}")
    print(f"  Unique games:   {unique_games}")
    below_threshold = sum(1 for c in chunks if c["distance"] < 0.5)
    print(f"  Results with distance < 0.5: {below_threshold}/{len(chunks)}")
    print()


# ── Test 1: specific, single-game anchor ─────────────────────────────────────
run_query("specific", "What happens when you roll a 7?")

# ── Test 2: cross-game concept ────────────────────────────────────────────────
run_query("cross-game", "How do you win?")
