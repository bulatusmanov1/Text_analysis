"""
Module for converting PDF files into a Markdown AST-like structure.
"""

from typing import List, Dict

AST = Dict


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
    for line in markdown.splitlines() + [""]:
        if line.startswith("#") or line == "":
            if par != "":
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

    return out


def convert(md: str) -> List[AST]:
    """
    Takes a path to a PDF file and returns an AST of it's Markdown conversion
    """

    ast = _to_ast(markdown)

    return ast
