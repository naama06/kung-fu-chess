# אנחנו מייבאים את הפונקציה solve מתוך קובץ ה-main שלנו!
from main import solve

def test_valid_board_print():
    """טסט שבודק שהדפסת לוח תקין עובדת כמו שצריך"""
    test_input = [
        "Board:",
        "wK .",
        ". bK",
        "Commands:",
        "print board"
    ]
    
    result = solve(test_input)
    
    # המילה assert אומרת: "אני מצפה שמה שכתוב מימין יהיה שווה למה שמשמאל"
    # אם זה נכון - הטסט עובר (ירוק). אם לא - הטסט נכשל (אדום).
    assert result == "wK .\n. bK"


def test_unknown_token_error():
    """טסט שבודק שהמערכת מזהה כלי מזויף ומחזירה שגיאה מתאימה"""
    test_input = [
        "Board:",
        "wK xZ",  # כלי מזויף!
        ". bK",
        "Commands:",
        "print board"
    ]
    
    result = solve(test_input)
    assert result == "ERROR UNKNOWN_TOKEN"


def test_row_width_mismatch_error():
    """טסט שבודק שהמערכת מזהה שורה קצרה או ארוכה מדי"""
    test_input = [
        "Board:",
        "wK . .",
        ". bK",  # שורה קצרה מדי לעומת הראשונה!
        "Commands:",
        "print board"
    ]
    
    result = solve(test_input)
    assert result == "ERROR ROW_WIDTH_MISMATCH"