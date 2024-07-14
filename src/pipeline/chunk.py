"""
Semantic sentence chunking
"""

from scipy.spatial import distance

from typing import List, Literal, Dict

from .sentence import Sentence
from ..util import yapi

Mode = Literal["size-128", "size-256", "section"]
Chunk = Dict


def chunk(sentences: List[Sentence], mode: Mode) -> List[Chunk]:
    match mode:
        case "size-128":
            return _chunk_size(sentences, size=128)
        case "size-256":
            return _chunk_size(sentences, size=256)
        case "section":
            return _chunk_sections(sentences)


def _chunk_sections(sentences: List[Sentence]) -> List[Chunk]:
    out = []

    heading = None
    line_start = 0
    page_start = 0
    line_end = 0
    page_end = 0
    content = ""

    for sentence in sentences:
        if heading is None:
            heading = sentence["heading"]
            line_start = sentence["line"]
            page_start = sentence["page"]

        if heading == sentence["heading"]:
            content += f"{sentence['content']} "
            line_end = sentence["line"]
            page_end = sentence["page"]
        else:
            out.append(
                {
                    "content": content,
                    "heading": heading,
                    "line_start": line_start,
                    "line_end": line_end,
                    "page_start": page_start,
                    "page_end": page_end,
                    "document": sentence["document"],
                }
            )

            heading = sentence["heading"]
            content = sentence["heading"]

    return out


def _chunk_size(sentences: List[Sentence], size: int) -> List[Chunk]:
    out = []

    heading = None
    line_start = 0
    page_start = 0
    line_end = 0
    page_end = 0
    content = ""

    for sentence in sentences:
        if heading is None:
            heading = sentence["heading"]
            line_start = sentence["line"]
            page_start = sentence["page"]

        if len(content) + len(sentence["content"]) < size:
            content += f"{sentence['content']} "
            line_end = sentence["line"]
            page_end = sentence["page"]
        else:
            out.append(
                {
                    "content": content,
                    "heading": heading,
                    "line_start": line_start,
                    "line_end": line_end,
                    "page_start": page_start,
                    "page_end": page_end,
                    "document": sentence["document"],
                }
            )

            heading = sentence["heading"]
            content = sentence["content"]

    # there's an edgecase when the Markdown page doesn't have starting headers
    out = [chunk for chunk in out if chunk["content"] != ""]
    return out
