import subprocess
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
EXPERIENCE_FILE = "experiences.json"

class TriggerType(Enum):
    SOUND = 'Sound'
    COLOR = 'Color'
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
        self.load_experiences()
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

        # Trigger Settings Group
        trigger_settings_group = QGroupBox('Trigger Settings')
        trigger_settings_group.setStyleSheet('QGroupBox { background-color: #d9d9d9; }')
        trigger_settings_group.setStyleSheet('QGroupBox { border: 2px solid #d9d9d9; }')
        trigger_settings_layout = QVBoxLayout()


        # Trigger Input
        trigger_input_layout = QHBoxLayout()
        self.mp3_button = QPushButton('Select MP3 File')
        self.time_edit = QLineEdit()
        self.time_edit.setPlaceholderText('Enter time stamp')
        self.time_edit.setValidator(QRegExpValidator(QRegExp(r'\d{2}:\d{2}:\d{2}')))
        trigger_input_layout.addWidget(self.mp3_button)
        trigger_input_layout.addWidget(self.time_edit)
        trigger_settings_layout.addLayout(trigger_input_layout)

        # Parallel Combo Boxes
        self.combo_box_layout_1 = QVBoxLayout()
        self.combo_box_layout_2 = QVBoxLayout()
        combo_boxes_layout = QHBoxLayout()

        self.combo_box_label_1 = QLabel('Color input range')
        self.combo_box_1 = QComboBox()
        self.combo_box_1.addItems([color.value for color in ColorType])
        self.combo_box_layout_1.addWidget(self.combo_box_label_1)
        self.combo_box_layout_1.addWidget(self.combo_box_1)

        self.combo_box_label_2 = QLabel('Effect triggered')
        self.combo_box_2 = QComboBox()
        self.combo_box_2.addItems([colorEffect.value for colorEffect in EffectType])
        self.combo_box_layout_2.addWidget(self.combo_box_label_2)
        self.combo_box_layout_2.addWidget(self.combo_box_2)

        combo_boxes_layout.addLayout(self.combo_box_layout_1)
        combo_boxes_layout.addLayout(self.combo_box_layout_2)
        trigger_settings_layout.addLayout(combo_boxes_layout)

        # Add new combo box button
        self.add_combo_box_button = QPushButton('+')
        trigger_settings_layout.addWidget(self.add_combo_box_button)

        trigger_settings_group.setLayout(trigger_settings_layout)
        left_column_layout.addWidget(trigger_settings_group)

        # Submit Button
        self.submit_button = QPushButton('Save')
        left_column_layout.addWidget(self.submit_button)

        # Right Column Layout
        right_column_layout = QVBoxLayout()

        # Effects Group
        self.effects_group = QGroupBox('Effects')
        self.effects_group.setStyleSheet('QGroupBox { background-color: #d9d9d9; }')
        effect_layout = QVBoxLayout()
        # self.lightning_radio = QRadioButton(EffectType.LIGHTNING.value)
        # self.blur_radio = QRadioButton(EffectType.BLUR.value)
        # self.rain_radio = QRadioButton(EffectType.RAIN.value)
        # effect_layout.addWidget(self.lightning_radio)
        # effect_layout.addWidget(self.blur_radio)
        # effect_layout.addWidget(self.rain_radio)
        self.effect_radios = {}
        for effect_type in EffectType:
            radio_button = QRadioButton(effect_type.value)
            self.effect_radios[effect_type] = radio_button
            effect_layout.addWidget(radio_button)
        self.effects_group.setLayout(effect_layout)
        right_column_layout.addWidget(self.effects_group)

        # Add effect button
        self.add_effect_button = QPushButton('Add Effect')
        self.add_effect_button.clicked.connect(self.run_program)
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

    def run_program(self):
        subprocess.Popen(['dist/new_trigger_menu.exe'])

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
        # self.colour_edit.setVisible(trigger_type == TriggerType.COLOR.value)

        if trigger_type == TriggerType.COLOR.value:
            for radio_button in self.effect_radios.values():
                radio_button.setEnabled(False)
        else:
            for radio_button in self.effect_radios.values():
                radio_button.setEnabled(True)
        
        count1 = self.combo_box_layout_1.count()
        count2 = self.combo_box_layout_2.count()
        for i in range(count1):
            widget = self.combo_box_layout_1.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(trigger_type == TriggerType.COLOR.value)
        for i in range(count2):
            widget = self.combo_box_layout_2.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(trigger_type == TriggerType.COLOR.value)

              

        self.combo_box_1.setVisible(trigger_type == TriggerType.COLOR.value)
        self.combo_box_2.setVisible(trigger_type == TriggerType.COLOR.value)
        self.combo_box_label_1.setVisible(trigger_type == TriggerType.COLOR.value)
        self.combo_box_label_2.setVisible(trigger_type == TriggerType.COLOR.value)
        self.add_combo_box_button.setVisible(trigger_type == TriggerType.COLOR.value)
        self.time_edit.setVisible(trigger_type == TriggerType.TIME.value)

    @pyqtSlot()
    def select_mp3_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select an MP3 File', '', MP3_FILE_FILTER)
        if file_path:
            print(f'Selected file: {file_path}')

    def load_experiences(self):
        try:
            with open(EXPERIENCE_FILE, 'r') as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.experiences = data.get('experiences', {})
                    self.selected_experience = data.get('selected_experience', '')
                else:
                    # Assume data is a list of experiences
                    self.experiences = {exp['name']: exp for exp in data}
                    self.selected_experience = ''
        except (FileNotFoundError, json.JSONDecodeError):
            self.experiences = {}
            self.selected_experience = ''

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

        if trigger_type != TriggerType.COLOR and not effect_type:
            QMessageBox.warning(self, "Warning", "Please select an effect.")
            return

        if trigger_type == TriggerType.COLOR:
            experience = {
                'trigger_type': trigger_type.value,
                **sample_value
            }
        else:
            experience = {
                'trigger_type': trigger_type.value,
                'effect': effect_type.value,
                **sample_value
            }

        self.experiences[trigger_name] = experience
        self.save_experiences()
        self.clear_form()

    def get_selected_effect(self):
        for effect_type, radio_button in self.effect_radios.items():
            if radio_button.isChecked():
                return effect_type
        return None
    
    def get_trigger_sample(self, trigger_type):
        if trigger_type == TriggerType.SOUND:
            return {'file_path': self.mp3_button.text()}
        elif trigger_type == TriggerType.COLOR:
            color_mapping = {}
            count = self.combo_box_layout_1.count()
            for i in range(1, count):
                color_selection = self.combo_box_layout_1.itemAt(i).widget()
                color_effect = self.combo_box_layout_2.itemAt(i).widget()
                if color_selection is not None and color_effect is not None:
                    color = color_selection.currentText()
                    effect = color_effect.currentText()
                    color_mapping[color] = effect
            return {'colors': color_mapping}
        elif trigger_type == TriggerType.TIME:
            return {'time_stamp': self.time_edit.text()}
        else:
            return {}

    def save_experiences(self):
        try:
            with open(EXPERIENCE_FILE, 'w') as file:
                json.dump({
                    'selected_experience': self.selected_experience,
                    'experiences': self.experiences
                }, file, indent=4)
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Failed to save experiences: {e}")

    def clear_form(self):
        self.name_edit.clear()
        # self.mp3_button.setText('')
        # count = self.combo_box_layout_1.count()
        # for i in range(2, count):
        #     widget1 = self.combo_box_layout_1.itemAt(i).widget()
        #     widget2 = self.combo_box_layout_2.itemAt(i).widget()
        #     if widget1 is not None and widget2 is not None:
        #         widget1.deleteLater()
        #         widget2.deleteLater()
        self.time_edit.clear()
        for radio_button in self.effect_radios.values():
            radio_button.setChecked(False)

        self.trigger_combo.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = TriggerInputForm()
    form.show()
    sys.exit(app.exec_())