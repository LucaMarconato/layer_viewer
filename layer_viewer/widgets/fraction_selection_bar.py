import warnings

from pyqtgraph.Qt import QtCore, QtGui


class FractionSelectionBar(QtGui.QWidget):
    fractionChanged = QtCore.pyqtSignal(float)

    def __init__(self, initial_fraction=1., parent=None):
        super(FractionSelectionBar, self).__init__(parent=parent)
        self._fraction = initial_fraction
        self._lmb_down = False

    def fraction(self):
        return self._fraction

    def set_fraction(self, value):
        if value == self._fraction:
            return
        if value < 0.:
            value = 0.
            warnings.warn(
                "FractionSelectionBar.setFraction(): value has to be between 0. and 1. (was %s); setting to 0." % str(
                    value))
        if value > 1.:
            value = 1.
            warnings.warn(
                "FractionSelectionBar.setFraction(): value has to be between 0. and 1. (was %s); setting to 1." % str(
                    value))
        self._fraction = float(value)
        self.update()
        self.fractionChanged.emit(self._fraction)

    def mouseMoveEvent(self, event):
        if self._lmb_down:
            self.set_fraction(self._fraction_from_position(event.localPos()))
            self.fractionChanged.emit(self._fraction)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            return
        self._lmb_down = True
        self.set_fraction(self._fraction_from_position(event.localPos()))
        self.fractionChanged.emit(self._fraction)

    def mouseReleaseEvent(self, event):
        self._lmb_down = False

    def paintEvent(self, ev):
        painter = QtGui.QPainter(self)

        # calc bar offset
        y_offset = (self.height() - self._bar_height()) // 2
        # prevent negative offset
        y_offset = 0 if y_offset < 0 else y_offset

        # frame around fraction indicator
        painter.setBrush(self.palette().dark())
        painter.save()
        # no fill color
        b = painter.brush();
        b.setStyle(QtCore.Qt.NoBrush);
        painter.setBrush(b)
        painter.drawRect(
            QtCore.QRect(QtCore.QPoint(0, y_offset),
                         QtCore.QSize(self._bar_width(), self._bar_height())))
        painter.restore()

        # fraction indicator
        painter.drawRect(
            QtCore.QRect(QtCore.QPoint(0, y_offset),
                         QtCore.QSize(self._bar_width() * self._fraction, self._bar_height())))

    def sizeHint(self):
        return QtCore.QSize(100, 10)

    def minimum_size_hint(self):
        return QtCore.QSize(1, 3)

    def _bar_width(self):
        return self.width() - 1

    def _bar_height(self):
        return self.height() - 1

    def _fraction_from_position(self, pointf):
        frac = float(pointf.x()) / self.width()
        # mouse has left the widget
        if frac < 0.:
            frac = 0.
        if frac > 1.:
            frac = 1.
        return frac
