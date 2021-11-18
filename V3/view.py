from PySide2.QtCore import Qt
from PySide2.QtWidgets import QTableView
from V3.delegate import Delegate


class View(QTableView):
    """
    class for Table visualisation
    """

    def __init__(self, model, parent=None):
        super(View, self).__init__(parent)
        self.model = model

        self.setMouseTracking(True)
        self.setModel(self.model)
        self.setItemDelegate(Delegate())
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        # self.resize(*size)

        # change style of table column header
        column_header = self.horizontalHeader()
        stylesheet = """::section{
background-color: lightgray;
color: rgb(0, 55, 155);
                                 }"""
        column_header.setStyleSheet(stylesheet)

        # change style of table row header
        row_header = self.verticalHeader()
        row_header.setStyleSheet(stylesheet)

    def cell_updated(self, row, column):
        self.resizeRowToContents(row)
        self.resizeColumnToContents(column)
