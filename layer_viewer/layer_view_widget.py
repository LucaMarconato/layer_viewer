import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt import QtCore, QtGui

_nameToPattern = {
    'SolidPattern': QtCore.Qt.SolidPattern,
    'LinearGradientPattern': QtCore.Qt.LinearGradientPattern,
    'Dense1Pattern': QtCore.Qt.Dense1Pattern,
    'Dense2Pattern': QtCore.Qt.Dense2Pattern,
    'Dense3Pattern': QtCore.Qt.Dense3Pattern,
    'Dense4Pattern': QtCore.Qt.Dense4Pattern,
    'Dense5Pattern': QtCore.Qt.Dense5Pattern,
    'Dense6Pattern': QtCore.Qt.Dense6Pattern,
    'Dense7Pattern': QtCore.Qt.Dense7Pattern,
    'NoBrush': QtCore.Qt.NoBrush,
    'HorPattern': QtCore.Qt.HorPattern,
    'VerPattern': QtCore.Qt.VerPattern,
    'CrossPattern': QtCore.Qt.CrossPattern,
    'BDiagPattern': QtCore.Qt.BDiagPattern,
    'FDiagPattern': QtCore.Qt.FDiagPattern,
    'DiagCrossPattern': QtCore.Qt.DiagCrossPattern
}


def get_qt_pattern(name):
    return _nameToPattern[str(name)]


class MyViewBox(pg.ViewBox):
    def __init__(self):
        super(MyViewBox, self).__init__()

    def keyPressEvent(self, ev):
        pass
        # ev.ignore()


class LayerViewWidget(QtGui.QWidget):
    def __init__(self, settings_widget, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.graph_view = pg.GraphicsView()
        self.graph_view_layout = QtGui.QGraphicsGridLayout()
        self.graph_view.centralWidget.setLayout(self.graph_view_layout)

        # self.setPolicy(self.graph_view,QtGui.QSizePolicy.Expanding)

        # view box
        self.view_box = MyViewBox()
        self.view_box.setAspectLocked(True)
        # add view box to graph view layout
        self.graph_view_layout.addItem(self.view_box, 0, 0)
        self.hbox = QtGui.QHBoxLayout()
        self.setLayout(self.hbox)
        self.hbox.addWidget(self.graph_view)

        # flip the view box
        self.view_box.invertY(True)

        self.settings_widget = settings_widget

        def bg_change(*args, **kwargs):
            # print("waerawe")
            self.set_background()

        bg_params = settings_widget.p.param('ViewBox Options', 'ViewBox Background')

        # too lazy for recursion:
        for child in bg_params.children():
            child.sigValueChanged.connect(bg_change)
            for ch2 in child.children():
                ch2.sigValueChanged.connect(bg_change)

        self.set_background()

        s = self.view_box.menu.addAction('Settings')
        s.triggered.connect(self.show_settings)

    def show_settings(self):
        print("settings")
        self.settings_widget.show()
        self.settings_widget.resize(QtCore.QSize(500, 300))
        self.settings_widget.move(
            self.window().frameGeometry().topLeft() + self.window().rect().center() - self.settings_widget.rect().center())

    def set_background(self):
        self.bg_type = self.settings_widget.p[('ViewBox Options', 'ViewBox Background', 'bg-type')]
        self.bg_color1 = self.settings_widget.p[('ViewBox Options', 'ViewBox Background', 'bg-color 1')]
        self.bg_color2 = self.settings_widget.p[('ViewBox Options', 'ViewBox Background', 'bg-color 2')]

        bg = self.view_box.background
        self.view_box.background.show()
        bg.setVisible(True)
        if self.bg_type == 'LinearGradientPattern':
            g = QtGui.QLinearGradient(
                QtCore.QRectF(self.rect()).topLeft(),
                QtCore.QRectF(self.rect()).bottomLeft()
            )
            g.setColorAt(0, self.bg_color1)
            g.setColorAt(1, self.bg_color2)
            brush = QtGui.QBrush(g)
        else:
            brush = QtGui.QBrush()
            brush.setStyle(get_qt_pattern(self.bg_type))
            brush.setColor(self.bg_color1)

        bg.setBrush(brush)
