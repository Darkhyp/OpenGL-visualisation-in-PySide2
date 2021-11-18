from PySide2.QtWidgets import QApplication

from V3.SETUP import DATAFRAME0
from V3.main_window import Window
from V3.data import Data


class Application(QApplication):
    """
    class for main application
    """
    # number of angles in polygons (realized for triangles and quads only)
    n_angles = 4

    def __init__(self, argv=[]):
        super(Application, self).__init__(argv)

        # create the instance of data container
        self._data = Data(DATAFRAME0)

        # create the instance of main Window
        self.window = Window(self)

    def model_info(self):
        # get model info (nuber of rows, columns and column headers in data frame)
        row_count, column_count = self._data.shape
        header_labels = self._data.columns

        return row_count, column_count, header_labels

    @property
    def data(self):
        return self._data

    def get_data(self, row, column):
        return self._data.get_data(row, column)

    def set_data(self, row, column, value):
        is_passed = self._data.set_data(row, column, value)
        self.cell_updated(row, column)
        return is_passed

    def cell_updated(self, row, column):
        self.window.cell_updated(row, column)

    def run(self):
        # showing all the widgets
        self.window.show()
        return self.exec_()

    def new_data(self):
        # create new data
        self._data.new()

        # update view
        self.window.update_data(self._data)

    def load_data(self):
        # load data
        self._data.load()

        # update view
        self.window.update_data(self._data)

    def save_data(self):
        # save data
        self._data.save()

    def delete_line_in_data(self):
        # delete selected line in data
        selected_rows = set([i.row() for i in self.window.view.selectedIndexes()])

        if self._data.delete_line(selected_rows):
            self.window.view.clearSelection()

        # update view
        self.window.update_data(self._data)

    def add_new_line_to_data(self):
        # append one line to data
        self._data.add_new_line()

        # update view
        self.window.update_data(self._data)
