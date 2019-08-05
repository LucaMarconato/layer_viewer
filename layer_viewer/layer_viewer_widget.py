from pyqtgraph.Qt import QtGui
from pyqtgraph.dockarea import *

from .layer_ctrl_widget import LayerCtrlWidget
from .layer_view_widget import LayerViewWidget
from .settings_widget import SettingsWidget


class LayerViewerWidget(QtGui.QWidget):
    def __init__(self, gui_style='splitter', parent=None):
        QtGui.QWidget.__init__(self, parent)

        # for backward compatibility
        self.addLayer = self.add_layer
        self.m_hbox = QtGui.QHBoxLayout()
        self.setLayout(self.m_hbox)

        self.settings_widget = SettingsWidget()
        self.m_layer_view_widget = LayerViewWidget(settings_widget=self.settings_widget)
        self.m_layer_ctrl_widget = LayerCtrlWidget()

        gui_style = 'dock'
        if gui_style == 'dock':
            self.area = DockArea()
            self.m_hbox.addWidget(self.area)
            d_view = Dock("Viewer", size=(500, 500))
            d_ctrl = Dock("Ctrl", size=(200, 500))
            d_view.addWidget(self.m_layer_view_widget)
            d_ctrl.addWidget(self.m_layer_ctrl_widget)
            self.area.addDock(d_view)
            self.area.addDock(d_ctrl, 'right', d_view)

        elif gui_style == 'splitter':
            self.splitter = QtGui.QSplitter()
            self.m_hbox.addWidget(self.splitter)
            self.splitter.addWidget(self.m_layer_view_widget)
            self.splitter.addWidget(self.m_layer_ctrl_widget)

        self.m_layers = dict()

        self.m_exclusive_layer = None

    @property
    def view_box(self):
        return self.m_layer_view_widget.view_box

    # def addLayer(self, layer, opacity=1.0, visible=True):
    #     self.add_layer(layer, opacity, visible)

    def add_layer(self, layer, opacity=1.0, visible=True):
        image_item = layer.get_image_item()
        self.m_layer_ctrl_widget.add_layer(layer)
        self.view_box.addItem(image_item)
        self.m_layers[layer.name] = layer
        self.set_layer_visibility(layer.name, bool(visible))
        self.set_layer_opacity(layer.name, float(opacity))
        layer.viewer = self

    def remove_all_layers(self):
        to_rm = list(self.m_layers.keys())
        for l in to_rm:
            self.remove_layer(l)

    def remove_layer(self, layer_name):
        layer = self.m_layers[layer_name]
        self.view_box.removeItem(layer.get_image_item())
        self.m_layer_ctrl_widget.remove_layer(layer)
        del self.m_layers[layer_name]

    def has_layer(self, layer_name):
        return layer_name in self.m_layers

    def layer_visibility(self, layer_name):
        layer = self.m_layers[layer_name]
        image_item = layer.get_image_item()
        return image_item.isVisible()

    def layer_opacity(self, layer_name):
        layer = self.m_layers[layer_name]
        image_item = layer.get_image_item()
        return image_item.opacity()

    def set_layer_visibility(self, layer_name, visible):
        self.m_layers[layer_name].setVisible(visible)

    def set_layer_opacity(self, layer_name, opacity):
        self.m_layers[layer_name].setOpacity(opacity)

    def update_data(self, layer_name, **kwargs):
        self.m_layers[layer_name].update_data(**kwargs)

    def set_data(self, layer_name, **kwargs):
        self.m_layers[layer_name].set_data(**kwargs)

    def show_and_hide_others(self, layer_name):
        for ln in self.m_layers.keys():
            layer = self.m_layers[ln]
            if ln == layer_name:
                layer.setVisible(2)
                self.m_exclusive_layer = layer
            else:
                layer.setVisible(False)
