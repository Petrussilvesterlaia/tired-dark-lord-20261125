#!/usr/bin/env python3
"""The Tired Dark Lord: A 100-Word Villain Monologue.

Writes one monologue to /output/entry.txt, then reads the file back
and verifies it is byte-identical to the validated text.

The monologue is a fixed string: no dependencies, no network,
no randomness, so every run produces the same bytes.
"""

import os
import sys

OUTPUT_PATH = "/output/entry.txt"

MONOLOGUE = (
    "Hero, sit. No\u2014stand. The chains fit, I checked. Twice. "
    "I am Malachar, Lord of the Hollow Hill, and I have kept your "
    "king's crown in a pickle jar since the war of the three moons. "
    "Tonight I meant to end you with the curse of black rain, but I "
    "left the words in the tower. Nine hundred stairs. So the vale "
    "waits. I had the spell, the salt, the moonless night, all lined "
    "up to turn it to glass. Then the well went dry, the goat died, "
    "and my knee learned that click. Tomorrow. Bring bread. "
    "The rats ate mine."
)

# Words that would announce the tiredness outright; the monologue
# must show it through rhythm and deflection instead.
FORBIDDEN_WORDS = (
    "tired",
    "weary",
    "exhausted",
    "sleepy",
    "drowsy",
    "fatigued",
    "yawning",
)


def fail(message):
    print("validation failed: " + message, file=sys.stderr)
    sys.exit(1)


def validate(text):
    if not text or not text.strip():
        fail("text is empty or only whitespace")
    if text != text.strip():
        fail("text has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        fail("text must be a single line with no newline characters")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        fail("text contains control characters")
    words = text.split()
    if not 95 <= len(words) <= 105:
        fail("word count %d is outside 95-105" % len(words))
    if not 1 <= len(text) <= 600:
        fail("character count %d is outside 1-600" % len(text))
    lowered = text.lower()
    for banned in FORBIDDEN_WORDS:
        if banned in lowered:
            fail("text contains forbidden word %r" % banned)
    return words


def main():
    words = validate(MONOLOGUE)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(MONOLOGUE)

    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != MONOLOGUE.encode("utf-8"):
        fail("entry.txt is not byte-identical to the validated text")

    print("words: %d" % len(words))
    print("characters: %d" % len(MONOLOGUE))
    print("wrote %s (%d bytes)" % (OUTPUT_PATH, len(written)))


if __name__ == "__main__":
    main()
