import sys
from PySide2.QtCore import Qt, QMimeData, QPointF
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsItem, QLabel
from PySide2.QtGui import QPolygonF, QDrag, QPixmap, QPainter, QColor, QPen, QBrush

class DraggablePolygon(QGraphicsItem):
    def __init__(self, polygon, parent=None):
        super(DraggablePolygon, self).__init__(parent)
        self.polygon = polygon
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return self.polygon.boundingRect()

    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.black))
        painter.setBrush(QBrush(Qt.red))
        painter.drawPolygon(self.polygon)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragStartPosition = event.pos()
        super(DraggablePolygon, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.dragStartPosition).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self.scene().views()[0])
        pixmap = QPixmap(self.boundingRect().size().toSize())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        self.paint(painter, None, None)
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos().toPoint())

        mime_data = QMimeData()
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)

        

    def mouseReleaseEvent(self, event):
        super(DraggablePolygon, self).mouseReleaseEvent(event)
        if self.scene() and self.scene().views():
            if self.scene().views()[0].parent() == self.scene().views()[0].parent().source_view:
                self.scene().views()[0].parent().source_view.create_polygon()

class PolygonView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))

        self.setRenderHint(QPainter.Antialiasing)
        self.setAcceptDrops(True)

    def create_polygon(self):
        polygon_points = [QPointF(-50, -50), QPointF(0, 50), QPointF(50, -50)]
        polygon = QPolygonF(polygon_points)
        self.polygon_item = DraggablePolygon(polygon)
        self.scene().addItem(self.polygon_item)

    def dragEnterEvent(self, event):
        if event.source() != self:
            event.acceptProposedAction()
            if event.source() == self.parent().source_view:
                event.source().create_polygon()
    def dragMoveEvent(self, event):
        if event.source() != self:
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.source() != self:
            event.acceptProposedAction()
            event.source().scene().removeItem(event.source().polygon_item)
            self.scene().addItem(event.source().polygon_item)
            event.source().polygon_item.setPos(self.mapToScene(event.pos()) - event.source().polygon_item.boundingRect().center())


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)

        self.source_view = PolygonView()
        self.source_view.create_polygon()
        layout.addWidget(self.source_view)

        self.target_view = PolygonView()
        layout.addWidget(self.target_view)

def main():
   
    app = QApplication(sys.argv)

    main_widget = MainWindow()
    main_widget.setWindowTitle('Drag and Drop Polygon Example')
    main_widget.resize(800, 400)
    main_widget.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

