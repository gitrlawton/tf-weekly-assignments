"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies (coefficient of variation: stdev / mean).

    Returns:
        A float >= 0. Higher means more variation (more human).
        0.0 means completely uniform, or fewer than two sentences.
    """
    sents = sentences(text)
    if len(sents) < 2:
        return 0.0

    lengths = [len(words(s)) for s in sents]
    lengths = [l for l in lengths if l > 0]
    if len(lengths) < 2:
        return 0.0

    mean_len = statistics.mean(lengths)
    if mean_len == 0:
        return 0.0

    stdev_len = statistics.stdev(lengths)
    return round(stdev_len / mean_len, 4)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words.

    Returns:
        A float between 0.0 and 1.0. Higher means more varied vocabulary.
    """
    w = words(text)
    if not w:
        return 0.0
    return round(len(set(w)) / len(w), 4)


def punctuation_density(text: str) -> float:
    """
    How much punctuation relative to word count.

    Counts expressive punctuation (commas, semicolons, colons, dashes, quotes, etc.).
    Returns:
        A float >= 0.0. Higher means richer punctuation usage.
    """
    w = words(text)
    if not w:
        return 0.0
    punct_matches = re.findall(r"[,;:\—\-\(\)\"\'\?!]", text)
    return round(len(punct_matches) / len(w), 4)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Combines:
      1. sentence_length_spread: low spread (uniform rhythm) -> higher AI score.
      2. type_token_ratio: lower vocabulary variation -> higher AI score.
      3. punctuation_density: sparse/flat punctuation -> higher AI score.
    """
    w = words(text)
    if not w:
        return 0.5

    sents = sentences(text)
    spread = sentence_length_spread(text)
    ttr = type_token_ratio(text)
    punct = punctuation_density(text)

    # 1. Spread: Human CV is typically 0.40 - 0.90+. AI prose is typically 0.10 - 0.35.
    if len(sents) < 2:
        ai_spread = 0.5  # single-sentence edge case is neutral
    else:
        ai_spread = 1.0 - min(max((spread - 0.15) / 0.50, 0.0), 1.0)

    # 2. Vocabulary richness (Type-Token Ratio):
    ai_ttr = 1.0 - min(max((ttr - 0.45) / 0.40, 0.0), 1.0)

    # 3. Punctuation density:
    ai_punct = 1.0 - min(max((punct - 0.03) / 0.17, 0.0), 1.0)

    # Weighted combination: spread (0.50) + ttr (0.30) + punct (0.20)
    score = (0.50 * ai_spread) + (0.30 * ai_ttr) + (0.20 * ai_punct)
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
