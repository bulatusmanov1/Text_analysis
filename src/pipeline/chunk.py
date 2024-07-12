"""
Semantic sentence chunking
"""

from scipy.spatial import distance

from typing import List, Literal, Dict

from .sentence import Sentence
from ..util import yapi

Mode = Literal[
    "sentence",
    "section",
    "window",
]
Chunk = Dict


def chunk(sentences: List[Sentence], mode: Mode) -> List[Chunk]:
    match mode:
        case "sentence":
            return _chunk_sentences(sentences)
        case "section":
            return _chunk_sections(sentences)
        case "window":
            return _chunk_window(sentences)


def _chunk_sentences(sentences: List[Sentence]) -> List[Chunk]:
    out = []

    for sentence in sentences:
        out.append(
            {
                "content": sentence["content"],
                "heading": sentence["heading"],
                "line_start": sentence["line"],
                "line_end": sentence["line"],
                "page_start": sentence["page"],
                "page_end": sentence["page"],
            }
        )

    return out


def _chunk_sections(sentences: List[Sentence]) -> List[Chunk]:
    out = []

    heading = None
    line_start = 0
    page_start = 0
    line_end = 0
    page_end = 0
    content = ""

    for sentence in sentences:
        if type(heading) is None:
            heading = sentence["heading"]
            line_start = sentence["line"]
            page_start = sentence["page"]

        if heading == sentence["heading"]:
            content += sentence["heading"]
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
                }
            )

            heading = sentence["heading"]
            content = sentence["heading"]

    return out


def _chunk_window(sentences: List[Sentence], threshold: float = 0.3) -> List[Chunk]:
    out = []

    heading = None
    line_start = 0
    page_start = 0
    line_end = 0
    page_end = 0
    content = ""

    for sentence in sentences:
        if content == "":
            heading = sentence["heading"]
            line_start = sentence["line"]
            page_start = sentence["page_start"]
            content = sentence["content"]

        embed = yapi.embedding(content)
        curr_embed = yapi.embedding(sentence["content"])

        if distance.cosine(embed, curr_embed) > threshold:
            out.append(
                {
                    "content": content,
                    "heading": heading,
                    "line_start": line_start,
                    "line_end": line_end,
                    "page_start": page_start,
                    "page_end": page_end,
                }
            )
        else:
            content += sentence["content"]
            line_end = sentence["line"]
            page_end = sentence["page"]

    return out
