from PySide2.QtWidgets import QPushButton, QMainWindow

from TableModel.SETUP import EMPTY_DATAFRAME, NEW_ROW, XLS_FILE_NAME, XLS_SHEET_NAME
from TableModel.view import View
from TableModel.table_model import TableModel
import pandas as pd


class Window(QMainWindow):
    """
    class for main window
    """
    xls_file_name = XLS_FILE_NAME
    sheet_name = XLS_SHEET_NAME

    def __init__(self, data):
        super().__init__()
        self._data = data

        # setting geometry
        self.setGeometry(100, 100, 500, 400)

        # setting title
        self.setWindowTitle("Pandas dataframe visualisation")

        self.table_model = TableModel(self._data, self)
        self.view = View(self.table_model, self, size=(480, 290))
        self.view.setGeometry(10, 10, 480, 290)

        # creating a push buttons

        button_new = QPushButton("New", self)
        # setting geometry of button
        button_new.setGeometry(10, 320, 100, 70)
        # adding action to a button
        button_new.clicked.connect(self.new_data)

        button_load = QPushButton("Load", self)
        # setting geometry of button
        button_load.setGeometry(120, 320, 100, 70)
        # adding action to a button
        button_load.clicked.connect(self.load_xls)

        button_save = QPushButton("Save", self)
        # setting geometry of button
        button_save.setGeometry(230, 320, 100, 70)
        # adding action to a button
        button_save.clicked.connect(self.save_xls)

        button_delete_line = QPushButton("Delete current line", self)
        # setting geometry of button
        button_delete_line.setGeometry(340, 320, 150, 30)
        # adding action to a button
        button_delete_line.clicked.connect(self.delete_line)

        button_add_line = QPushButton("Add new line", self)
        # setting geometry of button
        button_add_line.setGeometry(340, 360, 150, 30)
        # adding action to a button
        button_add_line.clicked.connect(self.add_new_line)

    # action methods
    def new_data(self):
        print("new data")

        # créer un nouveau DataFrame
        self._data = EMPTY_DATAFRAME

        # update table model
        self.update_df()
        self.view.resizeColumnsToContents()

    def load_xls(self):
        print("load xls")

        # open xls file
        xls_file = pd.ExcelFile(self.xls_file_name)
        # extract the needed sheet from loaded xls-file
        self._data = xls_file.parse(self.sheet_name)

        # update table model
        self.update_df()
        self.view.resizeColumnsToContents()

    def save_xls(self):
        print("save xls")

        # enregistrer les données dans un fichier Excel
        fxls_out = pd.ExcelWriter(self.xls_file_name, engine='openpyxl')
        self._data.to_excel(fxls_out, sheet_name=self.sheet_name, index=False)
        fxls_out.save()
        fxls_out.close()

    def delete_line(self):
        print("delete line(s)")

        selected_rows = set([self._data.index[i.row()] for i in self.view.selectedIndexes()])

        # check if there are selected rows
        if len(selected_rows):
            # delete selected rows
            try:
                self._data = self._data.drop(labels=selected_rows, axis=0)

                # update table model
                self.update_df()
            except Exception as e:
                print(e)
            self.view.resizeColumnsToContents()
        else:
            print('there are no selected lines')

    def add_new_line(self):
        print("add new line")

        self._data = self._data.append(NEW_ROW, ignore_index=True)

        # update table model
        self.update_df()
        self.view.resizeRowsToContents()
        self.view.resizeColumnsToContents()

    def update_df(self):
        # update data (pandas dataframe) in table_model
        self.table_model.set_new_data(self._data)

    def cell_updated(self, row, column):
        self.view.cell_updated(row, column)
