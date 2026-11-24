#!/usr/bin/env python3
"""Say What Actually Broke — one line of brutal-truth error copy.

The program writes a single-line software error message (at most 200
characters) to ``entry.txt`` under the output directory: the failure named
in plain words, the joke intact, and what to do next. No network, no
randomness, no input read: the same line every run, byte for byte.

Run locally:

    MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py

In the grading sandbox the output directory is ``/output``.
"""

import os

# The entry: a wrong-password error that tells the brutal truth — the
# system will not say whether the username was wrong too, and the twist
# is the one detail the user can actually check: Caps Lock.
ENTRY = (
    "Wrong password \u2014 and no, we can't tell you if the username was "
    "wrong too. Caps Lock is on, by the way. Try again."
)


def check_gate(line):
    """Self-check the competition gate before writing anything."""
    if not isinstance(line, str):
        raise ValueError("entry is not text")
    if not (1 <= len(line) <= 200):
        raise ValueError("entry must be 1 to 200 characters, got %d" % len(line))
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")


def main():
    line = ENTRY
    check_gate(line)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the file holds exactly the one line, so the
    # scorer reads 1-200 characters of single-line UTF-8 text.
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    # The grader collects outputs as another user: leave the file readable.
    os.chmod(path, 0o644)
    try:
        # Best effort only: the sandbox may mount the output directory in
        # a way that forbids changing its own mode, and the entry file
        # above is already written, so never fail the run over this.
        os.chmod(out_dir, 0o755)
    except OSError:
        pass


if __name__ == "__main__":
    main()
