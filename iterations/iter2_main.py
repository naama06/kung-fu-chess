import sys


def solve(lines=None):
    if lines is None:
        lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    else:
        lines = [line.strip() for line in lines if line.strip()]

    if not lines:
        return "EMPTY_INPUT"

    try:
        board_index = lines.index("Board:")
        commands_index = lines.index("Commands:")
    except ValueError:
        return "ERROR INVALID_FORMAT"

    board_lines = lines[board_index + 1 : commands_index]
    commands = lines[commands_index + 1 :]

    valid_pieces = {"K", "Q", "R", "B", "N", "P"}
    expected_width = None
    board = []

    for row in board_lines:
        tokens = row.split()

        if expected_width is None:
            expected_width = len(tokens)
        elif len(tokens) != expected_width:
            return "ERROR ROW_WIDTH_MISMATCH"

        for token in tokens:
            if token == ".":
                continue

            if (
                len(token) != 2
                or token[0] not in {"w", "b"}
                or token[1] not in valid_pieces
            ):
                return "ERROR UNKNOWN_TOKEN"

        board.append(tokens)

    num_rows = len(board)
    num_cols = expected_width if expected_width is not None else 0
    selected = None
    output = []

    for cmd in commands:
        parts = cmd.split()

        if not parts:
            continue

        action = parts[0]

        if action == "print" and " ".join(parts) == "print board":
            for row in board:
                output.append(" ".join(row))

        elif action == "wait":
            continue

        elif action == "click":
            if len(parts) != 3:
                continue

            try:
                x = int(parts[1])
                y = int(parts[2])
            except ValueError:
                continue

            col = x // 100
            row = y // 100

            if row < 0 or row >= num_rows or col < 0 or col >= num_cols:
                continue

            clicked_token = board[row][col]

            if selected is None:
                if clicked_token != ".":
                    selected = (row, col)
            else:
                sel_row, sel_col = selected
                selected_token = board[sel_row][sel_col]

                if clicked_token != "." and clicked_token[0] == selected_token[0]:
                    selected = (row, col)
                else:
                    board[row][col] = selected_token
                    board[sel_row][sel_col] = "."
                    selected = None

    return "\n".join(output)


if __name__ == "__main__":
    print(solve())
