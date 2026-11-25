# Confess Your Worst Moment — entry program.
# Reads the prepared one-line confession from entry.txt next to this file
# and copies its exact bytes to $MAKEFUN_OUTPUT_DIR/entry.txt.
# The line must stay a single confession inside the 200-character gate.
import os
import sys
from pathlib import Path

MAX_CHARS = 200
SOURCE_NAME = "entry.txt"


def load_confession(source: Path) -> bytes:
    raw = source.read_bytes()
    if not raw:
        raise ValueError(f"{source} is empty: nothing to confess")
    text = raw.decode("utf-8")
    if "\n" in text or "\r" in text:
        raise ValueError("confession must be a single line, no line breaks")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"confession is {len(text)} chars, over the {MAX_CHARS} limit"
        )
    return raw


def main() -> int:
    here = Path(__file__).resolve().parent
    raw = load_confession(here / SOURCE_NAME)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / SOURCE_NAME
    target.write_bytes(raw)
    written = target.read_bytes()
    if written != raw:
        raise RuntimeError("entry.txt on disk differs from the prepared bytes")
    chars = len(raw.decode("utf-8"))
    print(f"wrote {len(raw)} bytes ({chars} chars) to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
