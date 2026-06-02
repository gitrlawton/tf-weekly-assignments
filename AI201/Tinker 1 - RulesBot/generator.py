from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    context_block = "\n\n".join(
        f'<source index="{i}" game="{chunk["game"]}">\n{chunk["text"]}\n</source>'
        for i, chunk in enumerate(retrieved_chunks, 1)
    )

    system_prompt = (
        "You are a board game rules assistant. Answer questions using ONLY the rule text "
        "provided in the CONTEXT block. Do not draw on your training knowledge of any board "
        "game — not even to fill gaps, correct apparent errors, or add helpful context you "
        "happen to know. Treat the provided text as the sole and complete source of truth. "
        "If the CONTEXT does not contain enough information to fully answer the question, "
        "say so explicitly: do not guess, infer, or speculate about rules that are not "
        "stated in the text.\n\n"
        "Always state which game your answer comes from, using the game name exactly as it "
        "appears in the CONTEXT. If the context contains rules from more than one game, keep "
        "each game's rules separate — do not blend or compare rules across games unless the "
        "user explicitly asks you to."
    )

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"CONTEXT:\n{context_block}\n\nQUESTION: {query}"},
        ],
    )

    return response.choices[0].message.content
