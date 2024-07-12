import spacy

from typing import Literal, List, Dict

from .md import AST

NLP = spacy.load("ru_core_news_sm")

Sentence = Dict


def _split_into_sentences(text: str) -> List[str]:
    return [sent.text.strip() for sent in NLP(text).sents]


def sentences(ast: List[AST]) -> List[Sentence]:
    out = []

    heading_top = ""
    heading_curr = ""

    for el in ast:
        match el["type"]:
            case "heading":
                if el["level"] == 1:
                    heading_top = el["content"]
                heading_curr = el["content"]

                out.append(
                    {
                        "content": el["content"],
                        "heading": heading_curr,
                        "heading_top": heading_top,
                    }
                )

            case "paragraph":
                sentences = _split_into_sentences(el["content"])

                for sentence in sentences:
                    out.append(
                        {
                            "content": sentence,
                            "heading": heading_curr,
                            "heading_top": heading_top,
                        }
                    )

    return out
