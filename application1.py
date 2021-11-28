from PySide2.QtWidgets import QApplication

from TableModel.SETUP import DATAFRAME0
from TableModel.main_window1 import Window


class Application(QApplication):
    """
    class for main application
    """

    def __init__(self, argv=[]):
        super(Application, self).__init__(argv)

        # create the instance of main Window
        self.window = Window(DATAFRAME0)

    def run(self):
        # showing all the widgets
        self.window.show()
        return self.exec_()
