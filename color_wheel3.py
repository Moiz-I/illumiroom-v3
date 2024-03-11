import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QSlider, QVBoxLayout, QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt

class HSVcolorpicker(QWidget):
  def __init__(self):  # Constructor with double underscores
      super().__init__()  
      self.initUI()

  def initUI(self):
      self.hue = QSlider(Qt.Horizontal)
      self.hue.setMinimum(0)
      self.hue.setMaximum(359)
      self.hue.setValue(312)
      self.hue.valueChanged.connect(self.update_color)

      self.saturation = QSlider(Qt.Horizontal)
      self.saturation.setMinimum(0)
      self.saturation.setMaximum(100)
      self.saturation.setValue(72)
      self.saturation.valueChanged.connect(self.update_color)

      self.value = QSlider(Qt.Horizontal)
      self.value.setMinimum(0)
      self.value.setMaximum(100)
      self.value.setValue(58)
      self.value.valueChanged.connect(self.update_color)

      self.color_label = QLabel()
      self.update_color_label()

      layout = QVBoxLayout()
      layout.addWidget(self.hue)
      layout.addWidget(self.saturation)
      layout.addWidget(self.value)
      layout.addWidget(self.color_label)
      self.setLayout(layout)

      self.setGeometry(300, 300, 300, 150)
      self.setWindowTitle('HSV Color Picker')
      self.show()

  def update_color(self):
      hue = self.hue.value()
      saturation = self.saturation.value()
      value = self.value.value()

      # Convert HSV to RGB
      color = self.hsv2rgb(hue, saturation, value)

      # Set the background color of the sliders
      self.hue.setStyleSheet(f"QSlider::groove:horizontal {{ background-color: hsl({hue}, 100%, 50%); }}")
      self.saturation.setStyleSheet(f"QSlider::groove:horizontal {{ background-color: hsl(0, {saturation}%, 50%); }}")
      self.value.setStyleSheet(f"QSlider::groove:horizontal {{ background-color: hsl(0, 0%, {value}%) }}")

      # Update the color label
      self.update_color_label()

  def update_color_label(self):
      hue = self.hue.value()
      saturation = self.saturation.value()
      value = self.value.value()

      color = self.hsv2rgb(hue, saturation, value)

      self.color_label.setText(f"Selected Color: RGB ({color[0]}, {color[1]}, {color[2]})")
      self.color_label.setStyleSheet(f"QLabel {{ background-color: rgb({color[0]}, {color[1]}, {color[2]}); }}")

  def hsv2rgb(self, h, s, v):
      h = h / 360
      s = s / 100
      v = v / 100
      c = v * s
      x = c * (1 - abs(h % 2 - 1))
      m = v - c

      if 0 <= h < 1:
          r = c + m
          g = x + m
          b = m
      elif 1 <= h < 2:
          r = x + m
          g = c + m
          b = m
      elif 2 <= h < 3:
          r = m
          g = c + m
          b = x + m
      elif 3 <= h < 4:
          r = m
          g = x + m
          b = c + m
      elif 4 <= h < 5:
          r = x + m
          g = m
          b = c + m
      else:
          r = c + m
          g = m
          b = x + m

      r = int(r * 255)
      g = int(g * 255)
      b = int(b * 255)
      return r, g, b  # Return the calculated RGB values


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HSVcolorpicker()
    sys.exit(app.exec_())
