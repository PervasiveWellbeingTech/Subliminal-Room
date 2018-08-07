import libs
import serial
import platform
import zephyr
import time
from zephyr.testing import simulation_workflow


def callback(value_name, value):
    pass
    # if value_name =
    # print('({}: {})'.format(value_name, value))

def main():
    serial_port_dict = {"Darwin": "/dev/tty.BHBHT022509-iSerialPort1",
                        "Windows": 23}

    serial_port = serial_port_dict[platform.system()]
    ser = serial.Serial(serial_port) #establish serial connection
    # time.sleep(10)
    simulation_workflow([callback], ser)



if __name__ == "__main__":
    main()
