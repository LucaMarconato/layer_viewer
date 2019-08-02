import pyqtgraph as pg
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

def getQtPattern(name):
    return _nameToPattern[str(name)]


class MyViewBox(pg.ViewBox):
    def __init__(self):
        super(MyViewBox, self).__init__()

    def keyPressEvent(self, ev):
        pass
        #ev.ignore()

class LayerViewWidget(QtGui.QWidget):
    def __init__(self,settings_widget, parent=None):
        QtGui.QWidget.__init__(self, parent)


        self.graphView       = pg.GraphicsView()
        self.graphViewLayout = QtGui.QGraphicsGridLayout()
        self.graphView.centralWidget.setLayout(self.graphViewLayout)

        #self.setPolicy(self.graphView,QtGui.QSizePolicy.Expanding)


        # view box
        self.view_box = MyViewBox()#parent=self)
        self.view_box.setAspectLocked(True)
        # add view box to graph view layout
        self.graphViewLayout.addItem(self.view_box,0,0)
        self.hbox = QtGui.QHBoxLayout()
        self.setLayout(self.hbox)
        self.hbox.addWidget(self.graphView)

        # flip the view box
        self.view_box.invertY(True)


        self.settings_widget = settings_widget

        def bg_change(*args,**kwargs):
            #print("waerawe")
            self.setBackground()


        bg_params = settings_widget.p.param('ViewBox Options','ViewBox Background')
        
        # Too lazy for recursion:
        for child in bg_params.children():
            child.sigValueChanged.connect(bg_change)
            for ch2 in child.children():
                ch2.sigValueChanged.connect(bg_change)
                

        self.setBackground()
                

 

        s = self.view_box.menu.addAction('Settings')
        s.triggered.connect(self.showSettings)


    def showSettings(self):
        print("settings")
        self.settings_widget.show()

    def setBackground(self):        

        self.bgType  = self.settings_widget.p[('ViewBox Options','ViewBox Background','bg-type')]
        self.bgColor1 = self.settings_widget.p[('ViewBox Options','ViewBox Background','bg-color 1')]
        self.bgColor2 = self.settings_widget.p[('ViewBox Options','ViewBox Background','bg-color 2')]

        bg = self.view_box.background
        self.view_box.background.show()
        bg.setVisible(True)
        if self.bgType == 'LinearGradientPattern':
            g =  QtGui.QLinearGradient(
                                       QtCore.QRectF(self.rect()).topLeft(),
                                       QtCore.QRectF(self.rect()).bottomLeft()
            )
            g.setColorAt(0, self.bgColor1);
            g.setColorAt(1, self.bgColor2);
            brush = QtGui.QBrush(g)
        else:
            brush = QtGui.QBrush()
            brush.setStyle(getQtPattern(self.bgType))
            brush.setColor(self.bgColor1)

        bg.setBrush(brush)