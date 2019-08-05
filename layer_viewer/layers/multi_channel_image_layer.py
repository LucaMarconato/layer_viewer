import pyqtgraph as pg

from .layer_base import LayerBase
from .layer_controller import *


class MultiChannelImageLayer(LayerBase):
    class CtrlWidget(LayerItemWidget):
        def __init__(self, name):
            super().__init__(name=name, add_gradient_widgtet=True, channel_selector=True)

            self.asRgb = QtGui.QCheckBox()
            self.asRgb.setToolTip("Show As RGB")
            self._layout.addWidget(self.asRgb, 3, 0)

    def __init__(self, name, data=None, auto_levels=True, levels=None, auto_histogram_range=False, cmap=None):
        super().__init__(name=name)

        self.current_channel = 0
        self.as_rgb = False
        self.m_data = data
        self.m_autoLevels = auto_levels
        self.m_levels = levels
        self.m_autoHistogramRange = auto_histogram_range
        self.m_image_item = pg.ImageItem()
        if self.m_data is not None:
            self.m_image_item.setImage(self.m_data[..., self.current_channel], autoLevels=self.m_autoLevels,
                                       levels=self.m_levels)

        self.m_ctrl_widget = MultiChannelImageLayer.CtrlWidget(name=self.name)
        self.viewer = None

        self.cmap = cmap
        if self.cmap is not None:
            self.m_ctrl_widget.gradientWidget.load_preset(self.cmap)

        # setup ctrl widget
        w = self.m_ctrl_widget
        if self.m_data is not None:
            w.channelSelector.setRange(0, self.m_data.shape[2] - 1)
        w.toggle_eye.setActive(True)
        self.update_rgb_enabled()

        def toggle_eye_changed(state):
            if self.viewer.m_exclusive_layer is not None:
                self.viewer.m_exclusive_layer.setVisible(True)
                self.viewer.m_exclusive_layer = None
            if state == 2:
                self.viewer.show_and_hide_others(self.name)
            else:
                self.setVisible(bool(state))

        w.toggle_eye.stateChanged.connect(toggle_eye_changed)

        def channel_changed(channel):
            if not self.as_rgb:
                self.current_channel = channel
                if self.m_data is not None:
                    self.m_image_item.setImage(self.m_data[..., self.current_channel], autoLevels=self.m_autoLevels,
                                               levels=self.m_levels, autoHistogramRange=self.m_autoHistogramRange)

        w.channelSelector.valueChanged.connect(channel_changed)

        def as_rgb_changed(as_rgb):
            self.as_rgb = bool(as_rgb)
            self.m_ctrl_widget.channelSelector.setEnabled(not self.as_rgb)
            self.m_ctrl_widget.gradientWidget.setEnabled(not self.as_rgb)
            if self.as_rgb:
                self.m_image_item.setLookupTable(None)
                self.m_image_item.setImage(self.m_data, autoLevels=self.m_autoLevels,
                                           levels=self.m_levels, autoHistogramRange=self.m_autoHistogramRange)
            else:
                lut = w.gradientWidget.getLookupTable(512)
                self.m_image_item.setLookupTable(lut)
                self.m_image_item.setImage(self.m_data[..., self.current_channel], autoLevels=self.m_autoLevels,
                                           levels=self.m_levels, autoHistogramRange=self.m_autoHistogramRange)

        w.asRgb.stateChanged.connect(as_rgb_changed)

        w.bar.fractionChanged.connect(self.setOpacity)

        def update():
            lut = w.gradientWidget.getLookupTable(512)
            self.m_image_item.setLookupTable(lut)

        w.gradientWidget.sigGradientChanged.connect(update)
        w.layer = self

    def ctrl_widget(self):
        return self.m_ctrl_widget

    def get_image_item(self):
        return self.m_image_item

    def setOpacity(self, opacity):
        self.m_ctrl_widget.setFraction(opacity)
        self.m_image_item.setOpacity(opacity)

    def setVisible(self, visible):
        self.m_ctrl_widget.toggle_eye.setState(visible)
        self.m_image_item.setVisible(visible)

    def setZValue(self, z):
        self.m_image_item.setZValue(z)

    def update_data(self, image):
        self.m_data = image
        self.m_ctrl_widget.channelSelector.setRange(0, self.m_data.shape[2] - 1)
        self.m_image_item.updateImage(image[..., self.current_channel])
        self.update_rgb_enabled()

    def setData(self, image):
        self.m_data = image

        if image is None:
            self.m_image_item.clear()
            # self.m_image_item.setImage(None, autoLevels=self.m_autoLevels, 
            #         levels=self.m_levels, autoHistogramRange=self.m_autoHistogramRange)
        else:
            self.m_ctrl_widget.channelSelector.setRange(0, self.m_data.shape[2] - 1)

            if self.as_rgb:
                self.m_image_item.setImage(image, autoLevels=self.m_autoLevels,
                                           levels=self.m_levels, autoHistogramRange=self.m_autoHistogramRange)
            else:
                self.m_image_item.setImage(image[..., self.current_channel], autoLevels=self.m_autoLevels,
                                           levels=self.m_levels, autoHistogramRange=self.m_autoHistogramRange)
        self.update_rgb_enabled()

    def update_rgb_enabled(self):
        if len(self.m_data.shape) == 3 and self.m_data.shape[2] > 4:
            self.m_ctrl_widget.asRgb.setEnabled(False)
        else:
            self.m_ctrl_widget.asRgb.setEnabled(True)
