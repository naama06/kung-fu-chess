import sys

from chess_io.board_parser import BoardParser
from controller import Controller


def solve(lines=None):

    if lines is None:
        lines = [
            line.strip()
            for line in sys.stdin.readlines()
            if line.strip()
        ]

    else:
        lines = [
            line.strip()
            for line in lines
            if line.strip()
        ]


    if not lines:
        return "EMPTY_INPUT"


    try:
        board_index = lines.index("Board:")
        commands_index = lines.index("Commands:")

    except ValueError:
        return "ERROR INVALID_FORMAT"



    board_lines = lines[
        board_index + 1 : commands_index
    ]

    commands = lines[
        commands_index + 1 :
    ]



    # בדיקות תקינות קלט

    valid_pieces = {
        'K',
        'Q',
        'R',
        'B',
        'N',
        'P'
    }


    expected_width = None


    for row in board_lines:

        tokens = row.split()


        if expected_width is None:
            expected_width = len(tokens)

        elif len(tokens) != expected_width:
            return "ERROR ROW_WIDTH_MISMATCH"



        for token in tokens:

            if token == ".":
                continue


            if len(token) != 2:
                return "ERROR UNKNOWN_TOKEN"


            if token[0] not in {"w", "b"}:
                return "ERROR UNKNOWN_TOKEN"


            if token[1] not in valid_pieces:
                return "ERROR UNKNOWN_TOKEN"



    # יצירת לוח אמיתי עם האובייקטים

    board_text = "\n".join(board_lines)

    board = BoardParser.parse(board_text)


    controller = Controller(board)


    output = []



    for cmd in commands:

        parts = cmd.split()


        if not parts:
            continue



        if parts[0] == "click":

            controller.execute_command(
                "click",
                parts[1:]
            )



        elif parts[0] == "wait":

            controller.execute_command(
                "wait",
                parts[1:]
            )



        elif parts[0] == "jump":

            controller.execute_command(
                "jump",
                parts[1:]
            )



        elif parts[0] == "print":

            if len(parts) == 2 and parts[1] == "board":

                output.append(
                    str(board)
                )



    return "\n".join(output)



if __name__ == "__main__":
    print(solve())