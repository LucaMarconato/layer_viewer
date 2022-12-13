from PyQt5 import QtCore, QtGui, QtWidgets


class LayerBase(QtCore.QObject):
    def __init__(self, name):
        super(QtCore.QObject, self).__init__()
        self.name = name
        self.viewer = None

    def updateData(self, *args, **kargs):
        raise NotImplementedError("updateData must be implemented")

    def setOpacity(self, opacity):
        self.ctrl_widget().setFraction(opacity)
        self.get_image_item().setOpacity(opacity)

    def setVisible(self, visible):
        self.ctrl_widget().toggleEye.setState(visible)
        self.get_image_item().setVisible(visible)

    def setZValue(self, z):
        self.get_image_item().setZValue(z)
