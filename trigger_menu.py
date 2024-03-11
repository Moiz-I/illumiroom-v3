import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QFileDialog, QGridLayout, QGroupBox, QRadioButton, QVBoxLayout
)
import json

experiences = []

class TriggerInputForm(QWidget):
    def __init__(self):
        super().__init__()
        self.colour_value = ""
        self.time_value = ""
        self.mp3_file_path = None
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        self.name_label = QLabel('Enter Name', self)
        self.name_edit = QLineEdit(self)
        grid.addWidget(self.name_label, 0, 0)
        grid.addWidget(self.name_edit, 0, 1)

        self.effects_group = QGroupBox('Effects')
        vbox = QVBoxLayout()

        self.light_snow_radio = QRadioButton('Lightning')
        self.medium_snow_radio = QRadioButton('Blur')
        self.harsh_snow_radio = QRadioButton('Rain')
        vbox.addWidget(self.light_snow_radio)
        vbox.addWidget(self.medium_snow_radio)
        vbox.addWidget(self.harsh_snow_radio)
        self.effects_group.setLayout(vbox)
        grid.addWidget(self.effects_group, 0, 2, 4, 1)

        self.trigger_label = QLabel('Trigger', self)
        self.trigger_combo = QComboBox(self)
        self.trigger_combo.addItem('Sound')
        self.trigger_combo.addItem('Colour')
        self.trigger_combo.addItem('Time')
        grid.addWidget(self.trigger_label, 2, 0)
        grid.addWidget(self.trigger_combo, 2, 1)

        self.mp3_button = QPushButton('Select MP3 File', self)
        self.colour_edit = QLineEdit(self)
        self.colour_edit.setPlaceholderText('Enter colour value')
        self.time_edit = QLineEdit(self)
        self.time_edit.setPlaceholderText('Enter time stamp')
        grid.addWidget(self.mp3_button, 3, 0, 1, 2)
        grid.addWidget(self.colour_edit, 3, 0, 1, 2)
        grid.addWidget(self.time_edit, 3, 0, 1, 2)
        self.mp3_button.setVisible(False)
        self.colour_edit.setVisible(False)
        self.time_edit.setVisible(False)

        self.submit_button = QPushButton('Save', self)
        self.submit_button.setEnabled(True)
        grid.addWidget(self.submit_button, 4, 0, 1, 2)

        self.setLayout(grid)

        self.mp3_button.clicked.connect(self.select_mp3_file)
        self.trigger_combo.currentIndexChanged.connect(self.on_trigger_combo_change)
        self.submit_button.clicked.connect(self.on_submit_form)
        self.colour_edit.textChanged.connect(self.on_colour_text_change)
        self.time_edit.textChanged.connect(self.on_time_text_change)  # Connect time edit text change signal

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Trigger Input Menu')

    def on_trigger_combo_change(self):
        trigger = self.trigger_combo.currentText()
        self.mp3_button.setVisible(trigger == 'Sound')
        self.colour_edit.setVisible(trigger == 'Colour')
        self.time_edit.setVisible(trigger == 'Time')

    def select_mp3_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select an MP3 File', '', 'MP3 files (*.mp3)')
        if file_path:
            print(f'Selected file: {file_path}')
            self.mp3_file_path = file_path
        else:
            print('No file was selected.')

    def on_colour_text_change(self):
        self.colour_value = self.colour_edit.text()

    def on_time_text_change(self):
        self.time_value = self.time_edit.text()

    def on_submit_form(self):
        selected_trigger = self.trigger_combo.currentText()
        trigger_name = self.name_edit.text()
        effect = 'None'  # Assume no effect is selected, since there is no effect_combo

        # Determine which radio button is checked
        if self.light_snow_radio.isChecked():
            effect = 'Lightning'
        elif self.medium_snow_radio.isChecked():
            effect = 'Blur'
        elif self.harsh_snow_radio.isChecked():
            effect = 'Rain'

        if selected_trigger == "Sound":
            sample_value = self.mp3_file_path
        elif selected_trigger == "Colour":
            sample_value = self.colour_edit.text()
        elif selected_trigger == "Time":
            sample_value = self.time_edit.text()
        else:
            sample_value = ""

        experience = {
            'effect': effect,
            'trigger_type': selected_trigger,
            'name': trigger_name,
            'sample': sample_value
        }

        experiences.append(experience)
        print(experiences)
        self.save_to_json()
        self.clear_form()
    
    def save_to_json(self): 
        with open('experience.json', 'w') as file: 
            json.dump(experiences, file, indent=4)

    def clear_form(self):
        self.name_edit.clear()
        self.mp3_file_path = None
        self.light_snow_radio.setChecked(False)
        self.medium_snow_radio.setChecked(False)
        self.harsh_snow_radio.setChecked(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TriggerInputForm()
    ex.show()
    sys.exit(app.exec_())