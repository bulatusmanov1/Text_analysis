import matplotlib.pyplot as plt
import numpy as np

import json
from itertools import product

CHUNK_MODES = ["size-256", "size-512", "paragraph"]
EMBED_MODES = ["plain", "heading"]

STYLES = [
    "dotted",
    (0, (2, 3)),
    "dashed",
    "dashdot",
    "solid",
    (0, (8, 2)),
]

with open("results.json", "r") as file:
    data = json.load(file)


fig, ax = plt.subplots(figsize=(8, 8))
ax.set_title("Кривая precision-recall")

ax.set_xlabel("Точность (precision)")
ax.set_ylabel("Полнота (recall)")

ax.set_xticks(np.arange(0.5, 1.0, 0.05))
ax.set_yticks(np.arange(0.2, 1.2, 0.2))

ax.set_xlim(0.55, 0.85)
ax.set_ylim(0.2, 0.8)

for i, (chunk_mode, embed_mode) in enumerate(product(CHUNK_MODES, EMBED_MODES)):
    d = data[f"{chunk_mode}+{embed_mode}.json"]
    precision = [test["precision"] for test in d]
    recall = [test["recall"] for test in d]

    ax.plot(
        precision,
        recall,
        linestyle=STYLES[i],
        color = "0.2" if i % 2 == 0 else "0.4",
        label=f"{chunk_mode}, {embed_mode}"
    )

ax.legend()

fig.savefig("test.png")

##################################################################################

MAXS = [
    (0.48, 0.70),
    (0.51, 0.60),
    (0.39, 0.71),
    (0.38, 0.79),
    (0.42, 0.59),
    (0.52, 0.61),
]

fig, ax = plt.subplots(figsize=(8, 8))

ax.set_xlabel("Уровень отсеевания (cutoff)")
ax.set_ylabel("F-мера")

for i, (chunk_mode, embed_mode) in enumerate(product(CHUNK_MODES, EMBED_MODES)):
    d = data[f"{chunk_mode}+{embed_mode}.json"]
    cutoff = [test["cutoff"] for test in d]
    f = [test["f"] for test in d]

    ax.plot(
        cutoff,
        f,
        linestyle=STYLES[i],
        color = "0.2" if i % 2 == 0 else "0.4",
        label=f"{chunk_mode}, {embed_mode}"
    )

ax.scatter([x for x, _ in MAXS], [y for _, y in MAXS], color="black", marker="v")

ax.legend()

fig.savefig("test2.png")
