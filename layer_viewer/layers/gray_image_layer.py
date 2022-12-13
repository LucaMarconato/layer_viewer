from .layer_base import LayerBase
from ..widgets import TripleToggleEye, ToggleEye, FractionSelectionBar
from ..pixel_path import *
from .layer_controller import *
import pyqtgraph as pg
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy

###############################################################################
from builtins import range

# from past.utils import old_div
import warnings
from PyQt5.QtCore import (
    pyqtSignal,
    Qt,
    QEvent,
    QRect,
    QSize,
    QTimer,
    QPoint,
    QItemSelectionModel,
)
from PyQt5.QtGui import QPainter, QFontMetrics, QFont, QPalette, QMouseEvent, QPixmap
from PyQt5.QtWidgets import (
    QStyledItemDelegate,
    QWidget,
    QListView,
    QStyle,
    QLabel,
    QGridLayout,
    QSpinBox,
    QApplication,
)


class GrayImageLayer(LayerBase):
    def __init__(
        self,
        name,
        data=None,
        autoLevels=True,
        levels=None,
        autoHistogramRange=False,
        cmap=None,
    ):
        super(GrayImageLayer, self).__init__(name=name)

        self.m_data = data
        self.m_autoLevels = autoLevels
        self.m_levels = levels
        self.m_autoHistogramRange = autoHistogramRange
        self.m_image_item = pg.ImageItem()
        if self.m_data is not None:
            self.m_image_item.setImage(
                self.m_data, autoLevels=self.m_autoLevels, levels=self.m_levels
            )

        self.m_ctrl_widget = LayerItemWidget(name=self.name, add_gradient_widgtet=True)
        self.viewer = None

        self.cmap = cmap
        if self.cmap is not None:
            self.m_ctrl_widget.gradientWidget.loadPreset(self.cmap)

        self.m_ctrl_widgettoggleEye.setActive(True)

        def toogleEyeChanged(state):
            if self.viewer.m_exlusive_layer is not None:
                self.viewer.m_exlusive_layer.setVisible(True)
                self.viewer.m_exlusive_layer = None
            if state == 2:
                self.viewer.showAndHideOthers(self.name)
            else:
                self.setVisible(bool(state))

        self.m_ctrl_widgettoggleEye.stateChanged.connect(toogleEyeChanged)

        self.m_ctrl_widgetbar.fractionChanged.connect(self.setOpacity)

        def update():
            lut = self.m_ctrl_widgetgradientWidget.getLookupTable(512)
            self.m_image_item.setLookupTable(lut)

        self.m_ctrl_widgetgradientWidget.sigGradientChanged.connect(update)
        self.m_ctrl_widgetlayer = self

    def ctrl_widget(self):
        return self.m_ctrl_widget

    def get_image_item(self):
        return self.m_image_item

    def updateData(self, image):
        self.m_data = image
        self.m_image_item.updateImage(image)

    def setData(self, image):
        self.m_image_item.setImage(
            image,
            autoLevels=self.m_autoLevels,
            levels=self.m_levels,
            autoHistogramRange=self.m_autoHistogramRange,
        )
        self.m_data = image
