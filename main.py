import sys

def solve():
    # קריאת כל השורות מ-Standard Input
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    
    if not lines:
        return

    # 1. מציאת מיקום הלוח והפקודות
    try:
        board_index = lines.index("Board:")
        commands_index = lines.index("Commands:")
    except ValueError:
        # אם המילים "Board:" או "Commands:" לא קיימות בקלט
        return

    # 2. חילוץ שורות הלוח (כל השורות שבין Board ל-Commands)
    board_lines = lines[board_index + 1 : commands_index]
    
    # 3. חילוץ הפקודות (כל השורות שאחרי Commands)
    commands = lines[commands_index + 1 :]

    # רשימת הכלים החוקיים בשחמט (עבור בדיקת UNKNOWN_TOKEN)
    # משבצת ריקה היא '.' והכלים הם המרה של צבע (w/b) וסוג כלי (K, Q, R, B, N, P)
    valid_pieces = {'K', 'Q', 'R', 'B', 'N', 'P'}

    # 4. ולידציה (בדיקות תקינות הלוח)
    expected_width = None
    
    for row in board_lines:
        tokens = row.split()
        
        # בדיקה 1: האם רוחב השורה תואם לשורות הקודמות? (ROW_WIDTH_MISMATCH)
        if expected_width is None:
            expected_width = len(tokens)
        elif len(tokens) != expected_width:
            print("ERROR ROW_WIDTH_MISMATCH")
            return
            
        # בדיקה 2: האם כל האסימונים (tokens) חוקיים? (UNKNOWN_TOKEN)
        for token in tokens:
            if token == '.':
                continue
            # כלי חוקי חייב להיות באורך 2 תווים, להתחיל ב-w או b, והתו השני חייב להיות כלי מוכר
            if len(token) != 2 or token[0] not in {'w', 'b'} or token[1] not in valid_pieces:
                print("ERROR UNKNOWN_TOKEN")
                return

    # 5. ביצוע הפקודות
    for cmd in commands:
        if cmd == "print board":
            for row in board_lines:
                print(row)

if __name__ == "__main__":
    solve()