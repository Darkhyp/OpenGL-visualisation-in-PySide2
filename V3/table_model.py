from PySide2 import QtCore

from TableModel.cell import Cell


class TableModel(QtCore.QAbstractTableModel):
    """
    class for Table data
    """
    row_count = None
    column_count = None
    header_labels = []

    def __init__(self, data, application=None, n_gons=4):
        QtCore.QAbstractTableModel.__init__(self, application)

        self.application = application
        self._data = data
        self.n_gons = n_gons
        self.init_data()

    def init_data(self):
        self.row_count, self.column_count = self._data.shape
        self.header_labels = self._data.columns

    def set_new_data(self, data):
        self.layoutAboutToBeChanged.emit()
        self._data = data
        self.init_data()
        self.layoutChanged.emit()

    def data(self, index, role):
        if role == QtCore.Qt.UserRole:
            return Cell(self._data.iloc[index.row(), index.column()], index.row(), index.column(), self.n_gons)

    def rowCount(self, index):
        return self.row_count

    def columnCount(self, index):
        return self.column_count

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            row, column = index.row(), index.column()
            try:
                self._data.iloc[row, column] = type(self._data.iloc[row, column])(value)
                if self.application is not None:
                    self.application.cell_updated(row, column)
            except ValueError:
                return False
            return True
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        # return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.header_labels[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)
