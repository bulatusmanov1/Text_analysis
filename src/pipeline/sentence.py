from nltk.tokenize import sent_tokenize
import spacy

from typing import Literal, List, Dict

NLP = spacy.load("ru_core_news_sm")

type Mode = Literal["period", "line", "spacy", "nltk"]


def _split_into_sentences(text: str, mode: Mode) -> List[str]:
    match mode:
        case "period":
            sentences = text.split(".")
        case "line":
            sentences = text.split("\n")
        case "spacy":
            sentences = [sent.text.strip() for sent in NLP(text).sents]
        case "nltk":
            sentences = sent_tokenize(text)
        case _:
            raise Exception("Выберете доступный режим: period, line, spacy, nltk")
    return sentences


def sentences(ast: List[Dict]) -> List[Dict]:
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
