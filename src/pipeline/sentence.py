import spacy

from typing import List, Dict

from .md import AST

NLP = spacy.load("ru_core_news_sm")

Sentence = Dict


def _split_into_sentences(text: str) -> List[str]:
    return [sent.text.strip() for sent in NLP(text).sents]


def sentences(ast: List[AST]) -> List[Sentence]:
    out = []

    heading = ""
    for el in ast:
        match el["type"]:
            case "heading":
                heading = el["content"]

                out.append(
                    {
                        "content": el["content"],
                        "heading": heading,
                        "line": el["line"],
                        "page": el["page"],
                        "document": el["document"],
                    }
                )

            case "line":
                sentences = _split_into_sentences(el["content"])

                for sentence in sentences:
                    out.append(
                        {
                            "content": sentence,
                            "heading": heading,
                            "line": el["line"],
                            "page": el["page"],
                            "document": el["document"],
                        }
                    )

    return out
