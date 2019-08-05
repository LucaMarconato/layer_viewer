from pyqtgraph.Qt import QtCore


class LayerBase(QtCore.QObject):

    def __init__(self, name):
        super(QtCore.QObject, self).__init__()
        self.name = name
        self.viewer = None

    def update_data(self, *args, **kargs):
        raise NotImplementedError("update_data must be implemented")
