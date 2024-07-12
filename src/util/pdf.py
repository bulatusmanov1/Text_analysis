from pikepdf import Pdf

from typing import Literal


def edit_pdf(path: str, action: Literal["delete", "rotate"], num: int):
    with Pdf.open(path, allow_overwriting_input=True) as pdf:
        match action:
            case "delete":
                del pdf.pages[num]
            case "rotate":
                pdf.pages[num].rotate(90)
        pdf.save()


if __name__ == "__main__":
    import sys

    path = sys.argv[1]
    action = sys.argv[2]
    num = int(sys.argv[3])

    edit_pdf(path, action, num - 1)
