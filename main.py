#!/usr/bin/env python3
"""Runner for THE DAY'S POST — final3's G4 page for news-image-20261123.

One image tells the whole of Monday 23 November 2026: THE DAY'S POST, a
sepia-and-teal broadsheet with brick-red accents, 41 stories in 12 numbered
cards plus 29 briefs, led by the US Army's plan to detonate tons of unstable
explosives in Iowa. compose.py drew it; this file ships it.

Shipping means copying, nothing more. Only hashlib, os and sys are used.
The runner opens entry.png beside itself, refuses anything that is not a
PNG, anything over the 1 MiB competition ceiling, and anything whose byte
count or SHA-256 differs from the values sealed at render time. It then
writes those exact bytes to MAKEFUN_OUTPUT_DIR (falling back to /output),
so repeated runs can never drift apart.

Tail rewrite note: this entries-repo copy was re-authored from the staging
runner in the same session, keeping the sealed byte count and digest of
THE DAY'S POST page (103842 bytes) as the single source of truth.
"""

import hashlib
import os
import sys

SEALED_BYTES = 103842
SEALED_SHA256 = "1248d428ecb0a1ccfb97982d0a57d9ac961a60ca59c5feba6928086fbfba9275"

SIGNATURE = b"\x89PNG\r\n\x1a\n"
CEILING = 1048576


def ship():
    here = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dst_path = os.path.join(out_dir, "entry.png")

    with open(src_path, "rb") as fh:
        blob = fh.read()

    if len(blob) == 0:
        sys.exit("entry.png is empty — nothing to ship")
    if blob[:8] != SIGNATURE:
        sys.exit("entry.png fails the PNG signature check")
    if len(blob) > CEILING:
        sys.exit("entry.png exceeds 1 MiB: %d bytes" % len(blob))
    if len(blob) != SEALED_BYTES:
        sys.exit("entry.png size mismatch: %d != %d" % (len(blob), SEALED_BYTES))
    if hashlib.sha256(blob).hexdigest() != SEALED_SHA256:
        sys.exit("entry.png sha256 mismatch against the sealed digest")

    os.makedirs(out_dir, exist_ok=True)
    with open(dst_path, "wb") as fh:
        fh.write(blob)
    sys.stderr.write(
        "shipped entry.png: %d bytes sha256=%s\n" % (len(blob), SEALED_SHA256)
    )


if __name__ == "__main__":
    ship()
