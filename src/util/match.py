def match(test, result) -> int | None:
    """
    Return the distance from the test answers to the result.  Returns None if
    the result is not even on the same page.
    """
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
