# from PyQt5.QtGui import QFontMetrics, QFont
# from PyQt5.QtWidgets import QWidget, QLabel, QSpinBox
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets

from ..widgets import TripleToggleEye, FractionSelectionBar, GradientWidget


class LayerItemWidget(QtWidgets.QWidget):

    def __init__(self, name=None, parent=None, add_gradient_widgtet=False,
                 channel_selector=False, add_as_rgb_button=False):
        super(LayerItemWidget, self).__init__(parent=parent)
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
        self.channel_selector.setVisible(channel_selector)

        self._layout = QtGui.QGridLayout(self)
        self._layout.addWidget(self.toggle_eye, 0, 0)
        self._layout.addWidget(self.name_label, 0, 1)
        self._layout.addWidget(self.opacity_label, 0, 2)
        self._layout.addWidget(self.channel_selector, 1, 0)

        self._layout.addWidget(self.bar, 1, 1, 1, 2)

        if add_gradient_widgtet:
            self.gradient_widget = GradientWidget(orientation='top')
            self.gradient_widget.load_preset('grey')
            self._layout.addWidget(self.gradient_widget, 3, 1, 1, 2)

        # if add_as_rgb_button:
        #     self.asRgb = QCheckBox(  )
        #     #self.asRgb.setFrame( False )
        #     #self.asRgb.setFont( self._font )
        #     self.asRgb.setMaximumWidth( 35 )
        #     self.asRgb.setAlignment(Qt.AlignRight)
        #     self.asRgb.setToolTip("Show As RGB")
        #     #self.asRgb.setVisible(channel_selector)
        #     self._layout.addWidget( self.gradient_widget, 3,0,1,2)

        self._layout.setColumnMinimumWidth(2, 35)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        def f(frac):
            self.opacity_label.setText(u"\u03B1=%0.1f%%" % (100.0 * (self.bar.fraction())))

        self.bar.fractionChanged.connect(f)

    def setFraction(self, opacity):
        self.bar.set_fraction(opacity)
        self.opacity_label.setText(u"\u03B1=%0.1f%%" % (100.0 * (self.bar.fraction())))

    def set_name(self, name):
        self.name_label.setText(str(name))

    def mousePressEvent(self, ev):
        super(LayerItemWidget, self).mousePressEvent(ev)
