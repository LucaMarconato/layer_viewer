# from pyqtgraph.Qt import QtGui
from PyQt5 import QtGui
import PyQt5.QtCore as qt
from PyQt5.QtWidgets import QWidget
from pyqtgraph.dockarea import *

from .layer_ctrl_widget import LayerCtrlWidget
from .layer_plot_widget import LayerPlotWidget
from .layer_view_widget import LayerViewWidget
from .settings_widget import SettingsWidget


class LayerViewerWidget(QtGui.QWidget):
    def __init__(self, gui_style='splitter', parent=None):
        QtGui.QWidget.__init__(self, parent)

        # for backward compatibility
        self.addLayer = self.add_layer

        # this is the layout
        # |-------|------|
        # |       | ctrl |
        # | image |------|
        # |       | plot |
        # |-------|------|
        self.m_hbox = QtGui.QHBoxLayout()
        self.m_vhbox = QtGui.QVBoxLayout()
        self.setLayout(self.m_hbox)

        self.settings_widget = SettingsWidget()
        self.m_layer_view_widget = LayerViewWidget(settings_widget=self.settings_widget)
        self.m_layer_ctrl_widget = LayerCtrlWidget()
        self.m_layer_plot_widget = LayerPlotWidget()

        # gui_style = 'dock'
        if gui_style == 'dock':
            self.area = DockArea()
            self.m_hbox.addWidget(self.area)
            d_view = Dock('Viewer', size=(500, 500))
            d_ctrl = Dock('Ctrl', size=(200, 300))
            d_plot = Dock('Plot', size=(200, 200))
            d_view.addWidget(self.m_layer_view_widget)
            d_ctrl.addWidget(self.m_layer_ctrl_widget)
            self.area.addDock(d_view)
            self.area.addDock(d_ctrl, 'right', d_view)

            print('warning: plot dock not yet')
            # self.area.addDock(d_plot, 'below', d_ctrl)

            # self.inner_area = DockArea()
            # self.m_vhbox.addWidget(self.inner_area)
            # self.inner_area.addDock(d_ctrl)
            # self.inner_area.addDock(d_plot)
            # self.outer_area = DockArea()
            # self.m_hbox.addWidget(self.outer_area)
            # d_ctrl = Dock('Ctrl', size=(200, 500))
            # d_view = Dock('Viewer', size=(500, 500))
            # d_view.addWidget(self.m_layer_view_widget)
            # self.outer_area.addDock(d_view)
            # self.outer_area.addDock(d_ctrl, 'right', d_view)
            # self.outer_area.addDock(d_plot, 'below', d_ctrl)

        elif gui_style == 'splitter':
            self.inner_container = QWidget()
            self.inner_container.setLayout(self.m_vhbox)
            self.inner_splitter = QtGui.QSplitter()
            self.inner_splitter.setOrientation(qt.Qt.Vertical)
            self.m_vhbox.addWidget(self.inner_splitter)
            self.inner_splitter.addWidget(self.m_layer_ctrl_widget)
            self.inner_splitter.addWidget(self.m_layer_plot_widget)

            self.outer_splitter = QtGui.QSplitter()
            self.m_hbox.addWidget(self.outer_splitter)
            self.outer_splitter.addWidget(self.m_layer_view_widget)
            self.outer_splitter.addWidget(self.inner_container)

        self.m_layers = dict()

        self.m_exclusive_layer = None
        self.showMaximized()

    def axes(self):
        return self.m_layer_plot_widget.axes()

    def plot_canvas(self):
        return self.m_layer_plot_widget.mpl_canvas

    def draw_plot_canvas(self):
        self.m_layer_plot_widget.mpl_canvas.draw()

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
