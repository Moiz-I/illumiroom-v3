import sys
from enum import Enum
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QFileDialog,
    QGridLayout, QGroupBox, QRadioButton, QVBoxLayout, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, pyqtSlot, Qt
import json

# Constants
MP3_FILE_FILTER = "MP3 files (*.mp3)"
EXPERIENCE_FILE = "experience.json"

class TriggerType(Enum):
    SOUND = 'Sound'
    COLOR = 'Colour'
    TIME = 'Time'

class EffectType(Enum):
    PARTICLES = 'Particles'
    LIGHTNING = 'Lightning'
    BLUR = 'Blur'
    RAIN = 'Rain'
    FIRE = 'Fire'
    SNOW = 'Snow'

class ColorType(Enum):
    DEFAULT = 'Default'
    RED = 'Red'
    GREEN = 'Green'
    BLUE = 'Blue'    

class TriggerInputForm(QWidget):
    def __init__(self):
        super().__init__()
        self.experiences = []
        self.initUI()

    def initUI(self):
        self.main_layout = QHBoxLayout()

        # Left Column Layout
        left_column_layout = QVBoxLayout()

        # Name Input
        name_layout = QHBoxLayout()
        self.name_label = QLabel('Enter Name')
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_edit)
        left_column_layout.addLayout(name_layout)

        # Trigger Type
        trigger_layout = QHBoxLayout()
        self.trigger_label = QLabel('Trigger')
        self.trigger_combo = QComboBox()
        self.trigger_combo.addItems([trigger.value for trigger in TriggerType])
        trigger_layout.addWidget(self.trigger_label)
        trigger_layout.addWidget(self.trigger_combo)
        left_column_layout.addLayout(trigger_layout)

        # Trigger Input
        trigger_input_layout = QHBoxLayout()
        self.mp3_button = QPushButton('Select MP3 File')
        self.time_edit = QLineEdit()
        self.time_edit.setPlaceholderText('Enter time stamp')
        self.time_edit.setValidator(QRegExpValidator(QRegExp(r'\d{2}:\d{2}:\d{2}')))
        self.colour_edit = QLineEdit()
        self.colour_edit.setPlaceholderText('Enter colour value')
        trigger_input_layout.addWidget(self.mp3_button)
        trigger_input_layout.addWidget(self.colour_edit)
        trigger_input_layout.addWidget(self.time_edit)
        left_column_layout.addLayout(trigger_input_layout)

        # Parallel Combo Boxes
        self.combo_box_layout_1 = QVBoxLayout()
        self.combo_box_layout_2 = QVBoxLayout()
        combo_boxes_layout = QHBoxLayout()

        self.combo_box_label_1 = QLabel('Combo Box 1')
        self.combo_box_1 = QComboBox()
        self.combo_box_1.addItems([color.value for color in ColorType])
        self.combo_box_layout_1.addWidget(self.combo_box_label_1)
        self.combo_box_layout_1.addWidget(self.combo_box_1)

        self.combo_box_label_2 = QLabel('Combo Box 2')
        self.combo_box_2 = QComboBox()
        self.combo_box_2.addItems([colorEffect.value for colorEffect in EffectType])
        self.combo_box_layout_2.addWidget(self.combo_box_label_2)
        self.combo_box_layout_2.addWidget(self.combo_box_2)

        combo_boxes_layout.addLayout(self.combo_box_layout_1)
        combo_boxes_layout.addLayout(self.combo_box_layout_2)
        left_column_layout.addLayout(combo_boxes_layout)

        # Add new combo box button
        self.add_combo_box_button = QPushButton('Add Combo Box')
        left_column_layout.addWidget(self.add_combo_box_button)

        # Submit Button
        self.submit_button = QPushButton('Save')
        left_column_layout.addWidget(self.submit_button)

        # Right Column Layout
        right_column_layout = QVBoxLayout()

        # Effects Group
        self.effects_group = QGroupBox('Effects')
        effect_layout = QVBoxLayout()
        self.lightning_radio = QRadioButton(EffectType.LIGHTNING.value)
        self.blur_radio = QRadioButton(EffectType.BLUR.value)
        self.rain_radio = QRadioButton(EffectType.RAIN.value)
        effect_layout.addWidget(self.lightning_radio)
        effect_layout.addWidget(self.blur_radio)
        effect_layout.addWidget(self.rain_radio)
        self.effects_group.setLayout(effect_layout)
        right_column_layout.addWidget(self.effects_group)

        #add effect button
        self.add_effect_button = QPushButton('Add Effect')
        right_column_layout.addWidget(self.add_effect_button)
        

        # Add layouts to main layout
        self.main_layout.addLayout(left_column_layout)
        self.main_layout.addLayout(right_column_layout)

        self.setLayout(self.main_layout)

        # Signal-Slot Connections
        self.mp3_button.clicked.connect(self.select_mp3_file)
        self.trigger_combo.currentTextChanged.connect(self.toggle_trigger_input)
        self.submit_button.clicked.connect(self.on_submit_form)
        self.add_combo_box_button.clicked.connect(self.add_combo_box)

        # Set initial trigger input visibility
        self.toggle_trigger_input(TriggerType.SOUND.value)

        self.setWindowTitle('Trigger Input Menu')

        # Initialize combo box counters
        self.combo_box_counter_1 = 1
        self.combo_box_counter_2 = 1

    @pyqtSlot()
    def add_combo_box(self):
        # Create a new combo box for column 1
        combo_box_1 = QComboBox()
        combo_box_1.addItems([color.value for color in ColorType])
        self.combo_box_layout_1.addWidget(combo_box_1)
        self.combo_box_counter_1 += 1

        # Create a new combo box for column 2
        combo_box_2 = QComboBox()
        combo_box_2.addItems([colorEffect.value for colorEffect in EffectType])
        self.combo_box_layout_2.addWidget(combo_box_2)
        self.combo_box_counter_2 += 1

    @pyqtSlot(str)
    def toggle_trigger_input(self, trigger_type):
        self.mp3_button.setVisible(trigger_type == TriggerType.SOUND.value)
        self.colour_edit.setVisible(trigger_type == TriggerType.COLOR.value)
        self.time_edit.setVisible(trigger_type == TriggerType.TIME.value)

    @pyqtSlot()
    def select_mp3_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select an MP3 File', '', MP3_FILE_FILTER)
        if file_path:
            print(f'Selected file: {file_path}')

    @pyqtSlot()
    def on_submit_form(self):
        trigger_type = TriggerType(self.trigger_combo.currentText())
        trigger_name = self.name_edit.text().strip()
        effect_type = self.get_selected_effect()
        sample_value = self.get_trigger_sample(trigger_type)

        if not trigger_name:
            QMessageBox.warning(self, "Warning", "Please enter a name.")
            return

        if not sample_value:
            QMessageBox.warning(self, "Warning", "Please provide a valid trigger sample.")
            return
        
        if not effect_type:
            QMessageBox.warning(self, "Warning", "Please select an effect.")
            return

        experience = {
            'effect': effect_type.value,
            'trigger_type': trigger_type.value,
            'name': trigger_name,
            'sample': sample_value
        }

        self.experiences.append(experience)
        self.save_experiences()
        self.clear_form()

    def get_selected_effect(self):
        if self.lightning_radio.isChecked():
            return EffectType.LIGHTNING
        elif self.blur_radio.isChecked():
            return EffectType.BLUR
        elif self.rain_radio.isChecked():
            return EffectType.RAIN
        else:
            return None

    def get_trigger_sample(self, trigger_type):
        if trigger_type == TriggerType.SOUND:
            return self.mp3_button.text()
        elif trigger_type == TriggerType.COLOR:
            return self.colour_edit.text()
        elif trigger_type == TriggerType.TIME:
            return self.time_edit.text()
        else:
            return None

    def save_experiences(self):
        try:
            with open(EXPERIENCE_FILE, 'w') as file:
                json.dump(self.experiences, file, indent=4)
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Failed to save experiences: {e}")

    def clear_form(self):
        self.name_edit.clear()
        self.mp3_button.setText('')
        self.colour_edit.clear()
        self.time_edit.clear()
        self.lightning_radio.setChecked(False)
        self.blur_radio.setChecked(False)
        self.rain_radio.setChecked(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = TriggerInputForm()
    form.show()
    sys.exit(app.exec_())