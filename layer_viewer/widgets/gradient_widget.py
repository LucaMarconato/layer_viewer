import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets


# custom gradient widget with custom sizes
class GradientWidget(pg.GradientWidget):
    def __int__(self, *args, **kwargs):
        super(GradientWidget, self).__init__(*args, **kwargs)
        self.setMaxDim(3)
        self.setMaximumHeight(40)

    def sizeHint(self):
        sh = super(GradientWidget, self).sizeHint()
        new_sh = QtCore.QSize(10, sh.height())
        return new_sh

    def loadPreset(self, name):
        self.item.loadPreset(name)
