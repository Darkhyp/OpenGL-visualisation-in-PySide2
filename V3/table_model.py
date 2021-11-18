from PySide2 import QtCore

from V3.cell import Cell


class TableModel(QtCore.QAbstractTableModel):
    """
    class for Table data
    """
    row_count = None
    column_count = None
    header_labels = []

    def __init__(self, application):
        QtCore.QAbstractTableModel.__init__(self, application)

        self.application = application

        self.init_data()

    def init_data(self):
        self.row_count, self.column_count, self.header_labels = self.application.model_info()

    # override method
    def rowCount(self, index):
        return self.row_count

    # override method
    def columnCount(self, index):
        return self.column_count

    def set_new_data(self):
        self.layoutAboutToBeChanged.emit()
        self.init_data()
        self.layoutChanged.emit()

    # override method
    def data(self, index, role):
        if role == QtCore.Qt.UserRole:
            row, column = index.row(), index.column()
            return Cell(self.application.get_data(row, column), row, column, self.application.n_angles)

    # override method
    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            row, column = index.row(), index.column()
            return self.application.set_data(row, column, value)
        return False

    # override method
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        # return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

    # override method
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.header_labels[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)
