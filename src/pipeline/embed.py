"""
Chunk embedding
"""

import numpy as np

from typing import Literal, List, Tuple, Dict

from .chunk import Chunk
from ..util import yapi

# How to process the chunk contents.
# - "plain" leaves the content as it.
# - "heading" prepends the current heading.
# - "both-headings" prepends both the top level and the current headings
Mode = Literal["plain", "heading", "both-headings"]
Payload = Dict


def embed(chunks: List[Chunk], mode: Mode) -> List[Tuple[np.array, Payload]]:
    """
    Create a list of embeddings and their payloads from chunks.
    """

    out = []

    for chunk in chunks:
        content = _edit_chunk(chunk, edit_mode)
        embed = yapi.embedding(content)

        payload = {
            "line_start": line_start,
            "line_end": line_end,
            "page_start": page_start,
            "page_end": page_end,
        }
        out.append((embed, payload))

    return out


def _edit_chunk(chunk: Chunk, mode: Mode) -> str:
    match mode:
        case "plain":
            return chunk["content"]
        case "heading":
            return f"{chunk['heading']} {chunk['content']}"
        case "both-headings":
            return f"{chunk['heading_top']} {chunk['heading']} {chunk['content']}"
