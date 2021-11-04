from PySide2.QtWidgets import QApplication

from V3.SETUP import DATAFRAME0
from V3.main_window import Window
from V3.data import Data


class Application(QApplication):
    """
    class for main application
    """

    def __init__(self, argv=[]):
        super(Application, self).__init__(argv)

        # create the instance of data container
        self._data = Data(DATAFRAME0, self)

        # create the instance of main Window
        self.window = Window(self._data, self)

    def update_data(self):
        self.window.update_data(self._data._data)

    def cell_updated(self, row, column):
        self.window.cell_updated(row, column)

    def run(self):
        # showing all the widgets
        self.window.show()
        return self.exec_()
