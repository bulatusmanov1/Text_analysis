from nltk.tokenize import sent_tokenize
import spacy

from typing import Literal, List, Dict

from .convert import AST

NLP = spacy.load("ru_core_news_sm")

Mode = Literal["period", "spacy", "nltk"]
Sentence = Dict


def _split_into_sentences(text: str, mode: Mode) -> List[str]:
    match mode:
        case "period":
            sentences = text.split(".")
        case "spacy":
            sentences = [sent.text.strip() for sent in NLP(text).sents]
        case "nltk":
            sentences = sent_tokenize(text)
        case _:
            raise Exception("Выберите доступный режим: period, line, spacy, nltk")
    return sentences


def sentences(ast: List[AST], mode: Mode) -> List[Sentence]:
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
                sentences = _split_into_sentences(el["content"], mode)

                for sentence in sentences:
                    out.append(
                        {
                            "content": sentence,
                            "heading": heading_curr,
                            "heading_top": heading_top,
                        }
                    )

    return out
