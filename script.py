import sys
import os
import json
from itertools import product

from src import pipeline
from src.util import qdrant
from src.util.sbert import EMBEDDER
from src.util.match import match


FILES = list(range(0, 81))
CHUNK_MODES = ["size-256", "size-512" "paragraph"]
EMBED_MODES = ["plain", "heading"]

match sys.argv[1]:
    case "print":
        with open(f"data/md/{sys.argv[2]}.json", "r") as file:
            content = file.read()
        pages = json.loads(content)

        for i, page in enumerate(pages):
            for j, line in enumerate(page.splitlines()):
                print(f"{i: <2}:{j: <2}:\t{line}")
            print("_" * 80)

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

        print(qdrant.convert_points(points))

    case "bench":
        chunk_mode = os.environ["CHUNK_MODE"]
        embed_mode = os.environ["EMBED_MODE"]

        with open("/data/tests/document.json", "r") as file:
            content = file.read()
            tests = json.loads(content)

        for test in tests:
            query = EMBEDDER.encode(test["question"])
            points = qdrant.search(
                query,
                collection=f"{chunk_mode}+{embed_mode}",
                document=test["document"],
            )
            results = qdrant.convert_points(points)
            # a list of (distance, score) tuples
            results = [(match(test, result), result["score"]) for result in results]
