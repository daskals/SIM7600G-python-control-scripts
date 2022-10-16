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
rec_buff = ''

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


def SendShortMessage(phone_number, text_message):
    print("Setting SMS mode...")
    send_at("AT+CMGF=1", "OK", 1)
    print("Sending Short Message")
    answer = send_at("AT+CMGS=\"" + phone_number + "\"", ">", 2)
    if 1 == answer:
        ser.write(text_message.encode())
        ser.write(b'\x1A')
        answer = send_at('', 'OK', 20)
        if 1 == answer:
            print('send successfully')
        else:
            print('error')
    else:
        print('error%d' % answer)


def ReceiveShortMessage():
    rec_buff = ''
    print('Setting SMS mode...')
    send_at('AT+CMGF=1', 'OK', 1)
    send_at('AT+CPMS=\"SM\",\"SM\",\"SM\"', 'OK', 1)
    answer = send_at('AT+CMGR=1', '+CMGR:', 2)
    if 1 == answer:
        answer = 0
        if 'OK' in rec_buff:
            answer = 1
            print(rec_buff)
    else:
        print('error%d' % answer)
        return False
    return True



if __name__ == "__main__":

    phone_number = '00447783153933'  # ********** change it to the phone number you want to call
    text_message = '101'
    # print('Sending Short Message Test:')
    # SendShortMessage(phone_number, text_message)
    print('Receive Short Message Test:\n')
    print('Please send message to phone ' + phone_number)
    ReceiveShortMessage()


