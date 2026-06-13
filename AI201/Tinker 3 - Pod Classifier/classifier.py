import json
import os
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_LABELS, DATA_PATH, TRAIN_FILE, LABELS_FILE

_client = Groq(api_key=GROQ_API_KEY)


def load_labeled_examples() -> list[dict]:
    """
    Load the training episodes and merge them with the student's labels.

    Returns a list of dicts, each with:
      - "id"          : episode ID
      - "title"       : episode title
      - "podcast"     : podcast name
      - "description" : episode description
      - "label"       : the label from my_labels.json (may be None if not yet annotated)

    Only returns episodes where the label is a valid, non-null string.
    Episodes with null labels are silently skipped.
    """
    train_path = os.path.join(DATA_PATH, TRAIN_FILE)
    labels_path = os.path.join(DATA_PATH, LABELS_FILE)

    with open(train_path, encoding="utf-8") as f:
        episodes = {ep["id"]: ep for ep in json.load(f)}

    with open(labels_path, encoding="utf-8") as f:
        labels = {entry["id"]: entry["label"] for entry in json.load(f)}

    labeled = []
    for ep_id, ep in episodes.items():
        label = labels.get(ep_id)
        if label in VALID_LABELS:
            labeled.append({**ep, "label": label})

    return labeled


def build_few_shot_prompt(labeled_examples: list[dict], description: str) -> str:
    task_instruction = """You are classifying podcast episodes by their format. Classify the episode into exactly one of these four labels:

- interview: a conversation between a host and one or more guests
- solo: a single host speaking from memory, experience, or opinion — no guests, no assembled external sources
- panel: multiple guests with roughly equal speaking time, often debating or discussing a topic together
- narrative: a story assembled from external sources — interviews, archival audio, reporting — with a clear narrative arc

Return only the label and your reasoning. Do not explain the taxonomy."""

    examples_block = ""
    for ex in labeled_examples:
        examples_block += f"\nTitle: {ex['title']}\nDescription: {ex['description']}\nLabel: {ex['label']}\n---"

    new_episode = f"\nTitle: [unknown]\nDescription: {description}\nLabel: ?"

    output_instruction = """
Classify the episode above. Return your answer in this format:
Label: {one of: interview, solo, panel, narrative}
Reasoning: {one sentence explaining the key signal that determined the label}"""

    return f"{task_instruction}\n{examples_block}\n{new_episode}\n{output_instruction}"


def classify_episode(description: str, labeled_examples: list[dict]) -> dict:
    try:
        prompt = build_few_shot_prompt(labeled_examples, description)

        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
        )

        response_text = response.choices[0].message.content or ""
        print(response_text)

        label_raw = ""
        reasoning = ""
        for line in response_text.strip().splitlines():
            if line.lower().startswith("label:"):
                label_raw = line.split(":", 1)[1].strip().lower()
            elif line.lower().startswith("reasoning:"):
                reasoning = line.split(":", 1)[1].strip()

        label = label_raw if label_raw in VALID_LABELS else "unknown"

        return {"label": label, "reasoning": reasoning}

    except Exception:
        return {"label": "unknown", "reasoning": ""}
