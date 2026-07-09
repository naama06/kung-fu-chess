# Git Repository: https://github.com/naama06/kung-fu-chess
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

    valid_pieces = {'K', 'Q', 'R', 'B', 'N', 'P'}
    expected_width = None
    
    # בניית הלוח כמטריצה של איברים (רשימה של רשימות)
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
            if len(token) != 2 or token[0] not in {'w', 'b'} or token[1] not in valid_pieces:
                return "ERROR UNKNOWN_TOKEN"
        board.append(tokens)

    num_rows = len(board)
    num_cols = expected_width if expected_width is not None else 0

    # משתנה שיזכור את מיקום הכלי שנבחר כרגע (row, col)
    selected = None
    output = []

    # מעבר על הפקודות
    for cmd in commands:
        parts = cmd.split()
        if not parts:
            continue
            
        action = parts[0]

        if action == "print" and " ".join(parts) == "print board":
            # הדפסת המצב הנוכחי של הלוח
            for row in board:
                output.append(" ".join(row))
                
        elif action == "wait":
            # באיטרציה זו רק קוראים את הזמן ולא עושים איתו דבר
            continue
            
        elif action == "click":
            if len(parts) != 3:
                continue
            try:
                x = int(parts[1])
                y = int(parts[2])
            except ValueError:
                continue

            # המרה מפיקסלים לאינדקסים של מטריצה
            c = x // 100
            r = y // 100

            # בדיקה אם הקליק מחוץ לגבולות הלוח (אם כן - מתעלמים)
            if r < 0 or r >= num_rows or c < 0 or c >= num_cols:
                continue

            clicked_token = board[r][c]

            if selected is None:
                # אם שום כלי לא נבחר, וקליק על משבצת שאינה ריקה -> נבחר הכלי
                if clicked_token != '.':
                    selected = (r, c)
            else:
                # יש כבר כלי נבחר
                sel_r, sel_c = selected
                selected_token = board[sel_r][sel_c]

                if clicked_token != '.' and clicked_token[0] == selected_token[0]:
                    # קליק על כלי חבר (אותו צבע) -> החלפת הבחירה
                    selected = (r, c)
                else:
                    # פקודת תנועה חוקית לאיטרציה זו (למשבצת ריקה או כלי יריב)
                    board[r][c] = selected_token  # הכלי עובר למשבצת החדשה
                    board[sel_r][sel_c] = '.'     # המשבצת הישנה מתרוקנת
                    selected = None               # איפוס הבחירה

    return "\n".join(output)
if __name__ == "__main__":
    print(solve())