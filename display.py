import json
import sys

with open(f"data/md/{sys.argv[1]}.json", "r") as file:
    content = file.read()
pages = json.loads(content)

for i, page in enumerate(pages):
    for j, line in enumerate(page.splitlines()):
        print(f"{i: <2} {j: <2}\t{line}")
    print("_" * 80)

sys.exit()
