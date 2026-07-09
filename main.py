# Git Repository: https://github.com/naama06/kung-fu-chess
import sys

def solve(lines=None):
    # אם לא שלחו לנו שורות מבחוץ (כלומר זה רץ באתר או ידנית), נקרא מהמקלדת
    if lines is None:
        lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    else:
        # אם שלחו לנו שורות מהטסט, רק ננקה רווחים
        lines = [line.strip() for line in lines if line.strip()]

    # אם הקלט ריק לחלוטין, אין מה לעשות
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

    # בדיקות תקינות הלוח
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

    # ביצוע פקודות
    output = []
    for cmd in commands:
        if cmd == "print board":
            for row in board_lines:
                output.append(row)
    
    # מחזירים את התוצאה כטקסט מחובר, כדי שהטסט יוכל לבדוק אותה
    return "\n".join(output)