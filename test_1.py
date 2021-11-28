from PySide2 import QtWidgets, QtCore, QtGui


class ItemDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        editor.setValidator(QtGui.QIntValidator())
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model()._data[index.row()][index.column()])
        editor.setText(value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            try:
                value = int(value)
            except ValueError:
                return False
            self._data[index.row()][index.column()] = value
            return True
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        data = [
            [1, 2],
            [3, 4],
            [5, 6],
        ]

        self.model = TableModel(data)

        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.table.setItemDelegate(ItemDelegate(self))

        self.setCentralWidget(self.table)


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    win = MainWindow()
    win.show()
    app.exec_()
