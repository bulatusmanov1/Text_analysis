"""
Semantic sentence chunking
"""

from typing import List, Literal, Dict

from .sentence import Sentence

type Mode = Literal["sentence", "section", "window", ]
type Chunk = Dict


def chunk(sentences: List[Sentence], mode: Mode) -> List[Chunk]:
    match mode:
        case "sentence":
            return _chunk_sentences(sentences)
        case "section":
            return _chunk_sections(sentences)


def _chunk_sentences(sentences: List[Sentence]) -> List[Chunk]:
    return sentences


def _chunk_sections(sentences: List[Sentence]) -> List[Chunk]:
    out = []

    heading = None
    heading_top = None
    content = ""

    for sentence in sentences:
        if type(heading) is None:
            heading = sentence["heading"]
            heading_top = sentence["heading_top"]

        if heading == sentence["heading"]:
            content += sentence["heading"]
        else:
            out.append(
                {"content": content, "heading": heading, "heading_top": heading_top}
            )

            heading = sentence["heading"]
            heading_top = sentence["heading_top"]
            content = sentence["heading"]

    return out


def _chunk_window(sentences: List[Sentence]) -> List[Chunk]:
    # TODO
    pass
