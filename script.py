import sys
import os
import json
from itertools import product

from src import pipeline
from src.util import qdrant
from src.util.sbert import EMBEDDER


FILES = list(range(0, 81))
CHUNK_MODES = ["size-256", "size-512" "section"]
EMBED_MODES = ["plain", "heading"]

match sys.argv[1]:
    case "print":
        with open(f"/data/md/{sys.argv[2]}.json", "r") as file:
            content = file.read()
        pages = json.loads(content)
        print("\n\n---\n\n".join(pages))
        sys.exit()

    case "init":
        for chunk_mode, embed_mode in product(CHUNK_MODES, EMBED_MODES):
            print(f"Processing '{chunk_mode}+{embed_mode}'")
            pipeline.pipeline(FILES, chunk_mode, embed_mode)

    case "search":
        chunk_mode = os.environ["CHUNK_MODE"]
        embed_mode = os.environ["EMBED_MODE"]

        query = EMBEDDER.encode(sys.argv[2])

        if len(sys.argv) > 3:
            document = int(sys.argv[3])
        else:
            document = None

        points = qdrant.search(
            query,
            limit=10,
            collection=f"{chunk_mode}+{embed_mode}",
            document=document,
        )

        print(qdrant.dump_points(points))

    case "bench":
        pass


def matcher(test, result) -> int | None:
    MIN, MAX = 0, 1000

    distance = None

    for answer in test["answer"]:
        if answer["page"] == result["payload"]["page_start"]:
            line_start = result["payload"]["line_start"]

            if answer["page"] == result["payload"]["page_end"]:
                line_end = result["payload"]["line_end"]
            else:
                line_end = MAX

        elif answer["page"] == result["payload"]["page_end"]:
            line_end = result["payload"]["line_end"]

            if answer["page"] == result["payload"]["page_end"]:
                line_start = result["payload"]["line_start"]
            else:
                line_start = MIN

        else:
            # no match for this answer
            continue

        if line_start <= answer["line"] <= line_end:
            distance = 0
        else:
            distance = min(
                abs(answer["line"] - line_start), abs(answer["line"] - line_end)
            )

    return distance
