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
    How much sentence length varies.

    Returns:
        A float representing the coefficient of variation (stdev / mean) of
        sentence word counts. Higher values mean more varied, bursty sentence
        structures (more typical of human writing). Returns 0.0 for fewer than
        two sentences.
    """
    s_list = sentences(text)
    lengths = [len(words(s)) for s in s_list if words(s)]
    if len(lengths) < 2:
        return 0.0
    mean_len = statistics.mean(lengths)
    if mean_len <= 0:
        return 0.0
    stdev_len = statistics.stdev(lengths)
    return round(stdev_len / mean_len, 4)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words.

    Returns:
        A float between 0.0 and 1.0. Higher means more varied vocabulary
        (more typical of human writing).
    """
    w = words(text)
    if not w:
        return 0.0
    return round(len(set(w)) / len(w), 4)


def punctuation_density(text: str) -> float:
    """
    How much expressive punctuation, relative to word length.

    Counts expressive and structuring marks: commas, semicolons, colons,
    dashes (em-dash, en-dash, hyphen), parentheses, quotation marks,
    exclamation points, and question marks relative to word count.
    Higher means richer, more varied punctuation (more typical of human writing).
    """
    w = words(text)
    if not w:
        return 0.0
    marks = re.findall(r"[,;:—–\-\(\)\?\!\"']", text)
    return round(len(marks) / len(w), 4)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Combines sentence length spread, type-token ratio, and punctuation density.
    All three measures are inverted and scaled onto [0.0, 1.0] so that:
      - 1.0 indicates uniform, repetitive, flatly-punctuated prose (AI-like)
      - 0.0 indicates bursty, lexically diverse, expressively punctuated prose (Human-like)
    """
    s_list = sentences(text)
    w = words(text)
    if not w:
        return 0.5

    cv = sentence_length_spread(text)
    ttr = type_token_ratio(text)
    pd = punctuation_density(text)

    # 1. Sentence length spread: CV <= 0.15 is AI-like (1.0), CV >= 0.55 is human-like (0.0).
    # If there is only one sentence, variance cannot be assessed — return neutral (0.5).
    if len(s_list) < 2:
        spread_ai = 0.5
    else:
        spread_ai = max(0.0, min(1.0, 1.0 - (cv - 0.15) / (0.55 - 0.15)))

    # 2. Type-token ratio: TTR <= 0.70 is AI-like (1.0), TTR >= 0.92 is human-like (0.0).
    ttr_ai = max(0.0, min(1.0, 1.0 - (ttr - 0.70) / (0.92 - 0.70)))

    # 3. Punctuation density: density <= 0.04 is AI-like (1.0), density >= 0.14 is human-like (0.0).
    pd_ai = max(0.0, min(1.0, 1.0 - (pd - 0.04) / (0.14 - 0.04)))

    # Weighted combination: cadence variance (0.45), punctuation (0.35), vocabulary (0.20)
    score = 0.45 * spread_ai + 0.35 * pd_ai + 0.20 * ttr_ai
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
