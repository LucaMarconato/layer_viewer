from  . layer_base import LayerBase
from .. widgets import TrippleToggleEye, ToggleEye, FractionSelectionBar
from .. pixel_path import *
from . layer_controller import *
import pyqtgraph as pg
import os
from pyqtgraph.Qt import QtCore, QtGui
import numpy

###############################################################################
from builtins import range
#from past.utils import old_div
import warnings
from PyQt5.QtCore import pyqtSignal, Qt, QEvent, QRect, QSize, QTimer, QPoint, QItemSelectionModel
from PyQt5.QtGui import QPainter, QFontMetrics, QFont, QPalette, QMouseEvent, QPixmap
from PyQt5.QtWidgets import QStyledItemDelegate, QWidget, QListView, QStyle, \
                            QLabel, QGridLayout, QSpinBox, QApplication


  

class ObjectLayer(LayerBase):
    def __init__(self, name, data=None, lut=None, lut_size=10000, with_background=True):
        super(ObjectLayer, self).__init__(name=name) 

        if lut is None:
            s4 = (lut_size + with_background) * 4
            lut = numpy.random.randint(low=0, high=255, size=s4)
            lut = lut.reshape([lut_size + with_background, 4])
            lut[:,3] = 255
            if with_background:
                lut[0,3] = 0
            self.lut = lut.astype('int64')

        self.m_data = data
    
        self.m_image_item = pg.ImageItem()
        if self.m_data is not None:

            self.m_image_item.setImage(self._apply_lut(self.m_data), autoLevels=False)




        self.m_ctrl_widget = LayerItemWidget(name=self.name, add_gradient_widgtet=False)
        #self.m_ctrl_widget.setLut(lut)
        self.viewer = None

    def _apply_lut(self, image):
        image = image.astype('int64')
        img = numpy.take(self.lut, image, axis=0, mode='clip').astype('uint8')
        #img = numpy.rollaxis(img,0,3)
        #print("img after lut",img.shape)
        return img

    def ctrl_widget(self):
        #print("ctrl")
        w = self.m_ctrl_widget
        w.toggleEye.setActive(True)

        def toogleEyeChanged(state):
            if self.viewer.m_exlusive_layer is not None:
                self.viewer.m_exlusive_layer.setVisible(True)
                self.viewer.m_exlusive_layer = None
            if state == 2:
                 self.viewer.showAndHideOthers(self.name)
            else:
                self.setVisible(bool(state))
        

        w.toggleEye.stateChanged.connect(toogleEyeChanged)

        w.bar.fractionChanged.connect(self.setOpacity)  

        w.layer = self
        return w

    def get_image_item(self):
        return self.m_image_item

    def setOpacity(self, opacity):
        self.m_ctrl_widget.setFraction(opacity)
        self.m_image_item.setOpacity(opacity)

    def setVisible(self, visible):
        self.m_ctrl_widget.toggleEye.setState(visible)
        self.m_image_item.setVisible(visible)


    def setZValue(self, z):
        self.m_image_item.setZValue(z)

    def updateData(self, image):
        self.m_image_item.updateImage(self._apply_lut(image))

    def setData(self, image):
        self.m_image_item.setImage(self._apply_lut(image),autoLevels=False)
