"""
generate_response() smoke test — run directly:
    python test_generator.py

Three checks:
  1. Specific factual (Catan roll-a-7): answer should be fully traceable to
     the retrieved chunks printed alongside it — nothing the model couldn't
     have known from that text alone.
  2. Temptation to elaborate (Catan building costs): the model almost certainly
     knows the exact settlement/city/road costs from training. Check whether it
     sticks to what the chunks say or adds detail that isn't there.
  3. Out-of-rulebook (Chess): no Chess rulebook was loaded, so retrieved chunks
     will be from other games. RulesBot should admit it can't answer — not
     improvise a Chess answer from training knowledge.
"""

from retriever import retrieve
from generator import generate_response


def run_test(label, query):
    print(f"\n{'=' * 62}")
    print(f"TEST   : {label}")
    print(f"QUERY  : {query}")
    print("=" * 62)

    chunks = retrieve(query)

    print(f"\nRetrieved {len(chunks)} chunk(s) -- THIS IS ALL THE MODEL CAN SEE:")
    for i, chunk in enumerate(chunks, 1):
        print(f"\n  [{i}] {chunk['game']}  dist={chunk['distance']:.3f}")
        print(f"  {chunk['text'][:220]}")
        if len(chunk["text"]) > 220:
            print(f"  ... ({len(chunk['text'])} chars total)")

    print("\nRESPONSE:")
    print("-" * 40)
    print(generate_response(query, chunks))
    print("-" * 40)
    print()


# 1. Specific factual — trace every claim in the response back to a chunk above
run_test(
    "specific factual",
    "What happens when you roll a 7 in Catan?",
)

# 2. Temptation to elaborate — chunks may mention building exists but not costs;
#    watch for the model filling in the exact numbers from training knowledge
run_test(
    "temptation to elaborate",
    "What does it cost to build a settlement in Catan?",
)

# 3. Out-of-rulebook — Chess was never ingested; chunks will be from other games;
#    a grounded model must say so rather than answering from training
run_test(
    "out of rulebook",
    "How do you castle in Chess?",
)
