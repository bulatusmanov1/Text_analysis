from typing import List
import json

from . import md, sentence, chunk, embed, qdrant
from chunk import Mode as ChunkMode
from embed import Mode as EmbedMode


def pipeline(
    docs: List[int],
    chunk_mode: ChunkMode,
    embed_mode: EmbedMode,
):
    collection_id = f"{chunk_mode}+{embed_mode}"
    qdrant.create_collection(collection=collection_id)

    for doc in docs:
        with open(f"data/md/{doc}.md", "r") as file:
            content = file.read()
        pages = json.loads(content)

        for page in pages:
            _process_page(page, page_idx, doc, chunk_mode, embed_mode)


def _process_page(
    page: str,
    page_idx: int,
    doc: int,
    chunk_mode: ChunkMode,
    embed_mode: EmbedMode,
) -> None:
    ast = md.ast(page, page=page_idx, document=doc)
    sentences = sentence.sentences(ast)
    chunks = chunk.chunk(sentences, chunk_mode)
    embeds = embed.embed(chunks, embed_mode)

    qdrant.insert(embeds)
