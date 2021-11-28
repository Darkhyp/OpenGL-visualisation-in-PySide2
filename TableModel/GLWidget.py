import sys

import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets, QtOpenGL

from TableModel.SETUP2 import TRIANGLES, QUADS

try:
    from OpenGL import GL
except ImportError:
    app = QtWidgets.QApplication(sys.argv)
    messageBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "OpenGL hellogl",
                                       "PyOpenGL must be installed to run this example.",
                                       QtWidgets.QMessageBox.Close)
    messageBox.setDetailedText("Run:\npip install PyOpenGL PyOpenGL_accelerate")
    messageBox.exec_()
    sys.exit(1)


def normalizeAngle(angle):
    while angle < 0:
        angle += 360 * 16
    while angle > 360 * 16:
        angle -= 360 * 16
    return angle


class GLWidget(QtOpenGL.QGLWidget):
    xRotationChanged = QtCore.Signal(int)
    yRotationChanged = QtCore.Signal(int)
    zRotationChanged = QtCore.Signal(int)
    scaleChanged = QtCore.Signal(int)
    # meshType = TRIANGLES
    meshType = QUADS

    def __init__(self, data, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        self._data = data._data

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.scale = 0.2

        self.lastPos = QtCore.QPoint()

        self.backgroundColor = QtGui.QColor.fromRgbF(0, 0.5, 0.4, 0.0)

    def xRotation(self):
        return self.xRot

    def yRotation(self):
        return self.yRot

    def zRotation(self):
        return self.zRot

    def getScale(self):
        return int(self.scale*100)

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def setXRotation(self, angle):
        angle = normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.updateGL()

    def setYRotation(self, angle):
        angle = normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.updateGL()

    def setZRotation(self, angle):
        angle = normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.updateGL()

    def setScale(self, scale):
        fscale = float(scale)/100
        if fscale != self.scale:
            self.scale = fscale
            self.emit(QtCore.SIGNAL("scaleChanged(int)"), scale)
            self.object = self.makeObject()
            self.updateGL()

    def initializeGL(self):
        self.qglClearColor(self.backgroundColor.darker())
        self.object = self.makeObject()
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, -10.0)
        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        GL.glCallList(self.object)

    def resizeGL(self, width, height):
        side = min(width, height)
        GL.glViewport(int((width - side) / 2), int((height - side) / 2), side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-0.5, +0.5, -0.5, +0.5, 4.0, 15.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = QtCore.QPoint(event.pos())

    def set_new_data(self, data):
        self._data = data
        self.object = self.makeObject()
        self.updateGL()

    def change_mesh_type(self, state):
        if state:
            self.meshType = TRIANGLES
        else:
            self.meshType = QUADS
        self.object = self.makeObject()
        self.updateGL()

    def makeObject(self):
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)

        values = np.array(self._data, dtype=np.float32)

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glVertexPointer(3, GL.GL_FLOAT, 0, self.scale*values[:, :3])
        GL.glEnableClientState(GL.GL_COLOR_ARRAY)
        GL.glColorPointer(4, GL.GL_FLOAT, 0, values[:, 3:7])
        # GL.glNormalPointer(3, GL.GL_FLOAT, 0, values[:, 7:10])
        if self.meshType == TRIANGLES:
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, values.shape[0])
        elif self.meshType == QUADS:
            GL.glDrawArrays(GL.GL_QUADS, 0, values.shape[0])
        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        GL.glDisableClientState(GL.GL_COLOR_ARRAY)

        GL.glEndList()

        return genList

    def makeObject_old(self):
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)

        # old style (start openGL)
        GL.glBegin(GL.GL_QUADS)

        values = self._data.values

        for v in values:
            GL.glVertex3d(*(self.scale*v[:3]))
            GL.glColor3d(*v[3:6])

        # old style (end of openGL)
        GL.glEnd()
        GL.glEndList()

        return genList

    def freeResources(self):
        self.makeCurrent()
        GL.glDeleteLists(self.object, 1)

