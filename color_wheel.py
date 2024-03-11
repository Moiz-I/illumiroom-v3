import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class RangeColorPicker(QWidget):
    color_ranges = {
        "yellow": [((200, 200, 0), (255, 255, 100))],
        "blue": [((0, 0, 100), (70, 255, 255))],
        "white": [((200, 200, 200), (255, 255, 255))],
        "black": [((0, 0, 0), (50, 50, 50))],
        "red": [((150, 0, 0), (255, 60, 60))]
    }

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.selected_color = QColor(255, 255, 255)  # Default color is white

        self.setWindowTitle("Range Color Picker")
        self.setGeometry(100, 100, 400, 200)

        # Create a label to display the selected color
        self.color_label = self._create_color_label()
        main_layout.addWidget(self.color_label)

        # Create sliders for RGB values
        slider_layout = QHBoxLayout()
        self.red_slider = self._create_slider(255)
        self.green_slider = self._create_slider(255)
        self.blue_slider = self._create_slider(255)
        slider_layout.addWidget(self.red_slider)
        slider_layout.addWidget(self.green_slider)
        slider_layout.addWidget(self.blue_slider)
        main_layout.addLayout(slider_layout)

        # Connect slider signals to update_color_display
        self.red_slider.valueChanged.connect(self.update_color_display)
        self.green_slider.valueChanged.connect(self.update_color_display)
        self.blue_slider.valueChanged.connect(self.update_color_display)

        self.update_color_display()  # Update the color label initially

    def _create_color_label(self):
        label = QLabel()
        label.setAutoFillBackground(True)
        return label

    def _create_slider(self, max_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, max_value)
        slider.setValue(max_value)
        return slider

    def update_color_display(self):
        r = self.red_slider.value()
        g = self.green_slider.value()
        b = self.blue_slider.value()
        self.selected_color = QColor(r, g, b)

        palette = self.color_label.palette()
        palette.setColor(QPalette.Window, self.selected_color)
        self.color_label.setPalette(palette)

        self.check_color_ranges()

    def check_color_ranges(self):
        r, g, b = self.selected_color.red(), self.selected_color.green(), self.selected_color.blue()
        for color_range, ranges in self.color_ranges.items():
            for range_start, range_end in ranges:
                if (
                    range_start[0] <= r <= range_end[0] and
                    range_start[1] <= g <= range_end[1] and
                    range_start[2] <= b <= range_end[2]
                ):
                    print(f"The selected color is in the {color_range} range.")
                    break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    color_picker = RangeColorPicker()
    color_picker.show()
    sys.exit(app.exec_())