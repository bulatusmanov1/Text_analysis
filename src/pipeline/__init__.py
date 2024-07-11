from . import convert, sentence, chunk, embed, qdrant
from sentence import Mode as SentenceMode
from chunk import Mode as ChunkMode
from embed import Model as EmbedModel, EditMode as EmbedEditMode


def pipeline(
    num: int,
    dir: str,
    sentence_mode: SentenceMode,
    chunk_mode: ChunkMode,
    embed_model: EmbedModel,
    embed_edit_mode: EmbedEditMode,
):
    id = f"{sentence_mode}+{chunk_mode}+{embed_model}+{embed_edit_mode}"

    for i in range(1, num):
        path = f"{dir}{_filename(i)}"

        ast = convert.convert(path)
        sentences = sentence.sentences(ast, sentence_mode)
        chunks = chunk.chunk(sentences, chunk_mode)
        embeds = embed.embed(chunk, embed_model, embed_edit_mode)

        qdrant.creating_collection(collection_name=id)


def _filename(index: int, extension: str = "pdf") -> str:
    return f"{str(index):0>3}.{extension}"
