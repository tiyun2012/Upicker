import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QTabWidget, QHBoxLayout, QWidget, QSplitter,
                               QVBoxLayout, QGroupBox, QSlider, QFormLayout, QSizePolicy)
from PySide2.QtCore import Qt,Signal,QEvent





class CustomTabWidget(QTabWidget):
    tabClicked = Signal(int)
    tabHovered = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabBar().setMouseTracking(True)
        self.tabBar().installEventFilter(self)

    def eventFilter(self, watched, event):
        if watched == self.tabBar():
            if event.type() == QEvent.MouseMove:
                tab_index = self.tabBar().tabAt(event.pos())
                if tab_index != -1:
                    self.tabHovered.emit(tab_index)
                    print(f"You are hovering over tab {tab_index + 1}")
            
            if event.type() == QEvent.MouseButtonPress:
                mouse_event = event  # Cast QEvent to QMouseEvent
                if mouse_event.button() == Qt.LeftButton:  # Check if left button is pressed
                    tab_index = self.tabBar().tabAt(event.pos())
                    if tab_index != -1:
                        self.tabClicked.emit(tab_index)
                        print(f"You are Press over tab {tab_index + 1}")
            
        return super().eventFilter(watched, event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a central widget for the main window
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Set up the layout
        layout = QVBoxLayout(central_widget)
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # Create a QGraphicsView and QGraphicsScene
        graphics_view = QGraphicsView(self)
        graphics_scene = QGraphicsScene(self)
        graphics_view.setScene(graphics_scene)

        # Create a QTabWidget
        self.tab_widget = CustomTabWidget(self)
        self.tab_widget_height=self.tab_widget.height()
        self.tab_widget.setTabPosition(QTabWidget.East)  # Set tab position to the right side
        self.tab_widget.setMinimumWidth(35)  # Set minimum width to keep the tab border visible
        self.tab_widget.sizeHint()
        # Create the group boxes with sliders for each tab
        for i in range(2):
            group_box = QGroupBox(f"Group Box {i + 1}")
            form_layout = QFormLayout(group_box)

            for j in range(3):
                slider = QSlider(Qt.Horizontal)
                form_layout.addRow(f"Slider {j + 1}:", slider)

            self.tab_widget.addTab(group_box, f"Tab {i + 1}")

        # Apply custom style sheet for rounded tabs
        self.tab_widget.setStyleSheet("""
        QTabWidget::pane {
            border: none;
        }
        QTabBar::tab {
            border: 1px solid #999;
            border-radius: 10px;
            padding: 5px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E0E0E0, stop: 1 #FFFFFF);
            margin-top: 2px;
            margin-left: 2px;
        }
        QTabBar::tab:selected {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FFFFFF, stop: 1 #E0E0E0);
        }
        """)

        # Add the widgets to the splitter
        splitter.addWidget(graphics_view)
        splitter.addWidget(self.tab_widget)

        # Adjust splitter handle width
        splitter.setHandleWidth(5)

        # Set the minimum and maximum size of the QTabWidget
        self.tab_widget.setMinimumSize(40, 0)
        graphics_view.setMaximumWidth(self.width() - self.tab_widget.minimumWidth())

        # Connect the currentChanged signal to a custom slot
        # self.tab_widget.currentChanged.connect(self.on_tab_selected)

        # Connect the splitterMoved signal to the update_widget_sizes method
        splitter.splitterMoved.connect(self.update_widget_sizes)
        self.tab_widget.tabClicked.connect(self.on_tab_clicked)
        self.tab_widget.tabHovered.connect(self.on_tab_hovered)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_widget_sizes()

    def update_widget_sizes(self):
        graphics_view = self.centralWidget().findChild(QGraphicsView)
        max_width = self.width() - self.centralWidget().findChild(QTabWidget).minimumWidth()
        current_width = self.centralWidget().findChild(QTabWidget).width()
        graphics_view.setMaximumWidth(max_width)
        self.tab_widget.setMaximumWidth(self.width() - graphics_view.width())
        self.tab_widget.setMinimumSize(40, 0)

    def on_tab_clicked(self, index):
        # self.centralWidget().findChild(QGraphicsView).setMaximumWidth(self.width() - 200)
        # self.tab_widget.setFixedWidth(200)
        self.tab_widget.setMinimumSize(200, 0)
        print('hei: {}'.format(self.tab_widget_height))
    def on_tab_hovered(self, index):
        # self.centralWidget().findChild(QGraphicsView).setMaximumWidth(self.width() - 200)
        # self.tab_widget.setFixedWidth(200)
        print('on_tab_hovered---------------')
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()

    main_window.show()

    sys.exit(app.exec_())
