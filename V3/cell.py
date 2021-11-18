

class Cell:
    """
    class for Cell visualisation
    """
    def __init__(self, value, row, column, n_angles=4):
        self.text = str(value)
        self.count = len(self.text)
        self.row = row
        self.column = column
        self.n_angles = n_angles

    def print(self):
        # print cell string
        if self.column < 3:
            return f"vertex{int(self.row / self.n_angles)}.{'xyz'[self.column]}"
        return f"color{int(self.row / self.n_angles)}.{'RGBA'[self.column - 3]}"

    def __repr__(self):
        return f"<Cell[{self.row},{self.column}]('{self.text}')>"
