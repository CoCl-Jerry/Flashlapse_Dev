import Settings
import UI_Update
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from time import sleep


def light_confirm(self):
    current_CMD = str((self.Start_spinBox.value() - 1)) + "~" + str((self.End_spinBox.value() - 1)) + "~" + str(self.R_spinBox.value()) + "~" + str(
        self.G_spinBox.value()) + "~" + str(self.B_spinBox.value()) + "~" + str(self.W_spinBox.value()) + "~" + str(self.BRT_spinBox.value()) + "\n4\n"
    Settings.commands_list.append("3~" + current_CMD)
    Settings.ASD.write(bytes("1~" + current_CMD, 'UTF-8'))


def light_reset(self):
    current_CMD = "0\n"
    send_CMD(current_CMD)

    self.R_spinBox.setValue(0)
    self.G_spinBox.setValue(0)
    self.B_spinBox.setValue(0)
    self.W_spinBox.setValue(0)
    self.Start_spinBox.setValue(1)
    self.End_spinBox.setValue(20)
    self.BRT_spinBox.setValue(20)

    Settings.commands_list.clear()


def clear_lights():
    current_CMD = "0\n"
    send_CMD(current_CMD)


def deploy_lights(temp_list):
    for x in temp_list:
        send_CMD(x)
    current_CMD = "4\n"
    send_CMD(current_CMD)


def clinoStart(self):
    if not Settings.clino_running:
        Settings.clino_running = True
        current_CMD = "7\n"
        send_CMD(current_CMD)
        self.clinostatSet_pushButton.setText("Stop Clinostat")

    else:
        Settings.clino_running = False
        current_CMD = "\n"
        send_CMD(current_CMD)
        self.clinostatSet_pushButton.setText("Set Clinostat")


def send_CMD(CMD):
    print(CMD)
    Settings.ASD.write(bytes(CMD, 'UTF-8'))


def disco_run(self):
    Settings.commands_list.clear()
    current_CMD = "2~0~" + str(self.disco_spinBox.value()) + "\n"
    Settings.commands_list.append(current_CMD)
    send_CMD(current_CMD)


def rainbow_run(self):
    Settings.commands_list.clear()
    current_CMD = "2~1~" + str(self.rainbow_spinBox.value()) + "\n"
    Settings.commands_list.append(current_CMD)
    send_CMD(current_CMD)


def sundial_run(self):
    Settings.commands_list.clear()
    current_CMD = "2~2~" + str(self.sundial_spinBox.value() * 1000) + "\n"
    Settings.commands_list.append(current_CMD)
    send_CMD(current_CMD)


def pulse_run(self):
    Settings.commands_list.clear()
    current_CMD = "2~3~" + str(self.pulse_spinBox.value()) + "\n"
    Settings.commands_list.append(current_CMD)
    send_CMD(current_CMD)


def motorSliderChange(self):
    Settings.RPM = self.motorSpeed_slider.sliderPosition() / 10
    self.motorSpeed_label.setText("Motor RPM: " + str(Settings.RPM))


def motorSliderRelease(self):
    current_CMD = "6~" + str(int(60 / (2.038 * Settings.RPM))) + "\n"
    send_CMD(current_CMD)


def motor_rotate(deg):
    current_CMD = "8~" + str(deg) + "\n"
    send_CMD(current_CMD)
