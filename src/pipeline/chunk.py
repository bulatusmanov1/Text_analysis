"""
Semantic sentence chunking
"""

from typing import List, Literal, Dict

from .sentence import Sentence

Mode = Literal["size-256", "size-512", "paragraph"]
Chunk = Dict


def chunk(sentences: List[Sentence], mode: Mode) -> List[Chunk]:
    match mode:
        case "size-256":
            return _chunk_size(sentences, size=256)
        case "size-512":
            return _chunk_size(sentences, size=512)
        case "paragraph":
            return _chunk_paragraphs(sentences)


def _chunk_paragraphs(sentences: List[Sentence]) -> List[Chunk]:
    out = []

    heading = ""
    line_start = 0
    page_start = 0
    line_end = 0
    page_end = 0
    content = ""

    line = 0

    for sentence in sentences:
        if "heading" in sentence:
            heading = sentence["heading"]

        if sentence["line"] - line <= 1:
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
            page_start = sentence["page"]
            line_start = sentence["line"]

        line = sentence["line"]

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
