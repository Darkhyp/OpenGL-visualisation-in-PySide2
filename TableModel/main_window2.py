from PySide2.QtWidgets import QPushButton, QMainWindow, QCheckBox

from TableModel.GLWidget import GLWidget
from TableModel.SETUP2 import EMPTY_DATAFRAME, NEW_ROW, XLS_FILE_NAME, XLS_SHEET_NAME
from TableModel.view import View
from TableModel.table_model import TableModel
import pandas as pd

from PySide2 import QtCore, QtWidgets
from TableModel.GLWidget import GLWidget


# class Window(QMainWindow):
class Window(QtWidgets.QWidget):
    """
    class for main window
    """
    xls_file_name = XLS_FILE_NAME
    sheet_name = XLS_SHEET_NAME

    def __init__(self, data):
        # super().__init__()
        super(Window, self).__init__()

        self._data = data

        # setting title
        self.setWindowTitle("OpenGL visualisation")

        self.table_model = TableModel(self._data, self)
        self.view = View(self.table_model, self, size=(480, 290))

        # creating a push buttons

        button_new = QPushButton("&New", self)
        # adding action to a button
        button_new.clicked.connect(self.new_data)

        button_load = QPushButton("&Load", self)
        # adding action to a button
        button_load.clicked.connect(self.load_xls)

        button_save = QPushButton("&Save", self)
        # adding action to a button
        button_save.clicked.connect(self.save_xls)

        button_delete_line = QPushButton("&Delete current line", self)
        # adding action to a button
        button_delete_line.clicked.connect(self.delete_line)

        button_add_line = QPushButton("&Add new line", self)
        # adding action to a button
        button_add_line.clicked.connect(self.add_new_line)

        #  switch between triangular and quadratic mesh
        checkbox = QCheckBox("Use triangular mesh", self)
        checkbox.stateChanged.connect(self.change_mesh_type)
        checkbox.setChecked(False)

        # GL Widget
        self.glWidget = GLWidget(self._data)

        # sliders for rotations
        self.xSlider = self.createSlider(QtCore.SIGNAL("xRotationChanged(int)"),
                                         self.glWidget.setXRotation)
        self.ySlider = self.createSlider(QtCore.SIGNAL("yRotationChanged(int)"),
                                         self.glWidget.setYRotation)
        self.zSlider = self.createSlider(QtCore.SIGNAL("zRotationChanged(int)"),
                                         self.glWidget.setZRotation)
        # slider for scale
        self.sSlider = self.createSlider(QtCore.SIGNAL("scaleChanged(int)"),
                                         self.glWidget.setScale, stype='float')

        # Make layouts
        mainLayout = QtWidgets.QHBoxLayout()
        Layout1 = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(Layout1)
        Layout2 = QtWidgets.QHBoxLayout()
        Layout1.addWidget(self.view)
        Layout1.addWidget(checkbox)
        Layout1.addLayout(Layout2)
        Layout2.addWidget(button_new)
        Layout2.addWidget(button_load)
        Layout2.addWidget(button_save)
        Layout2.addWidget(button_add_line)
        Layout2.addWidget(button_delete_line)
        mainLayout.addWidget(self.glWidget)
        mainLayout.addWidget(self.xSlider)
        mainLayout.addWidget(self.ySlider)
        mainLayout.addWidget(self.zSlider)
        mainLayout.addWidget(self.sSlider)
        self.setLayout(mainLayout)

        self.xSlider.setValue(190 * 16)
        self.ySlider.setValue(160 * 16)
        self.zSlider.setValue(90 * 16)
        self.sSlider.setValue(20)
        self.xSlider.setToolTip("x-Rotation")
        self.ySlider.setToolTip("y-Rotation")
        self.zSlider.setToolTip("y-Rotation")
        self.sSlider.setToolTip("zoom")

    def createSlider(self, changedSignal, setterSlot, stype='degree'):
        slider = QtWidgets.QSlider(QtCore.Qt.Vertical)

        if stype == 'degree':
            slider.setRange(0, 360 * 16)
            slider.setSingleStep(16)
            slider.setPageStep(15 * 16)
            slider.setTickInterval(15 * 16)
        elif stype == 'float':
            slider.setRange(0, 100)
            slider.setSingleStep(1)
            slider.setPageStep(10)
            slider.setTickInterval(10)

        slider.setTickPosition(QtWidgets.QSlider.TicksRight)

        self.glWidget.connect(slider, QtCore.SIGNAL("valueChanged(int)"), setterSlot)
        self.connect(self.glWidget, changedSignal, slider, QtCore.SLOT("setValue(int)"))

        return slider

    # action methods
    def new_data(self):
        print("new data")

        # créer un nouveau DataFrame
        self._data = EMPTY_DATAFRAME

        # update table model
        self.update_df()
        self.view.resizeColumnsToContents()

    def load_xls(self):
        print(f"load xls ({self.xls_file_name})")

        # open xls file
        xls_file = pd.ExcelFile(self.xls_file_name)
        # extract the needed sheet from loaded xls-file
        self._data = xls_file.parse(self.sheet_name)

        # update table model
        self.update_df()
        self.view.resizeColumnsToContents()

    def save_xls(self):
        print(f"save xls ({self.xls_file_name})")

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

    def change_mesh_type(self, state):
        self.glWidget.change_mesh_type(state)
        self.table_model.n_gons = self.glWidget.meshType
        self.table_model.set_new_data(self._data)

    # update methods
    def update_df(self):
        # update data (pandas dataframe) in table_model
        self.table_model.set_new_data(self._data)
        self.glWidget.set_new_data(self._data)

    def cell_updated(self, row, column):
        self.view.cell_updated(row, column)
        self.glWidget.set_new_data(self._data)
