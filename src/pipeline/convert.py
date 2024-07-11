"""
Module for converting PDF files into a Markdown AST-like structure.
"""

import pdfminer

from typing import List, Dict

from ..util import yapi


def _extract_pdf(path: str) -> str:
    return open(path, "r").read()


def _llm_convert_to_md(text: str) -> str:
    return yapi.complete(
        text, instruction="Переведи текст в Markdown", max_tokens=2000, model="pro"
    )


def _count_hashes(line: str) -> int:
    out = 0

    for char in line:
        if char == "#":
            out += 1
        else:
            break

    return out


def _to_ast(markdown: str) -> List[Dict]:
    out = []

    par = ""
    for line in markdown.splitlines():
        if line.startswith("#") or line == "":
            out.append(
                {
                    "type": "paragraph",
                    "content": par,
                }
            )

        if line.startswith("#"):
            out.append(
                {
                    "type": "heading",
                    "content": line.strip(" #"),
                    "level": _count_hashes(line),
                }
            )
            continue

        par += line

    # last paragraph
    out.append(
        {
            "type": "paragraph",
            "content": par,
        }
    )

    return out