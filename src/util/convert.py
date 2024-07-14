from pikepdf import Pdf

from io import BytesIO
from typing import List
import logging
import sys
import json

from . import yapi

LOGGER = logging.getLogger(__name__)


def to_pdf_pages(path) -> List[bytes]:
    """
    Convert a PDF file to a list of pages encoded in binary
    """

    out = []

    with Pdf.open(path) as pdf:
        for page in pdf.pages:
            dst = Pdf.new()
            dst.pages.append(page)
            binary_page = BytesIO()
            dst.save(binary_page)

            out.append(binary_page.getvalue())
    return out


def to_txt(json) -> str:
    out = ""

    blocks = json["result"]["textAnnotation"]["blocks"]

    for block in blocks:
        text = ""
        for line in block["lines"]:
            text += f"{line['text']} "
        out += f"{text.strip()}\n\n"

    return out.strip()


def to_md(txt: str) -> str:
    return yapi.complete(
        txt,
        instruction="Перепиши текст в  Markdown, не используя блоки кода",
        temperature=0.3,
        model="pro",
        max_tokens=2000,
    )


def to_pages(path: str) -> List[str]:
    pdf_pages = to_pdf_pages(path)
    LOGGER.info(f"Processing {path}")

    out = []
    for i, pdf in enumerate(pdf_pages):
        LOGGER.info(f"\t- page {i+1}")
        json = yapi.ocr(pdf)
        txt = to_txt(json)
        md = to_md(txt)
        out.append(md)

    return out


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    for arg in sys.argv[1:]:
        pages = to_pages(f"/data/pdf/{arg}.pdf")
        open(f"/data/md/{arg}.json", "w").write(json.dumps(pages))
