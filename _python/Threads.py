import Settings
import Commands
import os
import sys
import subprocess
import smtplib
import Adafruit_DHT

from PyQt5 import QtCore
from time import sleep
from PyQt5.QtCore import QThread
from picamera import PiCamera


class Cycle(QThread):

    def __init__(self):
        QThread.__init__(self)
        Settings.cycle_running = True

    def __del__(self):
        self._running = False

    def run(self):

        Commands.clear_lights()
        sleep(1)

        while Settings.cycle_running:

            Commands.deploy_lights(Settings.commands_list)

            for x in range(Settings.cycle_time * 60):
                sleep(1)
                if not Settings.cycle_running:
                    break

            if Settings.cycle_running:
                Commands.clear_lights()

            for x in range(Settings.cycle_time * 60):
                sleep(1)
                if not Settings.cycle_running:
                    break


class MPreset(QThread):

    def __init__(self):
        QThread.__init__(self)
        Settings.motionPreset_running = True

    def __del__(self):
        self._running = False

    def run(self):

        while Settings.motionPreset_running:
            if not Settings.motionPreset_mode:
                Commands.clear_lights()
                Settings.current_CMD = "1~5~15~0~0~0~255~100\n4\n"
                Commands.send_CMD(Settings.current_CMD)

                for x in range(Settings.gravitropism_wait * 60):
                    for x in range(60):
                        sleep(1)
                        if not Settings.motionPreset_running:
                            break
                    if not Settings.motionPreset_running:
                        break
                if Settings.motionPreset_running:
                    Commands.motor_rotate(90)
                    Commands.clear_lights()
                    Settings.current_CMD = "1~0~10~0~0~0~255~100\n4\n"
                    Commands.send_CMD(Settings.current_CMD)
                    Settings.motionPreset_running = False
            else:
                for x in range(Settings.rotateDelay * 60):
                    for x in range(60):
                        sleep(1)
                        if not Settings.motionPreset_running:
                            break
                    if not Settings.motionPreset_running:
                        break
                if Settings.motionPreset_running:
                    Commands.motor_rotate(Settings.rotateAmount)
                    Settings.motionPreset_running = False


class Schedule(QThread):

    def __init__(self):
        QThread.__init__(self)
        Settings.sch_running = True

    def __del__(self):
        self._running = False

    def run(self):
        while Settings.sch_running:
            if Settings.sch_running:
                Commands.motor_rotate(Settings.angle_1)
            for x in range(Settings.delay_1 * 60):
                sleep(1)
                if not Settings.sch_running:
                    break
            if Settings.sch_running:
                Commands.motor_rotate(Settings.angle_2)
            for x in range(Settings.delay_2 * 60):
                sleep(1)
                if not Settings.sch_running:
                    break


class Test(QThread):

    def __init__(self):
        QThread.__init__(self)
        Settings.test_running = True

    def __del__(self):
        self._running = False

    def run(self):
        for x in range(5):
            if Settings.test_running:
                Commands.motor_rotate(Settings.angle_1)
            for x in range(5):
                sleep(1)
                if not Settings.test_running:
                    break

            if Settings.test_running:
                Commands.motor_rotate(Settings.angle_2)
            for x in range(5):
                sleep(1)
                if not Settings.test_running:
                    break
            if not Settings.test_running:
                break


class Snap(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        with PiCamera() as camera:
            camera.zoom = (Settings.AOI_X, Settings.AOI_Y,
                           Settings.AOI_W, Settings.AOI_H)
            camera.resolution = (390, 390)
            camera._set_rotation(90 * Settings.rotation)
            camera.capture("../_temp/snapshot.jpg")


class Live(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        with PiCamera() as camera:
            camera._set_rotation(90 * Settings.rotation)
            camera.zoom = (Settings.AOI_X, Settings.AOI_Y,
                           Settings.AOI_W, Settings.AOI_H)
            camera.resolution = (Settings.x_resolution, Settings.y_resolution)
            camera.start_preview()
            sleep(Settings.livetime)


class Preview(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        with PiCamera() as camera:
            camera.zoom = (Settings.AOI_X, Settings.AOI_Y,
                           Settings.AOI_W, Settings.AOI_H)
            camera.resolution = (Settings.x_resolution, Settings.y_resolution)

            camera._set_rotation(90 * Settings.rotation)

            if(Settings.image_format):
                camera.capture("../_temp/preview.jpg")
            else:
                camera.capture("../_temp/preview.png")


class Image(QThread):
    capturing = QtCore.pyqtSignal()
    complete = QtCore.pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        Settings.timelapse_running = True

    def __del__(self):
        self._running = False

    def run(self):
        if(not os.path.isdir(Settings.full_dir)):
            original_umask = os.umask(0)
            os.mkdir(Settings.full_dir, mode=0o777)
            os.umask(original_umask)
        for i in range(Settings.total):
            Settings.current = i
            sleep(0.2)
            Settings.current_image = Settings.file % i
            self.capturing.emit()
            with PiCamera() as camera:
                sleep(0.8)
                camera.zoom = (Settings.AOI_X, Settings.AOI_Y,
                               Settings.AOI_W, Settings.AOI_H)
                camera.resolution = (Settings.x_resolution,
                                     Settings.y_resolution)
                camera._set_rotation(90 * Settings.rotation)
                camera.capture(Settings.current_image)
            self.complete.emit()

            if(Settings.storage_mode):
                Settings.file_list.append(Settings.current_image)

            for x in range(Settings.interval - 1):
                sleep(1)
                if not Settings.timelapse_running:
                    break
            if not Settings.timelapse_running:
                break
        Settings.timelapse_running = False


class Sensor(QThread):
    update = QtCore.pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):

        while True:
            Settings.humidity, Settings.temperature = Adafruit_DHT.read_retry(
                Settings.DHT_SENSOR, 18)
            if Settings.humidity is not None and Settings.temperature is not None:
                self.update.emit()
            sleep(1)
