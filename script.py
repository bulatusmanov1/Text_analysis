from pprint import pp
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
