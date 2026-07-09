from main import solve

def test_select_piece_by_center_click():
    test_input = [
        "Board:",
        "wK . .",
        ". . .",
        ". . .",
        "Commands:",
        "click 50 50",
        "click 150 150",
        "wait 1000",
        "print board"
    ]
    result = solve(test_input)
    # תיקון הפורמט המצופה שיתאים בדיוק לשלוש משבצות בשורה הראשונה
    assert result == ". . .\n. wK .\n. . ."

def test_click_empty_cell_does_not_select():
    test_input = [
        "Board:",
        "wK . .",
        ". . .",
        ". . .",
        "Commands:",
        "click 150 150",
        "click 250 250",
        "wait 1000",
        "print board"
    ]
    result = solve(test_input)
    assert result == "wK . .\n. . .\n. . ."

def test_click_outside_board_is_ignored():
    test_input = [
        "Board:",
        "wK . .",
        ". . .",
        ". . .",
        "Commands:",
        "click 350 50",
        "click -10 50",
        "print board"
    ]
    result = solve(test_input)
    assert result == "wK . .\n. . .\n. . ."

def test_clicking_another_piece_replaces_selection():
    test_input = [
        "Board:",
        "wR . wK",
        ". . .",
        "Commands:",
        "click 50 50",
        "click 250 50",
        "click 250 150",
        "wait 1000",
        "print board"
    ]
    result = solve(test_input)
    assert result == "wR . .\n. . wK"

def test_reject_unknown_token():
    test_input = [
        "Board:",
        "wK xZ",
        ". .",
        "Commands:",
        "print board"
    ]
    result = solve(test_input)
    assert result == "ERROR UNKNOWN_TOKEN"

def test_reject_row_width_mismatch():
    test_input = [
        "Board:",
        "wK . .",
        ". bK",
        "Commands:",
        "print board"
    ]
    result = solve(test_input)
    assert result == "ERROR ROW_WIDTH_MISMATCH"