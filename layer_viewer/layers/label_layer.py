from builtins import range

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import pyqtSignal, Qt
# from PyQt5.QtGui import QFontMetrics, QFont
# from PyQt5.QtWidgets import QWidget, QLabel, QSpinBox
# from pyqtgraph.Qt import QtCore

from .layer_base import LayerBase
from ..distinct_colors import *
from ..pixel_path import *
from ..widgets import TripleToggleEye, FractionSelectionBar
from pyqtgraph.Qt import QtCore


class LabelLayer(LayerBase):
    labelsChangedSignal = QtCore.pyqtSignal(object)

    # the gui for the user in the layer stack
    class CtrlWidget(QtWidgets.QWidget):
        def __init__(self, name=None, parent=None, current_label=1, disc_rad=1):
            super(LabelLayer.CtrlWidget, self).__init__(parent=parent)
            # self._layer = None

            self._font = QtGui.QFont(QtGui.QFont().defaultFamily(), 9)
            self._fm = QtGui.QFontMetrics(self._font)
            self.bar = FractionSelectionBar(initial_fraction=1.)
            self.bar.setFixedHeight(10)
            self.name_label = QtGui.QLabel(parent=self)
            self.name_label.setFont(self._font)
            self.name_label.setText(str(name))
            self.opacity_label = QtGui.QLabel(parent=self)
            self.opacity_label.setAlignment(QtCore.Qt.AlignRight)
            self.opacity_label.setFont(self._font)
            self.opacity_label.setText(u"\u03B1=%0.1f%%" % (100.0 * (self.bar.fraction())))

            self.toggle_eye = TripleToggleEye(parent=self)
            self.toggle_eye.setActive(True)
            self.toggle_eye.setFixedWidth(35)
            self.toggle_eye.setToolTip("Visibility")

            self.channel_selector = QtGui.QSpinBox(parent=self)
            self.channel_selector.setFrame(False)
            self.channel_selector.setFont(self._font)
            self.channel_selector.setMaximumWidth(35)
            self.channel_selector.setAlignment(QtCore.Qt.AlignRight)
            self.channel_selector.setToolTip("Channel")
            self.channel_selector.setVisible(False)

            self._layout = QtGui.QGridLayout(self)
            self._layout.addWidget(self.toggle_eye, 0, 0)
            self._layout.addWidget(self.name_label, 0, 1)
            self._layout.addWidget(self.opacity_label, 0, 2)
            self._layout.addWidget(self.channel_selector, 1, 0)

            self._layout.addWidget(self.bar, 1, 1, 1, 2)

            self.label_label = QtGui.QLabel(parent=self)
            self.label_label.setAlignment(QtCore.Qt.AlignRight)
            self.label_label.setFont(self._font)
            self.label_label.setText("Label:")
            self._layout.addWidget(self.label_label, 3, 0, 1, 1)

            self.label_selector = QtGui.QSpinBox(parent=self)
            self.label_selector.setFrame(False)
            self.label_selector.setFont(self._font)
            self.label_selector.setMaximumWidth(35)
            self.label_selector.setAlignment(QtCore.Qt.AlignRight)
            self.label_selector.setToolTip("Label")
            self.label_selector.setVisible(True)
            self.label_selector.setMinimum(0)
            self.label_selector.setMaximum(255)
            self.label_selector.setValue(current_label)
            self._layout.addWidget(self.label_selector, 3, 1, 1, 1)

            self.brush_label = QtGui.QLabel(parent=self)
            self.brush_label.setAlignment(QtCore.Qt.AlignRight)
            self.brush_label.setFont(self._font)
            self.brush_label.setText("Brush:")
            self._layout.addWidget(self.brush_label, 3, 2, 1, 1)

            self.brush_selector = QtGui.QSpinBox(parent=self)
            self.brush_selector.setFrame(False)
            self.brush_selector.setFont(self._font)
            self.brush_selector.setMaximumWidth(35)
            self.brush_selector.setAlignment(QtCore.Qt.AlignRight)
            self.brush_selector.setToolTip("Brush")
            self.brush_selector.setVisible(True)
            self.brush_selector.setMinimum(0)
            self.brush_selector.setMaximum(255)
            self.brush_selector.setValue(disc_rad)
            self._layout.addWidget(self.brush_selector, 3, 3, 1, 1)

            self._layout.setColumnMinimumWidth(2, 35)
            self._layout.setSpacing(0)
            self.setLayout(self._layout)

            def f(frac):
                self.opacity_label.setText(u"\u03B1=%0.1f%%" % (100.0 * (self.bar.fraction())))

            self.bar.fractionChanged.connect(f)

        def setFraction(self, opacity):
            self.bar.set_fraction(opacity)
            self.opacity_label.setText(u"\u03B1=%0.1f%%" % (100.0 * (self.bar.fraction())))

        def get_current_label(self):
            return self.label_selector.value

        def set_num_classes(self, setNumClasses):
            self.label_selector.setRange(0, setNumClasses)

        def set_name(self, name):
            self.name_label.setText(str(name))

        def mousePressEvent(self, ev):
            super(LabelLayer.CtrlWidget, self).mousePressEvent(ev)

    # we need a special image item to handle mouse interaction
    class LabelLayerImageItem(pg.ImageItem):
        def __init__(self, label_layer):
            super(LabelLayer.LabelLayerImageItem, self).__init__()
            self.label_layer = label_layer
            self.m_label_data = label_layer.m_label_data
            self._pixel_path = label_layer._pixel_path

            # otherwise we do not get key events?
            self.setFlag(self.ItemIsFocusable, True)

        def mouseClickEvent(self, ev):
            pass

        def mouseDragEvent(self, ev):
            modifiers = QtGui.QApplication.keyboardModifiers()
            if modifiers != QtCore.Qt.ShiftModifier:

                if ev.isStart():

                    self._pixel_path.clear()
                    self._pixel_path.add(ev.pos())

                elif ev.isFinish():
                    # add the labels
                    self._pixel_path.insert_to_image(label_image=self.m_label_data,
                                                     label=self.label_layer.current_label,
                                                     rad=self.label_layer.disk_rad * [1, 3][
                                                         self.label_layer.current_label == 0]
                                                     )
                    # update image
                    self.setImage(self.m_label_data,
                                  autoLevels=False)
                    self.label_layer.m_temp_path.setPath(QtGui.QPainterPath())

                    # send signal
                    self.label_layer.labelsChangedSignal.emit(self.label_layer)

                else:
                    self._pixel_path.add(ev.pos())
                    self.label_layer.m_temp_path.setPath(self._pixel_path.qpath)

                ev.accept()

        def keyPressEvent(self, event):
            modifiers = QtGui.QApplication.keyboardModifiers()

            for label in range(10):
                if event.key() == getattr(QtCore.Qt, f"Key_{label}"):
                    if modifiers == QtCore.Qt.ControlModifier:
                        self.label_layer.set_current_disk_radius(label)
                    else:
                        self.label_layer.set_current_label(label)
                    event.accept()
                    break
                if event.key() == QtCore.Qt.Key_E:
                    if modifiers != QtCore.Qt.ControlModifier:
                        self.label_layer.set_current_label(0)
                        event.accept()

    # we need a custom graphics item group to handle key interaction
    class MyQGraphicsItemGroup(QtGui.QGraphicsItemGroup):
        keyPressed = QtCore.pyqtSignal(QtCore.QEvent)

        def __init__(self, image_item, temp_path):
            super(LabelLayer.MyQGraphicsItemGroup, self).__init__()
            self.image_item = image_item
            self.temp_path = temp_path
            self.addToGroup(self.image_item)
            self.addToGroup(self.temp_path)

        def keyPressEvent(self, event):
            self.image_item.keyPressEvent(event)

    def __init__(self, name, data=None, lut=None):
        super(LabelLayer, self).__init__(name=name)

        self.lut = get_label_lut()

        self.m_label_data = data

        self.current_label = 1
        self.disk_rad = 1

        # self.m_image_item_group.setHandlesChildEvents

        self.m_ctrl_widget = LabelLayer.CtrlWidget(name=self.name, current_label=self.current_label,
                                                   disc_rad=self.disk_rad)

        self._pixel_path = PixelPath()
        self.m_image_item = LabelLayer.LabelLayerImageItem(label_layer=self)
        self.m_image_item.setLookupTable(self.lut)
        self.m_temp_path = QtGui.QGraphicsPathItem()

        self._set_pen()

        self.m_image_item_group = LabelLayer.MyQGraphicsItemGroup(self.m_image_item, self.m_temp_path)

        if self.m_label_data is not None:
            self.m_image_item.setImage(self.m_label_data, autoLevels=False)

        self.m_image_item_group.addToGroup(self.m_image_item)
        self.m_image_item_group.addToGroup(self.m_temp_path)
        self.disk = disk(self.disk_rad)

        # self.m_ctrl_widget.setLut(lut)
        self.viewer = None

    def _set_pen(self):
        fac = [1, 3][self.current_label == 0]
        if self.current_label == 0:
            color = (0, 0, 0, 255.0 * 0.7)
        else:
            color = self.lut[self.current_label, :]
        p = pg.mkPen(color=color, width=fac * self.disk_rad * 2 + 1, cosmetic=False)
        p.setCapStyle(QtCore.Qt.RoundCap)
        self.m_temp_path.setPen(p)

    def set_num_classes(self, num_classes):
        self.m_ctrl_widget.set_num_classes(num_classes)

    def ctrl_widget(self):
        # print("ctrl")
        w = self.m_ctrl_widget

        # toggle eye
        w.toggle_eye.setActive(True)

        def toogle_eye_changed(state):
            if self.viewer.m_exclusive_layer is not None:
                self.viewer.m_exclusive_layer.setVisible(True)
                self.viewer.m_exclusive_layer = None
            if state == 2:
                self.viewer.show_and_hide_others(self.name)
            else:
                self.setVisible(bool(state))

        w.toggle_eye.stateChanged.connect(toogle_eye_changed)

        # opacity
        w.bar.fractionChanged.connect(self.setOpacity)

        # current label
        def on_label_change(label):
            self.current_label = label
            self._set_pen()

        w.label_selector.valueChanged.connect(on_label_change)

        # current label
        def on_disk_size_change(disk_rad):
            # print('disk_rad', disk_rad)
            self.disk_rad = disk_rad
            self._set_pen()

        w.brush_selector.valueChanged.connect(on_disk_size_change)

        w.layer = self
        return w

    def get_image_item(self):
        return self.m_image_item_group

    def set_current_label(self, label):
        self.current_label = label
        self._set_pen()
        self.m_ctrl_widget.label_selector.setValue(label)

    def set_current_disk_radius(self, rad):
        self.disc_rad = rad
        self._set_pen()
        self.m_ctrl_widget.brush_selector.setValue(rad)

    def setOpacity(self, opacity):
        self.m_ctrl_widget.setFraction(opacity)
        self.m_image_item_group.setOpacity(opacity)

    def setVisible(self, visible):
        self.m_ctrl_widget.toggle_eye.setState(visible)
        self.m_image_item_group.setVisible(visible)

    def setZValue(self, z):
        self.m_image_item_group.setZValue(z)

    def update_data(self, image):
        self.m_label_data = image
        self.m_image_item.m_label_data = self.m_label_data
        self.m_image_item.updateImage((image))

    def setData(self, image):
        self.m_label_data = image
        self.m_image_item.m_label_data = self.m_label_data
        self.m_image_item.setImage((image), autoLevels=False)
