"""
Module for converting PDF files into a Markdown AST-like structure.
"""

from typing import List, Dict

AST = Dict


def convert(md: str) -> List[AST]:
    """
    Takes a path to a PDF file and returns an AST of it's Markdown conversion
    """

    out = []

    par = ""
    for (i, line) in enumerate(md.splitlines() + [""]):
        if line.startswith("#") or line == "":
            if par != "":
                out.append(
                    {
                        "type": "paragraph",
                        "content": par,
                        "line": i,
                    }
                )

        if line.startswith("#"):
            out.append(
                {
                    "type": "heading",
                    "content": line.strip(" #"),
                    "line": i,
                }
            )
            continue

        par += line

    return out
