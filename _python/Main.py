# import basic libraries
import sys
import time

#import settings
import Settings

# import custom functions
import Commands
import Threads
import Functions

# import UI functions
import UI_Update

# import Qt content
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

# import generated UI
import FlashLapse_UI

#global variables
default_dir = "/home/pi/Desktop"
date = time.strftime('%m_%d_%Y')

# create class for Raspberry Pi GUI


class MainWindow(QMainWindow, FlashLapse_UI.Ui_MainWindow):

    def start_cycle(self):
        if not Settings.cycle_running:
            try:
                Settings.cycle_time = self.powerCycle_spinBox.value()

                self.Cycle_Thread = Threads.Cycle()
                self.Cycle_Thread.started.connect(
                    lambda: UI_Update.cycle_update(self))
                self.Cycle_Thread.start()

            except Exception as e:
                print(e)
        else:
            Settings.cycle_running = False
            UI_Update.cycle_update(self)

    def schedule_test(self):
        if not Settings.test_running:
            try:
                Settings.angle_1 = self.rotate1_spinbox.value()
                Settings.angle_2 = self.rotate2_spinbox.value()
                self.Test_Thread = Threads.Test()
                self.Test_Thread.started.connect(
                    lambda: UI_Update.test_update(self))
                self.Test_Thread.finished.connect(
                    lambda: UI_Update.test_update(self))
                self.Test_Thread.start()
            except Exception as e:
                print(e)
        else:
            Settings.test_running = False
            UI_Update.test_update(self)

    def schedule_run(self):
        if not Settings.sch_running:
            try:
                Settings.angle_1 = self.rotate1_spinbox.value()
                Settings.angle_2 = self.rotate2_spinbox.value()
                Settings.delay_1 = self.wait1_spinbox.value()
                Settings.delay_2 = self.wait2_spinbox.value()

                self.Schedule_Thread = Threads.Schedule()
                self.Schedule_Thread.started.connect(
                    lambda: UI_Update.schedule_update(self))
                self.Schedule_Thread.start()
            except Exception as e:
                print(e)
        else:
            Settings.sch_running = False
            UI_Update.schedule_update(self)

    def start_snapshot(self):
        try:
            Functions.Camera_update(self)
            self.Snap_Thread = Threads.Snap()
            self.Snap_Thread.started.connect(
                lambda: UI_Update.imaging_disable(self))
            self.Snap_Thread.finished.connect(
                lambda: UI_Update.update_frame_snap(self, "../_temp/snapshot.jpg"))
            self.Snap_Thread.start()

        except Exception as e:
            print(e)

    def start_livefeed(self):
        try:
            Settings.livetime = self.liveFeed_spinBox.value()
            self.livefeed_Thread = Threads.Live()
            self.livefeed_Thread.started.connect(
                lambda: UI_Update.imaging_disable(self))
            self.livefeed_Thread.finished.connect(
                lambda: UI_Update.imaging_enable(self))
            self.livefeed_Thread.start()

        except Exception as e:
            print(e)

    def start_preview(self):
        try:
            Functions.Camera_update(self)
            self.Preview_Thread = Threads.Preview()
            self.Preview_Thread.started.connect(
                lambda: UI_Update.imaging_disable(self))
            if(Settings.image_format):
                self.Preview_Thread.finished.connect(
                    lambda: UI_Update.update_frame_alt(self, "../_temp/preview.jpg"))
            else:
                self.Preview_Thread.finished.connect(
                    lambda: UI_Update.update_frame_alt(self, "../_temp/preview.png"))
            self.Preview_Thread.start()

        except Exception as e:
            print(e)

    def rotate_image(self):
        try:
            Functions.Camera_update(self)
            Settings.rotation += 1
            self.Snap_Thread = Threads.Snap()
            self.Snap_Thread.started.connect(
                lambda: UI_Update.imaging_disable(self))
            self.Snap_Thread.finished.connect(
                lambda: UI_Update.update_frame(self, "../_temp/snapshot.jpg"))
            self.Snap_Thread.start()

        except Exception as e:
            print(e)

    def start_sequence(self):

        if(Settings.image_format):
            Settings.file = Settings.full_dir + "/" + Settings.sequence_name + "_%04d.jpg"
        else:
            Settings.file = Settings.full_dir + "/" + Settings.sequence_name + "_%04d.png"
        self.Progress_Bar.setMaximum(Settings.total)

        try:
            if not Settings.timelapse_running:
                Functions.Camera_update(self)

                self.Imaging_Thread = Threads.Image()
                self.Imaging_Thread.started.connect(
                    lambda: UI_Update.timelapse_disable(self))
                self.Imaging_Thread.finished.connect(
                    lambda: UI_Update.timelapse_enable(self))
                self.Imaging_Thread.capturing.connect(
                    lambda: UI_Update.imaging_disable(self))
                self.Imaging_Thread.complete.connect(
                    lambda: UI_Update.update_frame(self, Settings.current_image))
                self.Imaging_Thread.start()
            else:
                Settings.timelapse_running = False
                UI_Update.timelapse_enable(self)

        except Exception as e:
            print(e)

        if(Settings.storage_mode):
            try:
                self.Dropbox_Thread = Threads.Dropbox()
                self.Dropbox_Thread.start()

                self.Email_Thread = Threads.Email()
                self.Email_Thread.start()

            except Exception as e:
                print(e)
 # access variables inside of the UI's file

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file
        Settings.init(self)
        Commands.startup()

        fh = open("../_temp/save_data.txt", "r")
        self.Email_lineEdit.setText(fh.readline())
        fh.close
        Settings.email = self.Email_lineEdit.text()

        self.Start_spinBox.valueChanged.connect(
            lambda: UI_Update.LED_validate(self))
        self.End_spinBox.valueChanged.connect(
            lambda: UI_Update.LED_validate(self))

        self.lightConfirm_pushButton.clicked.connect(
            lambda: Commands.light_confirm(self))
        self.lightReset_pushButton.clicked.connect(
            lambda: Commands.light_reset(self))

        self.disco_pushButton.clicked.connect(lambda: Commands.disco_run(self))
        self.rainbow_pushButton.clicked.connect(
            lambda: Commands.rainbow_run(self))
        self.sundial_pushButton.clicked.connect(
            lambda: Commands.sundial_run(self))
        self.pulse_pushButton.clicked.connect(lambda: Commands.pulse_run(self))

        self.confirmCycle_pushButton.clicked.connect(
            lambda: self.start_cycle())

        self.schedulerTest_pushButton.clicked.connect(
            lambda: self.schedule_test())
        self.schedulerSet_pushButton.clicked.connect(
            lambda: self.schedule_run())
        self.motorSpeed_slider.valueChanged.connect(
            lambda: Commands.motorSliderChange(self))
        self.motorSpeed_slider.sliderReleased.connect(
            lambda: Commands.motorSliderRelease(self))

        self.clinostatSet_pushButton.clicked.connect(
            lambda: Commands.clinoStart(self))
        self.snapshot_pushButton.clicked.connect(lambda: self.start_snapshot())
        self.liveFeed_pushButton.clicked.connect(lambda: self.start_livefeed())
        self.preview_pushButton.clicked.connect(lambda: self.start_preview())
        self.x_resolution_spinBox.valueChanged.connect(
            lambda: self.update_resolution())
        self.y_resolution_spinBox.valueChanged.connect(
            lambda: self.update_resolution())
        self.rotate_pushButton.clicked.connect(lambda: self.rotate_image())

        self.xAxis_horizontalSlider.valueChanged.connect(
            lambda: Functions.zoomSliderChange(self))
        self.xAxis_horizontalSlider.sliderReleased.connect(
            lambda: self.start_snapshot())

        self.yAxis_horizontalSlider.valueChanged.connect(
            lambda: Functions.zoomSliderChange(self))
        self.yAxis_horizontalSlider.sliderReleased.connect(
            lambda: self.start_snapshot())

        self.motorConfirm_pushButton.clicked.connect(
            lambda: Commands.motor_rotate(self.motor_spinBox.value()))

        self.imageTitle_lineEdit.textChanged.connect(
            lambda: Functions.IST_Edit(self))
        self.addDate_pushButton.clicked.connect(
            lambda: Functions.add_date(self))
        self.ImageInterval_spinBox.valueChanged.connect(
            lambda: Functions.ICI_Change(self))
        self.imageDuration_spinBox.valueChanged.connect(
            lambda: Functions.ISD_Change(self))
        self.directory_pushButton.clicked.connect(
            lambda: Functions.select_directory(self))

        self.Email_lineEdit.textChanged.connect(
            lambda: Functions.Email_Change(self))
        self.emailConfirm_pushButton.clicked.connect(
            lambda: Functions.Email_Entered(self))
        self.emailDefault_pushButton.clicked.connect(
            lambda: Functions.Save_Email(self))

        self.storage_tabWidget.currentChanged.connect(
            lambda: UI_Update.validate_input(self))
        self.startRoutines_pushButton.clicked.connect(
            lambda: self.start_sequence())

        self.JPG_radioButton.toggled.connect(
            lambda: Functions.img_format(self))
        self.PNG_radioButton.toggled.connect(
            lambda: Functions.img_format(self))

        self.lightingPreset_pushButton.clicked.connect(
            lambda: Functions.start_lighting_preset(self))
        # self.MotionPreset_pushButton.clicked.connect(
        # lambda: self.start_motion_preset())


# main function
def main():
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()

    # without this, the script exits immediately.
    sys.exit(app.exec_())


# python bit to figure how who started This
if __name__ == "__main__":
    main()
