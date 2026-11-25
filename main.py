#!/usr/bin/env python3
"""Write the "Your Week in One Line" entry to /output/entry.txt.

Method, in plain prose: the entry is one fixed line, picked once and never
varied while the program runs. The program first checks the line against the
same gate the sealed scorer applies: UTF-8 text, between 1 and 100
characters, not only white space, and exactly one line. It then writes the
line to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt) with no
trailing newline, reads the file back, and checks that what is on disk is
byte for byte the line it meant to write, re-checking the gate on the disk
content too, so a bad write can never pass silently. It prints the line and
its character count on success. No network, no randomness, no input, no
clock: two runs produce byte-identical output.
"""

import os
import sys

WEEK_LINE = "168 entries shipped, $0 won, one roast scored 59%, and the news-image relay died twice."

LOWER = 1
UPPER = 100


def gate_ok(text):
    """Check the sealed gate; return None when the text passes, else a reason."""
    if not isinstance(text, str):
        return "entry is not text"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return "entry is not valid UTF-8 text"
    if not (LOWER <= len(text) <= UPPER):
        return "entry is %d characters, gate needs %d-%d" % (
            len(text),
            LOWER,
            UPPER,
        )
    if not text.strip():
        return "entry is only white space"
    if "\n" in text or "\r" in text:
        return "entry is not a single line"
    return None


def main():
    problem = gate_ok(WEEK_LINE)
    if problem is not None:
        print("gate failed before write: %s" % problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(WEEK_LINE)

    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        on_disk = handle.read()
    if on_disk != WEEK_LINE:
        print("round-trip mismatch: disk does not match the line", file=sys.stderr)
        return 1
    problem = gate_ok(on_disk)
    if problem is not None:
        print("gate failed on disk: %s" % problem, file=sys.stderr)
        return 1

    print("wrote %s (%d characters)" % (out_path, len(on_disk)))
    print(on_disk)
    return 0


if __name__ == "__main__":
    sys.exit(main())
