from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from TableModel.SETUP import COUNT_HEIGHT, MIN_WIDTH, PADDING, HEIGHT


class Delegate(QtWidgets.QStyledItemDelegate):
    """
    class for Table visualisation
    """

    def __init__(self, parent=None):
        super(Delegate, self).__init__(parent)

        self.font = QtGui.QFont()
        self.metrics = QtGui.QFontMetrics(self.font)

    def paint(self, painter, option, index):
        cell = index.data(QtCore.Qt.UserRole)
        rect_text = QtCore.QRect(
            option.rect.left(),
            option.rect.top(),
            option.rect.width(),
            option.rect.height() - COUNT_HEIGHT
        )
        rect_count = QtCore.QRect(
            option.rect.left(),
            option.rect.top() + option.rect.height() - COUNT_HEIGHT,
            option.rect.width(),
            COUNT_HEIGHT
        )

        if option.state & QtWidgets.QStyle.State_MouseOver:
            painter.setPen(QtCore.Qt.red)
            painter.setBrush(QtCore.Qt.red)
            painter.drawRect(option.rect)

        if option.state & QtWidgets.QStyle.State_HasFocus:
            painter.setBrush(QtCore.Qt.gray)
            painter.drawRect(option.rect)

        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtCore.Qt.black)
        painter.drawText(
            rect_text,
            QtCore.Qt.AlignCenter,
            cell.text
        )

        painter.setPen(QtCore.Qt.darkGray)
        painter.drawText(
            rect_count,
            QtCore.Qt.AlignCenter,
            cell.print()
        )

    def sizeHint(self, option, index):
        cell = index.data(QtCore.Qt.UserRole)
        width = max(MIN_WIDTH, self.metrics.width(cell.text) + PADDING * 2)
        return QtCore.QSize(width, HEIGHT)

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        # editor.setValidator(QtGui.QIntValidator())
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.UserRole).text
        editor.setText(value)
