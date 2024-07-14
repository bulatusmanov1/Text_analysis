"""
Chunk embedding
"""

import numpy as np
from sentence_transformers import SentenceTransformer

from typing import Literal, List, Tuple, Dict

from .chunk import Chunk

EMBEDDER = SentenceTransformer("/model/")

# How to process the chunk contents.
# - "plain" leaves the content as it.
# - "heading" prepends the current heading.
Mode = Literal["plain", "heading"]
Payload = Dict


def embed(chunks: List[Chunk], mode: Mode) -> List[Tuple[np.array, Payload]]:
    """
    Create a list of embeddings and their payloads from chunks.
    """

    out = []

    for chunk in chunks:
        content = _edit_chunk(chunk, mode)
        embed = EMBEDDER.encode(content)

        payload = {
            "content": chunk["content"],
            "line_start": chunk["line_start"],
            "line_end": chunk["line_end"],
            "page_start": chunk["page_start"],
            "page_end": chunk["page_end"],
            "document": chunk["document"],
        }

        out.append((embed, payload))

    return out


def _edit_chunk(chunk: Chunk, mode: Mode) -> str:
    match mode:
        case "plain":
            return chunk["content"]
        case "heading":
            return f"{chunk['heading']} {chunk['content']}"
