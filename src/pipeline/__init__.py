from . import md, sentence, chunk, embed, qdrant
from chunk import Mode as ChunkMode
from embed import Mode as EmbedMode


def pipeline(
    num: int,
    dir: str,
    chunk_mode: ChunkMode,
    embed_mode: EmbedMode,
):
    id = f"{chunk_mode}+{embed_mode}"

    for i in range(1, num):
        path = f"{dir}{_filename(i)}"

        ast = md.ast(path)
        sentences = sentence.sentences(ast)
        chunks = chunk.chunk(sentences, chunk_mode)
        embeds = embed.embed(chunks, embed_mode)

        qdrant.creating_collection(collection_name=id)


def _filename(index: int, extension: str = "pdf") -> str:
    return f"{str(index):0>3}.{extension}"
