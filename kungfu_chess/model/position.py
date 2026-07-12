class Position:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return isinstance(other, Position) and self.row == other.row and self.col == other.col

    def __repr__(self):
        return f"Position({self.row}, {self.col})"
    
    
    #מגדיר "נקודה" על הלוח בעזרת שורה ועמודה, וקובע ששני מיקומים הם זהים אם הערכים שלהם שווים.