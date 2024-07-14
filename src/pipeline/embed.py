"""
Chunk embedding
"""

import numpy as np
import httpx

import asyncio
from typing import Literal, List, Tuple, Dict

from .chunk import Chunk
from ..util import yapi

# How to process the chunk contents.
# - "plain" leaves the content as it.
# - "heading" prepends the current heading.
Mode = Literal["plain", "heading"]
Payload = Dict


def embed(chunks: List[Chunk], mode: Mode) -> List[Tuple[np.array, Payload]]:
    """
    Create a list of embeddings and their payloads from chunks.
    """

    async def a():
        tasks = []

        async with httpx.AsyncClient() as client:
            async with asyncio.TaskGroup() as tg:
                for chunk in chunks:
                    task = tg.create_task(_embed_chunk(chunk, mode))
                    tasks.append(task)

        return tasks

    tasks = asyncio.run(a())
    out = [task.result() for task in tasks]

    return out


async def _embed_chunk(chunk, mode) -> Tuple[np.array, Payload]:
    content = _edit_chunk(chunk, mode)
    embed = yapi.embedding(content)

    payload = {
        "content": chunk["content"],
        "line_start": chunk["line_start"],
        "line_end": chunk["line_end"],
        "page_start": chunk["page_start"],
        "page_end": chunk["page_end"],
        "document": chunk["document"],
    }
    return (embed, payload)


def _edit_chunk(chunk: Chunk, mode: Mode) -> str:
    match mode:
        case "plain":
            return chunk["content"]
        case "heading":
            return f"{chunk['heading']} {chunk['content']}"
