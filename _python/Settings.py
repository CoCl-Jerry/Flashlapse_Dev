import serial
import time
import UI_Update


def init(self):

    global base_Connected
    base_Connected = True

    try:
        global ASD
        ASD = serial.Serial('/dev/ttyS0', 9600)

    except:
        UI_Update.desync(self)

    global commands_list
    commands_list = []

    global send_commands_list
    send_commands_list = []

    global current_CMD
    current_CMD = ""

    global cycle_running
    cycle_running = False

    global cycle_time
    cycle_time = 60

    global sch_running
    sch_running = False

    global test_running
    test_running = False

    global clino_running
    clino_running = False

    global timelapse_running
    timelapse_running = False

    global dropbox_running
    dropbox_running = False

    global email_running
    email_running = False

    global angle_1
    angle_1 = 0
    global angle_2
    angle_2 = 0
    global delay_1
    delay_1 = 0
    global delay_2
    delay_2 = 0

    global rpm
    RPM = 5

    global rotation
    rotation = 2

    global AOI_X
    AOI_X = 0
    global AOI_Y
    AOI_Y = 0
    global AOI_W
    AOI_W = 1
    global AOI_H
    AOI_H = 1

    global livetime
    livetime = 1
    global x_res
    x_resolution = 2464
    global y_res
    y_resolution = 2464

    global sequence_name
    sequence_name = ""

    global default_dir
    default_dir = "/home/pi/Desktop"

    global full_dir
    full_dir = ""

    global date
    date = time.strftime('%m_%d_%Y')

    global interval
    interval = 10

    global duration
    duration = 1

    global total
    total = 6

    global image_format
    image_format = 1

    global current
    current = 0

    global email
    email = ""

    global storage_mode
    storage_mode = 0

    global file_list
    file_list = []

    global file
    file = ""

    global current_image
    current_image = ""

    global germinationColor
    germinationColor = 0

    global germinationDirection
    germinationDirection = 0

    global cycleTime
    cycleTime = 24

    global stripLength
    stripLength = 5

    global lightingPreset_mode
    lightingPreset_mode = 0

    global motionPreset_mode
    lightingPreset_mode = 0

    global lightingPreset_running
    lightingPreset_running = False

    global motionPreset_running
    motionPreset_running = False

    global cpuserial
    f = open('/proc/cpuinfo', 'r')
    for line in f:
        if line[0:6] == 'Serial':
            cpuserial = line[10:26]
    f.close()
    print(cpuserial)

    global link
    link = ""
