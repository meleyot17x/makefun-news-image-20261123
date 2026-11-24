#!/usr/bin/env python3
"""THE DAY'S POST — entry runner for news-image-20261123 (final3, G4).

The artwork itself is entry.png, drawn by compose.py in this same session:
a sepia broadsheet front page with teal ink and brick-red accents that sums
up Monday 23 November 2026 in 41 stories, led by the US Army plan to
detonate unstable explosives in Iowa.

This runner is deliberately boring: standard library only, no image
libraries, no transformation. It reads the PNG sitting next to it, checks
the magic header, the 1 MiB competition cap and the exact byte count and
SHA-256 recorded when the page was rendered, then copies the bytes —
unchanged — into the output directory (MAKEFUN_OUTPUT_DIR or /output).
Two runs therefore always produce byte-identical output.

Revision note (same session): the size and hash guards were tightened to
fail on any drift at all, so a swapped or truncated entry.png can never
slip through as a silent pass.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 103842
EXPECTED_SHA256 = "1248d428ecb0a1ccfb97982d0a57d9ac961a60ca59c5feba6928086fbfba9275"

PNG_HEADER = b"\x89PNG\r\n\x1a\n"
HARD_CAP = 1048576  # the competition refuses anything above 1 MiB


def run():
    folder = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(folder, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = os.path.join(target_dir, "entry.png")

    with open(source, "rb") as handle:
        payload = handle.read()

    if not payload:
        sys.exit("entry.png is empty")
    if payload[:8] != PNG_HEADER:
        sys.exit("entry.png does not start with the PNG magic bytes")
    if len(payload) > HARD_CAP:
        sys.exit("entry.png is over the 1 MiB cap: %d bytes" % len(payload))
    if len(payload) != EXPECTED_BYTES:
        sys.exit(
            "entry.png size drifted: got %d bytes, expected %d"
            % (len(payload), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png sha256 drifted: got %s" % digest)

    os.makedirs(target_dir, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(payload)

    sys.stderr.write("entry.png copied: %d bytes sha256=%s\n" % (len(payload), digest))


if __name__ == "__main__":
    run()
