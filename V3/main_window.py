from PySide2.QtWidgets import QPushButton, QMainWindow, QCheckBox
from PySide2 import QtCore, QtWidgets

from V3.view import View
from V3.table_model import TableModel
from V3.gl_widget import GLWidget


# class Window(QMainWindow):
class Window(QtWidgets.QWidget):
    """
    class for main window
    """

    def __init__(self, data, application=None):
        # super().__init__()
        super(Window, self).__init__()

        self.application = application
        self._data = data

        # setting title
        self.setWindowTitle("OpenGL visualisation")

        self.table_model = TableModel(self._data._data, self.application)
        self.view = View(self.table_model, self)
        self.view.setFixedWidth(500)

        # creating a push buttons

        button_new = QPushButton("&New", self)
        # adding action to a button
        button_new.clicked.connect(self._data.new)

        button_load = QPushButton("&Load", self)
        # adding action to a button
        button_load.clicked.connect(self._data.load)

        button_save = QPushButton("&Save", self)
        # adding action to a button
        button_save.clicked.connect(self._data.save)

        button_delete_line = QPushButton("&Delete current line", self)
        # adding action to a button
        button_delete_line.clicked.connect(self._data.delete_line)

        button_add_line = QPushButton("&Add new line", self)
        # adding action to a button
        button_add_line.clicked.connect(self._data.add_new_line)

        #  switch between triangular and quadratic mesh
        checkbox = QCheckBox("Use triangular mesh", self)
        checkbox.stateChanged.connect(self.change_mesh_type)
        checkbox.setChecked(False)

        # GL Widget
        self.glWidget = GLWidget(self._data._data, self.application)

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
            slider.setRange(0, 3600)
            slider.setSingleStep(10)
            slider.setPageStep(150)
            slider.setTickInterval(150)
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
    def change_mesh_type(self, state):
        self.glWidget.change_mesh_type(state)
        self.table_model.n_gons = self.glWidget.meshType
        self.table_model.set_new_data(self._data._data)

    # update methods
    def update_data(self, data):
        # update data (pandas dataframe) in table_model
        self.table_model.set_new_data(data)
        self.glWidget.set_new_data(data)
        self.view.resizeColumnsToContents()
        self.view.resizeColumnsToContents()

    def cell_updated(self, row, column):
        self.view.cell_updated(row, column)
        self.update_data(self._data._data)
