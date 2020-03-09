import Settings
import UI_Update
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

import os
import re


def Camera_update(self):
    Settings.AOI_X = self.xAxis_horizontalSlider.sliderPosition() / 100
    Settings.AOI_Y = self.xAxis_horizontalSlider.sliderPosition() / 100
    Settings.AOI_W = self.yAxis_horizontalSlider.sliderPosition() / 100
    Settings.AOI_H = self.yAxis_horizontalSlider.sliderPosition() / 100

    Settings.x_resolution = self.x_resolution_spinBox.value()
    Settings.y_resolution = self.y_resolution_spinBox.value()


def IST_Edit(self):
    Settings.sequence_name = self.imageTitle_lineEdit.text().replace(" ", "_")
    self.imageTitle_lineEdit.setText(Settings.sequence_name)
    Settings.full_dir = Settings.default_dir + "/" + Settings.sequence_name
    self.directory_label.setText(Settings.full_dir)

    if Settings.date not in Settings.sequence_name:
        self.addDate_pushButton.setEnabled(True)
    if(len(Settings.sequence_name) == 0):
        self.addDate_pushButton.setEnabled(False)
    UI_Update.validate_input(self)


def add_date(self):
    Settings.sequence_name = Settings.sequence_name + "_" + Settings.date
    self.imageTitle_lineEdit.setText(Settings.sequence_name)
    Settings.full_dir = Settings.default_dir + "/" + Settings.sequence_name
    self.directory_label.setText(Settings.full_dir)
    self.addDate_pushButton.setEnabled(False)


def ICI_Change(self):
    Settings.interval = self.ImageInterval_spinBox.value()
    UI_Update.validate_input(self)


def ISD_Change(self):
    Settings.duration = self.imageDuration_spinBox.value()
    UI_Update.validate_input(self)


def select_directory(self):
    m_directory = str(QFileDialog.getExistingDirectory(
        self, "Select Directory", '/media/pi'))
    if(len(m_directory) != 0):
        Settings.full_dir = m_directory + "/" + Settings.sequence_name
        self.directory_label.setText(Settings.full_dir)
    UI_Update.validate_input(self)


def Email_Change(self):
    valid = None
    if (len(self.Email_lineEdit.text())) > 7:
        valid = re.match(
            '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.Email_lineEdit.text())
    if (valid != None):
        self.emailConfirm_pushButton.setEnabled(True)
    else:
        self.emailConfirm_pushButton.setEnabled(False)
        self.emailDefault_pushButton.setEnabled(False)


def Email_Entered(self):
    Settings.email = self.Email_lineEdit.text()
    self.emailDefault_pushButton.setEnabled(True)
    UI_Update.validate_input(self)


def Save_Email(self):
    open("../_temp/save_data.txt", "w").close()

    file = open("../_temp/save_data.txt", "w")
    file.write(Settings.email)
    file.close()


def zoomSliderChange(self):
    self.xAxis_label.setText(
        "AXIS A: " + str(self.xAxis_horizontalSlider.sliderPosition() / 100))
    self.yAxis_label.setText(
        "AXIS B: " + str(self.yAxis_horizontalSlider.sliderPosition() / 100))


def img_format(self):
    if(self.JPG_radioButton.isChecked()):
        Settings.image_format = 1
    else:
        Settings.image_format = 0
