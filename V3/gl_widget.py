import sys

import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets, QtOpenGL

from V3.SETUP import QUADS, TRIANGLES

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
    """
    Widget class for OpenGL visualisation
    """

    xRotationChanged = QtCore.Signal(int)
    yRotationChanged = QtCore.Signal(int)
    zRotationChanged = QtCore.Signal(int)
    scaleChanged = QtCore.Signal(int)
    meshType = QUADS

    def __init__(self, data):
        super(GLWidget, self).__init__()

        self._data = data

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

    # override method
    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    # override method
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

    # override method
    def initializeGL(self):
        self.qglClearColor(self.backgroundColor.darker())
        self.object = self.makeObject()
        GL.glEnable(GL.GL_DEPTH_TEST)

    def change_mesh_type(self, state):
        if state:
            self.meshType = TRIANGLES
        else:
            self.meshType = QUADS
        self.object = self.makeObject()
        self.updateGL()

    def change_flatcolor_view(self, state):
        # color is the same for all vertices of the face
        if state:
            GL.glShadeModel(GL.GL_FLAT)
        else:
            GL.glShadeModel(GL.GL_SMOOTH)
        self.updateGL()

    def change_backside_view(self, state):
        # back side of face is invisible
        if state:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)
        self.updateGL()

    def change_alpha_view(self, state):
        # make texture with alpha channel
        if state:
            GL.glEnable(GL.GL_BLEND)
            GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE)
            # GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
            # GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_CONSTANT_ALPHA)
        else:
            GL.glDisable(GL.GL_BLEND)
        self.updateGL()

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, -10.0)
        GL.glRotated(self.xRot / 10.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 10.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 10.0, 0.0, 0.0, 1.0)
        GL.glCallList(self.object)

    # override method
    def resizeGL(self, width, height):
        side = min(width, height)
        GL.glViewport(int((width - side) / 2), int((height - side) / 2), side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-0.5, +0.5, -0.5, +0.5, 4.0, 15.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    # override method
    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    # override method
    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 5 * dy)
            self.setYRotation(self.yRot + 5 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 5 * dy)
            self.setZRotation(self.zRot + 5 * dx)

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

    def makeObject_old(self):
        # old style (with glBegin and glEnd, it is refreshed every frame)
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)

        # old style (start openGL)
        GL.glBegin(GL.GL_QUADS)

        values = self._data.values

        for v in values:
            GL.glVertex3d(*(self.scale*v[:3]))
            GL.glColor4f(*v[3:7])

        # old style (end of openGL)
        GL.glEnd()
        GL.glEndList()

        return genList

    def makeObject(self):
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)

        values = np.array(self._data.values, dtype=np.float32)

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

    # override method
    def freeResources(self):
        self.makeCurrent()
        GL.glDeleteLists(self.object, 1)

