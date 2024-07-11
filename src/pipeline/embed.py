"""
Chunk embedding
"""

import numpy as np

from typing import Literal, List, Tuple, Dict

from .chunk import Chunk
from ..util import sbert, yapi

Mode = Literal["yandex", "sbert/paraphrase", "sbert/distiluse"]
EditMode = Literal["plain", "heading", "both-headings"]
Payload = Dict


def embed(
    chunks: List[Chunk], mode: Mode, edit_mode: EditMode
) -> List[Tuple[np.array, Payload]]:
    out = []

    for chunk in chunks:
        content = _edit_chunk(chunk, edit_mode)
        embed = None
        match mode:
            case "yandex":
                embed = yapi.embedding(content)
            case "sbert/paraphrase":
                embed = sbert.embed(content, "paraphrase")
            case "sbert/distiluse":
                embed = sbert.embed(content, "distiluse")

        # TODO figure out dict parameters
        out.append((embed, {}))

    return out


def _edit_chunk(chunk: Chunk, mode: EditMode) -> str:
    match mode:
        case "plain":
            return chunk["content"]
        case "heading":
            return f"{chunk['heading']} {chunk['content']}"
        case "both-headings":
            return f"{chunk['heading_top']} {chunk['heading']} {chunk['content']}"
