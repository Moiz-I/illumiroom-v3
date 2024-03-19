import subprocess
import sys
from enum import Enum
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QFileDialog,
    QGridLayout, QGroupBox, QRadioButton, QVBoxLayout, QMessageBox, QHBoxLayout, QTimeEdit
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, pyqtSlot, Qt, QTime
import json
from pymediainfo import MediaInfo

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

class TriggerUI:
    def __init__(self, parent):
        self.parent = parent
        self.trigger_type = None

    def setup_ui(self):
        raise NotImplementedError("This method should be implemented by the subclass.")

    def toggle_visibility(self, visible):
        raise NotImplementedError("This method should be implemented by the subclass.")

class SoundTriggerUI(TriggerUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.trigger_type = TriggerType.SOUND
        self.mp3_button = QPushButton('Select MP3 File')

    def setup_ui(self):
        self.mp3_button.clicked.connect(lambda: self.select_mp3_file(True))
        return self.mp3_button

    def toggle_visibility(self, visible):
        self.mp3_button.setVisible(visible)

    @pyqtSlot(bool)  # Explicitly specify the parameter type
    def select_mp3_file(self, checked):  # Accept the boolean parameter
        file_path, _ = QFileDialog.getOpenFileName(self.parent, 'Select an MP3 File', '', MP3_FILE_FILTER)
        if file_path:
            print(f'Selected file: {file_path}')

class ColorTriggerUI(TriggerUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.trigger_type = TriggerType.COLOR
        self.combo_box_counter_1 = 1
        self.combo_box_counter_2 = 1
        self.setup_ui()

    def setup_ui(self):
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

        self.add_combo_box_button = QPushButton('+')
        self.add_combo_box_button.clicked.connect(lambda: self.add_combo_box(True))

        color_trigger_widget = QWidget()
        color_trigger_layout = QVBoxLayout()
        color_trigger_layout.addLayout(combo_boxes_layout)
        color_trigger_layout.addWidget(self.add_combo_box_button)
        color_trigger_widget.setLayout(color_trigger_layout)

        return color_trigger_widget

    def toggle_visibility(self, visible):
        count1 = self.combo_box_layout_1.count()
        count2 = self.combo_box_layout_2.count()
        for i in range(count1):
            widget = self.combo_box_layout_1.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(visible)
        for i in range(count2):
            widget = self.combo_box_layout_2.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(visible)

    @pyqtSlot(bool)  # Explicitly specify the parameter type
    def add_combo_box(self, checked):  # Accept the boolean parameter
        combo_box_1 = QComboBox()
        combo_box_1.addItems([color.value for color in ColorType])
        self.combo_box_layout_1.addWidget(combo_box_1)
        self.combo_box_counter_1 += 1

        combo_box_2 = QComboBox()
        combo_box_2.addItems([colorEffect.value for colorEffect in EffectType])
        self.combo_box_layout_2.addWidget(combo_box_2)
        self.combo_box_counter_2 += 1

class TimeTriggerUI(TriggerUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.trigger_type = TriggerType.TIME
        self.combo_box_counter_1 = 1
        self.combo_box_counter_2 = 1
        self.combo_box_counter_3 = 1
        self.video_path = None
        self.setup_ui()

    def setup_ui(self):
        self.video_button = QPushButton('Select Video File')
        self.video_path_text = QLabel('No video selected')

        self.combo_box_layout_1 = QVBoxLayout()
        self.combo_box_layout_2 = QVBoxLayout()
        self.combo_box_layout_3 = QVBoxLayout()
        combo_boxes_layout = QHBoxLayout()

        self.combo_box_label_1 = QLabel('Timestamp')
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat('hh:mm:ss')
        self.combo_box_layout_1.addWidget(self.combo_box_label_1)
        self.combo_box_layout_1.addWidget(self.time_edit)

        self.combo_box_label_2 = QLabel('Duration')
        self.duration_edit = QTimeEdit()
        self.duration_edit.setDisplayFormat('hh:mm:ss')
        self.combo_box_layout_2.addWidget(self.combo_box_label_2)
        self.combo_box_layout_2.addWidget(self.duration_edit)

        self.combo_box_label_3 = QLabel('Effect triggered')
        self.combo_box_3 = QComboBox()
        self.combo_box_3.addItems([effect.value for effect in EffectType])
        self.combo_box_layout_3.addWidget(self.combo_box_label_3)
        self.combo_box_layout_3.addWidget(self.combo_box_3)

        combo_boxes_layout.addLayout(self.combo_box_layout_1)
        combo_boxes_layout.addLayout(self.combo_box_layout_2)
        combo_boxes_layout.addLayout(self.combo_box_layout_3)

        self.add_combo_box_button = QPushButton('+')
        self.add_combo_box_button.clicked.connect(lambda: self.add_combo_box(True))

        time_trigger_widget = QWidget()
        time_trigger_layout = QVBoxLayout()
        time_trigger_layout.addWidget(self.video_button)
        time_trigger_layout.addWidget(self.video_path_text)
        time_trigger_layout.addLayout(combo_boxes_layout)
        time_trigger_layout.addWidget(self.add_combo_box_button)
        time_trigger_widget.setLayout(time_trigger_layout)

        self.video_button.clicked.connect(lambda: self.select_video_file(True))

        return time_trigger_widget

    def toggle_visibility(self, visible):
        self.video_button.setVisible(visible)
        self.video_path_text.setVisible(visible)

        count1 = self.combo_box_layout_1.count()
        count2 = self.combo_box_layout_2.count()
        count3 = self.combo_box_layout_3.count()
        for i in range(count1):
            widget = self.combo_box_layout_1.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(visible)
        for i in range(count2):
            widget = self.combo_box_layout_2.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(visible)
        for i in range(count3):
            widget = self.combo_box_layout_3.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(visible)

    def convert_duration(self, duration_milliseconds):
        """Converts a duration in milliseconds to HH:MM:SS format."""
        seconds = int(duration_milliseconds / 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    @pyqtSlot(bool)
    def select_video_file(self, checked):
        file_path, _ = QFileDialog.getOpenFileName(self.parent, 'Select a Video File', '', 'Video files (*.mp4)')
        if file_path:
            print(f'Selected file: {file_path}')
            self.video_path = file_path
            media_info = MediaInfo.parse(file_path)
            duration = media_info.tracks[0].duration
            formatted_duration = self.convert_duration(duration)
            print(f"Duration: {formatted_duration}")
            self.video_path_text.setText(file_path + f" ({formatted_duration})")
            self.time_edit.setMaximumTime(QTime(0, 0, 0).addSecs(duration // 1000))

    @pyqtSlot(bool)
    def add_combo_box(self, checked):
        time_edit = QTimeEdit()
        time_edit.setDisplayFormat('hh:mm:ss')
        self.combo_box_layout_1.addWidget(time_edit)
        self.combo_box_counter_1 += 1

        duration_edit = QTimeEdit()
        duration_edit.setDisplayFormat('hh:mm:ss')
        self.combo_box_layout_2.addWidget(duration_edit)
        self.combo_box_counter_2 += 1

        combo_box_3 = QComboBox()
        combo_box_3.addItems([effect.value for effect in EffectType])
        self.combo_box_layout_3.addWidget(combo_box_3)
        self.combo_box_counter_3 += 1

class TriggerUIFactory:
    @staticmethod
    def create_trigger_ui(trigger_type, parent):
        if trigger_type == TriggerType.SOUND:
            return SoundTriggerUI(parent)
        elif trigger_type == TriggerType.COLOR:
            return ColorTriggerUI(parent)
        elif trigger_type == TriggerType.TIME:
            return TimeTriggerUI(parent)
        else:
            raise ValueError(f"Invalid trigger type: {trigger_type}")

class TriggerInputForm(QWidget):
    def __init__(self):
        super().__init__()
        self.video_path = None
        self.video_duration = None
        self.trigger_ui = None
        self.trigger_input_widget = QWidget()
        self.load_experiences()
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.column_layout = QHBoxLayout()

        # # Set the minimum size of the form
        self.setMinimumSize(700, 500)
        self.column_layout.setContentsMargins(20, 20, 20, 20)  # Adjust the margins of the main layout
        
        # Title Label
        title_label = QLabel('Open-Illumiroom Experience Creator')
        title_label.setAlignment(Qt.AlignCenter)
        title_font = title_label.font()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setMargin(0)
        title_label.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(title_label)

        # Set the font size for the form
        font = self.font()
        font.setPointSize(15)
        self.setFont(font)

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
        trigger_settings_layout.addWidget(self.trigger_input_widget)
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
        self.column_layout.addLayout(left_column_layout)
        self.column_layout.addLayout(right_column_layout)

        # Set spacing between widgets
        self.main_layout.setSpacing(0)
        self.column_layout.setSpacing(30)
        left_column_layout.setSpacing(20)
        right_column_layout.setSpacing(20)
        effect_layout.setSpacing(25)
        trigger_layout.setSpacing(20)

        self.main_layout.addLayout(self.column_layout)

        self.setLayout(self.main_layout)

        # Signal-Slot Connections
        self.trigger_combo.currentTextChanged.connect(self.toggle_trigger_input)
        self.submit_button.clicked.connect(self.on_submit_form)

        # Set initial trigger input visibility
        self.toggle_trigger_input(TriggerType.SOUND.value)

        self.setWindowTitle('Trigger Input Menu')

    def run_program(self):
        subprocess.Popen(['dist/new_trigger_menu.exe'])

    def toggle_trigger_input(self, trigger_type):
        trigger_type = TriggerType(trigger_type)
        if self.trigger_ui:
            self.trigger_ui.toggle_visibility(False)
        self.trigger_ui = TriggerUIFactory.create_trigger_ui(trigger_type, self)
        trigger_input_widget = self.trigger_ui.setup_ui()

        # Clear the existing layout of self.trigger_input_widget
        layout = self.trigger_input_widget.layout()
        if layout:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        self.trigger_input_widget.setLayout(QVBoxLayout())
        self.trigger_input_widget.layout().addWidget(trigger_input_widget)

        self.trigger_ui.toggle_visibility(True)
        for radio_button in self.effect_radios.values():
            radio_button.setEnabled(trigger_type != TriggerType.COLOR)

    def get_selected_effect(self):
        for effect_type, radio_button in self.effect_radios.items():
            if radio_button.isChecked():
                return effect_type
        return None

    def get_trigger_sample(self, trigger_type):
        if trigger_type == TriggerType.SOUND:
            return {}
        elif trigger_type == TriggerType.COLOR:
            color_mapping = {}
            count = self.trigger_ui.combo_box_layout_1.count()
            for i in range(1, count):
                color_selection = self.trigger_ui.combo_box_layout_1.itemAt(i).widget()
                color_effect = self.trigger_ui.combo_box_layout_2.itemAt(i).widget()
                if color_selection is not None and color_effect is not None:
                    color = color_selection.currentText()
                    effect = color_effect.currentText()
                    color_mapping[color] = effect
            return {'colors': color_mapping}
        elif trigger_type == TriggerType.TIME:
            time_mapping = []
            count = self.trigger_ui.combo_box_layout_1.count()
            for i in range(1, count):
                timestamp = self.trigger_ui.combo_box_layout_1.itemAt(i).widget().text()
                duration = self.trigger_ui.combo_box_layout_2.itemAt(i).widget().text()
                effect = self.trigger_ui.combo_box_layout_3.itemAt(i).widget().currentText()
                time_mapping.append({'timestamp': timestamp, 'duration': duration, 'effect': effect})
            return {'time_mapping': time_mapping}
        else:
            return {}

    def load_experiences(self):
        try:
            with open(EXPERIENCE_FILE, 'r') as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.experiences = data.get('experiences', {})
                    self.selected_experience = data.get('selected_experience', '')
                    self.experience_names = list(self.experiences.keys())
                else:
                    # Assume data is a list of experiences
                    self.experiences = {exp['name']: exp for exp in data}
                    self.experience_names = list(self.experiences.keys())
                    self.selected_experience = ''
        except (FileNotFoundError, json.JSONDecodeError):
            self.experiences = {}
            self.selected_experience = ''
            self.experience_names = []

    @pyqtSlot()
    def on_submit_form(self):
        trigger_type = TriggerType(self.trigger_combo.currentText())
        trigger_name = self.name_edit.text().strip()
        effect_type = self.get_selected_effect()
        sample_value = self.get_trigger_sample(trigger_type)
        video_path = self.trigger_ui.video_path if hasattr(self.trigger_ui, 'video_path') else None

        if not trigger_name:
            QMessageBox.warning(self, "Warning", "Please enter a name.")
            return

        if not sample_value:
            QMessageBox.warning(self, "Warning", "Please provide a valid trigger sample.")
            return

        if trigger_type == TriggerType.TIME and not video_path:
            QMessageBox.warning(self, "Warning", "Please select a video file.")
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
                'video_path': video_path,
                **sample_value
            }

        self.experiences[trigger_name] = experience
        self.experience_names.append(trigger_name)
        self.save_experiences()
        self.clear_form()

    def save_experiences(self):
        try:
            with open(EXPERIENCE_FILE, 'w') as file:
                json.dump({
                    'selected_experience': self.selected_experience,
                    'experience_names': self.experience_names,
                    'experiences': self.experiences
                }, file, indent=4)
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Failed to save experiences: {e}")

    def clear_form(self):
        self.name_edit.clear()
        # self.trigger_ui.clear_ui()
        for radio_button in self.effect_radios.values():
            radio_button.setChecked(False)

        self.trigger_combo.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = TriggerInputForm()
    form.show()
    sys.exit(app.exec_())




    # def initUI(self):
    #     self.main_layout = QVBoxLayout()
    #     self.main_layout.setContentsMargins(20, 20, 20, 20)  # Adjust the margins of the main layout
    #     self.main_layout.setSpacing(10)

    #     # Set the minimum size of the form
    #     self.setMinimumSize(500, 300)

    #     # Set the font size for the form
    #     font = self.font()
    #     font.setPointSize(12)
    #     self.setFont(font)

    #     # Title Label
    #     title_label = QLabel('Open-Illumiroom Experience Creator')
    #     title_label.setAlignment(Qt.AlignCenter)
    #     title_font = title_label.font()
    #     title_font.setPointSize(18)
    #     title_font.setBold(True)
    #     title_label.setFont(title_font)
    #     self.main_layout.addWidget(title_label)

    #     # Create a new layout for left and right columns
    #     columns_layout = QHBoxLayout()
    #     columns_layout.setContentsMargins(0, 0, 0, 0)  # Remove the margins of the columns layout
    #     columns_layout.setSpacing(20)  # Adjust the spacing between columns

    #     # Left Column Layout
    #     left_column_layout = QVBoxLayout()
    #     left_column_layout.setContentsMargins(0, 0, 0, 0)  # Remove the margins of the left column layout
    #     left_column_layout.setSpacing(10)  # Reduce the spacing between widgets in the left column

    #     # Name Input
    #     name_layout = QHBoxLayout()
    #     self.name_label = QLabel('Enter Name')
    #     self.name_edit = QLineEdit()
    #     name_layout.addWidget(self.name_label)
    #     name_layout.addWidget(self.name_edit)
    #     left_column_layout.addLayout(name_layout)

    #     # Trigger Type
    #     trigger_layout = QHBoxLayout()
    #     self.trigger_label = QLabel('Trigger')
    #     self.trigger_combo = QComboBox()
    #     self.trigger_combo.addItems([trigger.value for trigger in TriggerType])
    #     trigger_layout.addWidget(self.trigger_label)
    #     trigger_layout.addWidget(self.trigger_combo)
    #     left_column_layout.addLayout(trigger_layout)

    #     # Trigger Settings Group
    #     trigger_settings_group = QGroupBox('Trigger Settings')
    #     trigger_settings_group.setStyleSheet('QGroupBox { background-color: #d9d9d9; }')
    #     trigger_settings_group.setStyleSheet('QGroupBox { border: 2px solid #d9d9d9; }')
    #     trigger_settings_layout = QVBoxLayout()
    #     trigger_settings_layout.addWidget(self.trigger_input_widget)
    #     trigger_settings_group.setLayout(trigger_settings_layout)
    #     left_column_layout.addWidget(trigger_settings_group)

    #     # Submit Button
    #     self.submit_button = QPushButton('Save')
    #     left_column_layout.addWidget(self.submit_button)

    #     # Right Column Layout
    #     right_column_layout = QVBoxLayout()
    #     right_column_layout.setContentsMargins(0, 0, 0, 0)  # Remove the margins of the right column layout
    #     right_column_layout.setSpacing(10)  # Reduce the spacing between widgets in the right column

    #     # Effects Group
    #     self.effects_group = QGroupBox('Effects')
    #     self.effects_group.setStyleSheet('QGroupBox { background-color: #d9d9d9; }')
    #     effect_layout = QVBoxLayout()
    #     self.effect_radios = {}
    #     for effect_type in EffectType:
    #         radio_button = QRadioButton(effect_type.value)
    #         self.effect_radios[effect_type] = radio_button
    #         effect_layout.addWidget(radio_button)
    #     self.effects_group.setLayout(effect_layout)
    #     right_column_layout.addWidget(self.effects_group)

    #     # Add effect button
    #     self.add_effect_button = QPushButton('Add Effect')
    #     self.add_effect_button.clicked.connect(self.run_program)
    #     right_column_layout.addWidget(self.add_effect_button)

    #     # Add left and right column layouts to the columns layout
    #     columns_layout.addLayout(left_column_layout)
    #     columns_layout.addLayout(right_column_layout)

    #     columns_layout.setSpacing(30)
    #     left_column_layout.setSpacing(20)
    #     right_column_layout.setSpacing(20)

    #     # Add the columns layout to a new widget
    #     columns_widget = QWidget()
    #     columns_widget.setLayout(columns_layout)

    #     # Add the columns widget to the main layout
    #     self.main_layout.addWidget(columns_widget)

    #     self.setLayout(self.main_layout)

    #     # Signal-Slot Connections
    #     self.trigger_combo.currentTextChanged.connect(self.toggle_trigger_input)
    #     self.submit_button.clicked.connect(self.on_submit_form)

    #     # Set initial trigger input visibility
    #     self.toggle_trigger_input(TriggerType.SOUND.value)

    #     self.setWindowTitle('Trigger Input Menu')