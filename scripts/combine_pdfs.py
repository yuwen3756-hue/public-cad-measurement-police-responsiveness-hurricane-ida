from __future__ import annotations

import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: combine_pdfs.py MAIN.pdf SUPPLEMENT.pdf OUTPUT.pdf")

    inputs = [Path(sys.argv[1]), Path(sys.argv[2])]
    output = Path(sys.argv[3])
    writer = PdfWriter()
    for path in inputs:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as stream:
        writer.write(stream)


if __name__ == "__main__":
    main()
