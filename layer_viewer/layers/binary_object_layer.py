import numpy

from .layer_base import LayerBase
from .layer_controller import *


class BinaryObjectLayer(LayerBase):
    def __init__(self, name, data=None, color=None):
        super(BinaryObjectLayer, self).__init__(name=name)

        if color is None:
            color = numpy.random.randint(low=0, high=255, size=3)

        lut = numpy.zeros([2, 4])
        lut[:, 0:3] = color
        lut[:, 3] = 255
        lut[0, 3] = 0

        self.lut = lut.astype('int64')

        self.m_data = data

        self.m_image_item = pg.ImageItem()
        if self.m_data is not None:
            self.m_image_item.setImage(self._apply_lut(self.m_data), autoLevels=False)

        self.m_ctrl_widget = LayerItemWidget(name=self.name, add_gradient_widgtet=False)
        # self.m_ctrl_widget.setLut(lut)
        self.viewer = None

    def _apply_lut(self, image):
        image = image.astype('int64')
        img = numpy.take(self.lut, image, axis=0, mode='clip').astype('uint8')
        return img

    def ctrl_widget(self):

        w = self.m_ctrl_widget
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

        w.bar.fractionChanged.connect(self.setOpacity)

        w.layer = self
        return w

    def get_image_item(self):
        return self.m_image_item

    def setOpacity(self, opacity):
        self.m_ctrl_widget.setFraction(opacity)
        self.m_image_item_group.setOpacity(opacity)

    def setVisible(self, visible):
        self.m_ctrl_widget.toggle_eye.setState(visible)
        self.m_image_item.setVisible(visible)

    def setZValue(self, z):
        self.m_image_item.setZValue(z)

    def update_data(self, image):
        self.m_data = image
        self.m_image_item.updateImage(self._apply_lut(image))

    def setData(self, image):
        self.m_image_item.setImage(self._apply_lut(image), autoLevels=False)
