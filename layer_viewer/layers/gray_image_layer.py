from .layer_base import LayerBase
from .layer_controller import *


class GrayImageLayer(LayerBase):
    def __init__(self, name, data=None, auto_levels=True, levels=None, auto_histogram_range=False, cmap=None):
        super(GrayImageLayer, self).__init__(name=name)

        self.m_data = data
        self.m_autoLevels = auto_levels
        self.m_levels = levels
        self.m_autoHistogramRange = auto_histogram_range
        self.m_image_item = pg.ImageItem()
        if self.m_data is not None:
            self.m_image_item.setImage(self.m_data, autoLevels=self.m_autoLevels,
                                       levels=self.m_levels)

        self.m_ctrl_widget = LayerItemWidget(name=self.name, add_gradient_widgtet=True)
        self.viewer = None

        self.cmap = cmap
        if self.cmap is not None:
            self.m_ctrl_widget.gradientWidget.load_preset(self.cmap)

    def ctrl_widget(self):
        w = self.m_ctrl_widget
        w.toggle_eye.setActive(True)

        def toggle_eye_changed(state):
            if self.viewer.m_exclusive_layer is not None:
                self.viewer.m_exclusive_layer.setVisible(True)
                self.viewer.m_exclusive_layer = None
            if state == 2:
                self.viewer.show_and_hide_others(self.name)
            else:
                self.setVisible(bool(state))

        w.toggle_eye.stateChanged.connect(toggle_eye_changed)

        w.bar.fractionChanged.connect(self.setOpacity)

        def update():
            lut = w.gradientWidget.getLookupTable(512)
            self.m_image_item.setLookupTable(lut)

        w.gradientWidget.sigGradientChanged.connect(update)
        w.layer = self
        return w

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
        self.m_image_item.updateImage(image)

    def setData(self, image):
        self.m_image_item.setImage(image, autoLevels=self.m_autoLevels,
                                   levels=self.m_levels, autoHistogramRange=self.m_autoHistogramRange)
