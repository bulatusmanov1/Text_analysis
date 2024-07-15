from util import qdrant
from pipeline.chunk import Mode as ChunkMode
from pipeline.embed import Mode as EmbedMode


def search(
    query: str, chunk_mode: ChunkMode, embed_mode: EmbedMode, document: int = None
):
    return qdrant.search(
        query, collection=f"{chunk_mode}+{embed_mode}", document=document
    )
