#######################################################
#     Spiros Daskalakis                               #
#     last Revision: 10/10/2022                       #
#     Python Version:  3.7                            #
#     Email: daskalakispiros@gmail.com                #
#######################################################

import serial
import time

link_serial = 'COM13'
print('Selected Port:', link_serial)
ser = serial.Serial(link_serial)  # open serial port
ser.baudrate = 115200
ser.timeout = None


def send_at(command, back, timeout):
    rec_buff = ''
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01)
        rec_buff = ser.read(ser.inWaiting())
    if back not in rec_buff.decode():
        print(command + ' ERROR')
        print(command + ' back:\t' + rec_buff.decode())
        return 0
    else:
        print(rec_buff.decode())
        return 1


if __name__ == "__main__":
    data = "Check the connection of the MODEM"
    print(data)

    # Check COMMAND response
    at_command = 'AT'
    at_expected_answer = 'OK'
    at_answer = send_at(at_command, at_expected_answer, 2)
