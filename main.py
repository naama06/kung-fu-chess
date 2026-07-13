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

    board_lines = lines[board_index + 1:commands_index]
    commands = lines[commands_index + 1:]

    valid_pieces = {'K', 'Q', 'R', 'B', 'N', 'P'}
    expected_width = None

    board = []
    for row in board_lines:
        tokens = row.split()

        if expected_width is None:
            expected_width = len(tokens)
        elif len(tokens) != expected_width:
            return "ERROR ROW_WIDTH_MISMATCH"

        for token in tokens:
            if token == '.':
                continue

            if len(token) != 2:
                return "ERROR UNKNOWN_TOKEN"

            if token[0] not in {'w', 'b'}:
                return "ERROR UNKNOWN_TOKEN"

            if token[1] not in valid_pieces:
                return "ERROR UNKNOWN_TOKEN"

        board.append(tokens)

    num_rows = len(board)
    num_cols = expected_width if expected_width else 0

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

            c = x // 100
            r = y // 100

            if r < 0 or r >= num_rows or c < 0 or c >= num_cols:
                continue

            clicked_token = board[r][c]

            if selected is None:

                if clicked_token != '.':
                    selected = (r, c)

            else:

                sel_r, sel_c = selected
                selected_token = board[sel_r][sel_c]

                # לחיצה על כלי מאותו צבע = רק החלפת בחירה
                if clicked_token != '.' and clicked_token[0] == selected_token[0]:
                    selected = (r, c)
                    continue

                piece = selected_token[1]
                valid = False

                if piece == 'K':
                    row_diff = abs(sel_r - r)
                    col_diff = abs(sel_c - c)

                    if (row_diff != 0 or col_diff != 0) and row_diff <= 1 and col_diff <= 1:
                        valid = True

                elif piece == 'R':

                    if sel_r == r or sel_c == c:
                        valid = True

                else:
                    # שאר הכלים עדיין לא ממומשים
                    valid = True

                if valid:
                    board[r][c] = selected_token
                    board[sel_r][sel_c] = '.'

                selected = None

    return "\n".join(output)


if __name__ == "__main__":
    print(solve())