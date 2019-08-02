from pyqtgraph.Qt import QtCore, QtGui

class LayerBase(QtCore.QObject):

    def __init__(self, name):
        super(QtCore.QObject, self).__init__()
        self.name = name
        self.viewer = None


    def updateData(self, *args, **kargs):
        raise NotImplementedError("updateData must be implemented")

