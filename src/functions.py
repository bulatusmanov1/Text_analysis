from nltk.tokenize import sent_tokenize
import spacy


def split_into_sentences(text, mode):
    if mode == "points":
        sentences = text.split(".")
    elif mode == "lines":
        sentences = text.split("\n")
    elif mode == "spaCy":
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents]
    elif mode == "nltk":
        sentences = sent_tokenize(text)
    else:
        raise Exception('"Выберете доступный режим: points, lines, spaCy, nltk"')
    return sentences


text = "Вы можете использовать любую модель для распознавания из списка.\n Для примера, воспользуемся моделью page, которая позволяет распознавать любое количество текста на изображении."  # your text
print(split_into_sentences(text, "lines"))
