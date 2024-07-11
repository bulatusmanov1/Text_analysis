from src.util import sbert

sentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
]
embed = sbert.embed(sentences[0])

print(type(embed), embed)
