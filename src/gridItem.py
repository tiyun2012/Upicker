import sys
from PySide2.QtCore import Qt, QPointF
from PySide2.QtGui import QPen, QColor, QPainterPath
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPathItem

class GraphicsView(QGraphicsView):
    def __init__(self, background_color=Qt.white, grid_color=QColor(230, 230, 230)):
        super().__init__()

        self.background_color = background_color
        self.grid_color = grid_color

        # Set up the scene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.grid_item = self.create_grid_item(1000, 1000, 50)
        self.scene.addItem(self.grid_item)

        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setBackgroundBrush(QColor(self.background_color))

    def create_grid_item(self, width, height, spacing):
        item = QGraphicsPathItem()
        pen = QPen(self.grid_color)
        pen.setWidth(1)
        item.setPen(pen)

        path = QPainterPath()

        for x in range(0, width + 1, spacing):
            path.moveTo(x, 0)
            path.lineTo(x, height)

        for y in range(0, height + 1, spacing):
            path.moveTo(0, y)
            path.lineTo(width, y)

        item.setPath(path)

        return item
if __name__ == '__main__':
    app = QApplication([])
    view = GraphicsView(background_color=QColor(0, 0, 0), grid_color=QColor(230, 230, 230))
    view.show()
    sys.exit(app.exec_())