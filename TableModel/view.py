from PySide2.QtWidgets import QTableView
from TableModel.delegate import Delegate


class View(QTableView):
    """
    class for Table visualisation
    """

    def __init__(self, model, parent=None, size=(1280, 720)):
        super(View, self).__init__(parent)

        self.setMouseTracking(True)
        self.setModel(model)
        self.setItemDelegate(Delegate())
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.resize(*size)

    def cell_updated(self, row, column):
        self.resizeRowToContents(row)
        self.resizeColumnToContents(column)
