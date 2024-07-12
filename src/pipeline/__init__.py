from . import md, sentence, chunk, embed, qdrant
from chunk import Mode as ChunkMode
from embed import Model as EmbedModel, EditMode as EmbedEditMode


def pipeline(
    num: int,
    dir: str,
    chunk_mode: ChunkMode,
    embed_model: EmbedModel,
    embed_edit_mode: EmbedEditMode,
):
    id = f"{sentence_mode}+{chunk_mode}+{embed_model}+{embed_edit_mode}"

    for i in range(1, num):
        path = f"{dir}{_filename(i)}"

        ast = md.convert(path)
        sentences = sentence.sentences(ast)
        chunks = chunk.chunk(sentences, chunk_mode)
        embeds = embed.embed(chunks, embed_model, embed_edit_mode)

        qdrant.creating_collection(collection_name=id)


def _filename(index: int, extension: str = "pdf") -> str:
    return f"{str(index):0>3}.{extension}"
