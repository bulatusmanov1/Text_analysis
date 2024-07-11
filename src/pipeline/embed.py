"""
Chunk embedding
"""

import numpy as np

from typing import Literal, List, Tuple, Dict

from .chunk import Chunk
from ..util import sbert, yapi

# Which embedding model to use
Model = Literal["yandex", "sbert/paraphrase", "sbert/distiluse"]
# How to process the chunk contents.
# - "plain" leaves the content as it.
# - "heading" prepends the current heading.
# - "both-headings" prepends both the top level and the current headings
EditMode = Literal["plain", "heading", "both-headings"]
Payload = Dict


def embed(
    chunks: List[Chunk], model: Model, edit_mode: EditMode
) -> List[Tuple[np.array, Payload]]:
    """
    Create a list of embeddings and their payloads from chunks.
    """

    out = []

    for chunk in chunks:
        content = _edit_chunk(chunk, edit_mode)
        embed = None
        match model:
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
