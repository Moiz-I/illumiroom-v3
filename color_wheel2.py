import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QLinearGradient, QColor

class HSVSliders(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Hue Slider
        hue_slider = QSlider(Qt.Horizontal)
        hue_slider.setRange(0, 359)
        hue_slider.setValue(312)
        hue_gradient = QLinearGradient(0, 0, hue_slider.width(), 0)
        for i in range(360):
            hue_gradient.setColorAt(i / 360, QColor.fromHsv(i, 255, 255))
        hue_slider.setStyleSheet(f"QSlider::groove:horizontal {{ height: 20px; background: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 {hue_gradient.stops()[0][1]}, stop:1 {hue_gradient.stops()[-1][1]}); }} QSlider::handle:horizontal {{ background: white; width: 10px; }}")
        layout.addWidget(hue_slider)

        # Saturation Slider
        saturation_slider = QSlider(Qt.Horizontal)
        saturation_slider.setRange(0, 255)
        saturation_slider.setValue(71)
        saturation_gradient = QLinearGradient(0, 0, saturation_slider.width(), 0)
        saturation_gradient.setColorAt(0, Qt.white)
        saturation_gradient.setColorAt(1, QColor(255, 0, 255))
        saturation_slider.setStyleSheet(f"QSlider::groove:horizontal {{ height: 20px; background: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 {saturation_gradient.stops()[0][1]}, stop:1 {saturation_gradient.stops()[-1][1]}); }} QSlider::handle:horizontal {{ background: white; width: 10px; }}")
        layout.addWidget(saturation_slider)

        # Brightness/Value Slider
        brightness_slider = QSlider(Qt.Horizontal)
        brightness_slider.setRange(0, 255)
        brightness_slider.setValue(57)
        brightness_gradient = QLinearGradient(0, 0, brightness_slider.width(), 0)
        brightness_gradient.setColorAt(0, Qt.black)
        brightness_gradient.setColorAt(1, Qt.white)
        brightness_slider.setStyleSheet(f"QSlider::groove:horizontal {{ height: 20px; background: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 {brightness_gradient.stops()[0][1]}, stop:1 {brightness_gradient.stops()[-1][1]}); }} QSlider::handle:horizontal {{ background: white; width: 10px; }}")
        layout.addWidget(brightness_slider)

        self.setLayout(layout)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    hsv_sliders = HSVSliders()
    sys.exit(app.exec_())