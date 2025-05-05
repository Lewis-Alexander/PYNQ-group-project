import sys
import math
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox,
    QComboBox, QPushButton, QSpinBox
)
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure
from spiro import hypotrochoid, epitrochoid

class TrochoidPlot(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Hypotrochoid", "Epitrochoid"])
        self.type_combo.currentIndexChanged.connect(self.update_plot)

        # R, r, d 7-bit signed integer (-31 - 31)
        self.R_spin = QSpinBox()
        self.R_spin.setRange(-31, 31)
        self.R_spin.setValue(5)
        self.R_spin.valueChanged.connect(self.update_plot)

        self.r_spin = QSpinBox()
        self.r_spin.setRange(-31, 31)
        self.r_spin.setValue(3)
        self.r_spin.valueChanged.connect(self.update_plot)

        self.d_spin = QSpinBox()
        self.d_spin.setRange(-31, 31)
        self.d_spin.setValue(5)
        self.d_spin.valueChanged.connect(self.update_plot)

        # Numpoints 10-bit unsigned integer (1 - 1023)
        self.num_points_spin = QSpinBox()
        self.num_points_spin.setRange(1, 1023)
        self.num_points_spin.setValue(500)
        self.num_points_spin.valueChanged.connect(self.update_plot)

        # Pan & Zoom controls
        self.pan_interval_spin = QDoubleSpinBox()
        self.pan_interval_spin.setRange(0.01, 100)
        self.pan_interval_spin.setDecimals(2)
        self.pan_interval_spin.setValue(1.0)

        self.zoom_factor_spin = QDoubleSpinBox()
        self.zoom_factor_spin.setRange(1.01, 10)
        self.zoom_factor_spin.setDecimals(2)
        self.zoom_factor_spin.setValue(1.2)

        self.btn_pan_left = QPushButton("Pan Left")
        self.btn_pan_right = QPushButton("Pan Right")
        self.btn_pan_up = QPushButton("Pan Up")
        self.btn_pan_down = QPushButton("Pan Down")
        self.btn_zoom_in = QPushButton("Zoom In")
        self.btn_zoom_out = QPushButton("Zoom Out")

        # Connect pan/zoom
        self.btn_pan_left.clicked.connect(lambda: self.pan(-1, 0))
        self.btn_pan_right.clicked.connect(lambda: self.pan(1, 0))
        self.btn_pan_up.clicked.connect(lambda: self.pan(0, 1))
        self.btn_pan_down.clicked.connect(lambda: self.pan(0, -1))
        self.btn_zoom_in.clicked.connect(lambda: self.zoom(1))
        self.btn_zoom_out.clicked.connect(lambda: self.zoom(-1))

        # Layout controls
        controls = QHBoxLayout()
        controls.addWidget(QLabel("Type:"))
        controls.addWidget(self.type_combo)
        controls.addWidget(QLabel("R:"))
        controls.addWidget(self.R_spin)
        controls.addWidget(QLabel("r:"))
        controls.addWidget(self.r_spin)
        controls.addWidget(QLabel("d:"))
        controls.addWidget(self.d_spin)
        controls.addWidget(QLabel("Points:"))
        controls.addWidget(self.num_points_spin)

        panzoom = QHBoxLayout()
        panzoom.addWidget(QLabel("Pan interval:"))
        panzoom.addWidget(self.pan_interval_spin)
        panzoom.addWidget(self.btn_pan_left)
        panzoom.addWidget(self.btn_pan_right)
        panzoom.addWidget(self.btn_pan_up)
        panzoom.addWidget(self.btn_pan_down)
        panzoom.addSpacing(20)
        panzoom.addWidget(QLabel("Zoom factor:"))
        panzoom.addWidget(self.zoom_factor_spin)
        panzoom.addWidget(self.btn_zoom_in)
        panzoom.addWidget(self.btn_zoom_out)

        layout = QVBoxLayout()
        layout.addLayout(controls)
        layout.addLayout(panzoom)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Initial plot
        self.update_plot()

    def update_plot(self):
        R = self.R_spin.value()
        r = self.r_spin.value()
        d = self.d_spin.value()
        num_points = self.num_points_spin.value()
        trochoid_type = self.type_combo.currentText()

        if trochoid_type == "Hypotrochoid":
            x, y = hypotrochoid(R, r, d, num_points)
        else:
            x, y = epitrochoid(R, r, d, num_points)

        # Clear and redraw
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(x, y)
        self.ax.set_aspect('equal', 'box')
        self.ax.set_title(f"{trochoid_type} (R={R}, r={r}, d={d}, pts={num_points})")
        self.ax.grid(True)
        self.canvas.draw()

    def pan(self, dx, dy):
        interval = self.pan_interval_spin.value()
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(xlim[0] + dx * interval, xlim[1] + dx * interval)
        self.ax.set_ylim(ylim[0] + dy * interval, ylim[1] + dy * interval)
        self.canvas.draw()

    def zoom(self, direction):
        factor = self.zoom_factor_spin.value()
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        x_center = sum(xlim) / 2
        y_center = sum(ylim) / 2
        x_span = xlim[1] - xlim[0]
        y_span = ylim[1] - ylim[0]
        scale = 1/factor if direction > 0 else factor
        new_x_span = x_span * scale
        new_y_span = y_span * scale
        self.ax.set_xlim(x_center - new_x_span/2, x_center + new_x_span/2)
        self.ax.set_ylim(y_center - new_y_span/2, y_center + new_y_span/2)
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trochoid Explorer")
        self.setCentralWidget(TrochoidPlot())
        self.resize(1024, 768)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())