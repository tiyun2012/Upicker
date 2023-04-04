import sys
import json
from PySide2.QtWidgets import QApplication, QMainWindow, QToolBar, QAction
from PySide2.QtGui import QIcon, QPixmap, QPainter, QPolygonF
from PySide2.QtCore import Qt, QPointF

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Define a list of polygons (triangle and square)
        polygons = [
            QPolygonF([QPointF(0, 32), QPointF(16, 0), QPointF(32, 32)]),  # Triangle
            QPolygonF([QPointF(0, 0), QPointF(32, 0), QPointF(32, 32), QPointF(0, 32)])  # Square
        ]

        # Serialize the polygons and store them in a JSON file
        serialized_polygons = [
            [(point.x(), point.y()) for point in polygon] for polygon in polygons
        ]
        json_data = {"polybar": serialized_polygons}
        with open("polygons.json", "w") as file:
            json.dump(json_data, file)

        # Create a QToolBar widget
        toolbar = QToolBar()

        # Loop through the polygons and create icons for each
        for polygon in polygons:
            # Create a QPixmap object with the specified dimensions (32x32)
            pixmap = QPixmap(32, 32)
            # Fill the pixmap with a transparent background
            pixmap.fill(Qt.transparent)

            # Create a QPainter object to draw on the QPixmap
            painter = QPainter(pixmap)
            # Set the pen color to black for drawing the polygon's outline
            painter.setPen(Qt.black)
            # Set the brush color to blue for filling the polygon
            painter.setBrush(Qt.blue)

            # Draw the polygon on the QPixmap using the QPainter
            painter.drawPolygon(polygon)
            # End the QPainter's drawing operations
            painter.end()

            # Create a QIcon object from the QPixmap containing the drawn polygon
            polygon_icon = QIcon(pixmap)

            # Create a QAction with the QIcon and a text label, and add it to the toolbar
            polygon_action = QAction(polygon_icon, "Polygon", self)
            toolbar.addAction(polygon_action)

        # Add the toolbar to the main window
        self.addToolBar(toolbar)

if __name__ == "__main__":
    # Create a QApplication object for the main event loop
    app = QApplication(sys.argv)
    # Instantiate the MainWindow class
    window = MainWindow()
    # Show the main window on the screen
    window.show()
    # Start the main event loop and exit the application when it's closed
    sys.exit(app.exec_())
