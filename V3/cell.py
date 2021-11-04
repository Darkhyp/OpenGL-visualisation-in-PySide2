

class Cell:
    """
    class for Cell visualisation
    """
    def __init__(self, value, row, column, n_gons=4):
        self.text = str(value)
        self.count = len(self.text)
        self.row = row
        self.column = column
        self.n_gons = n_gons

    def print(self):
        # return f"({self.row},{self.column})"
        if self.column < 3:
            return f"vertex{int(self.row/self.n_gons)}.{'xyz'[self.column]}"
        return f"color{int(self.row/self.n_gons)}.{'RGBA'[self.column-3]}"

    def __repr__(self):
        return f"<Cell[{self.row},{self.column}]('{self.text}')>"
