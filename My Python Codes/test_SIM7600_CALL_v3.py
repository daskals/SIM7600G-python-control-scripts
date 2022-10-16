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
        return rec_buff.decode()


def modem_reset():
    print('RESET MODULE')
    send_at("AT+CRESET", 'OK', 2)


def modem_init(pin):
    # Check COMMAND response
    at_command = 'AT'
    at_expected_answer = 'OK'
    at_answer = send_at(at_command, at_expected_answer, 2)

    at_command = 'AT+CSQ'
    # This command is used to return received signal strength indication <rssi> and channel bit error rate <ber>
    # from the ME. Test command returns values supported by the TA as compound values.
    at_expected_answer = 'OK'
    at_answer = send_at(at_command, at_expected_answer, 2)
    # < rssi >
    # 0 – - 113 dBm or less
    # 1 – - 111 dBm
    # 2...30 – - 109... - 53 dBm
    # 31 – - 51 dBm or greater
    # 99 – not known or not detectable
    # 100 – - 116 dBm or less
    # 101 – - 115 dBm
    # 102…191 – - 114... - 26dBm
    # 191 – - 25 dBm or greater
    # 199 – not known or not detectable
    # 100…199 – expand to TDSCDMA, indicate RSCP received

    # BER (in percent)
    # 0 – <0.01%
    # 1 – 0.01% --- 0.1%
    # 2 – 0.1% --- 0.5%
    # 3 – 0.5% --- 1.0%
    # 4 – 1.0% --- 2.0%
    # 5 – 2.0% --- 4.0%
    # 6 – 4.0% --- 8.0%
    # 7 – >=8.0%
    # 99 – not known or not detectable
    if at_answer != 0:
        at_answer = at_answer.replace(': ', ',')
        print('RSSI: ', at_answer.split(',')[1])
        print('BER: ', at_answer.split(',')[2])
    else:
        modem_reset()

    if pin == '':
        at_command = 'AT+CPIN?'
        # This command is used to send the ME a password which is necessary before it can be operated (SIM PIN,
        # SIM PUK, PH-SIM PIN, etc.)
    elif pin != '':
        at_command = 'AT+CPIN=' + pin

    at_expected_answer = 'OK'
    at_answer = send_at(at_command, at_expected_answer, 2)
    if at_answer != 0:
        print('CPIN? STATUS: ', at_answer)
    else:
        modem_reset()

    at_command = 'AT+CREG?'
    # This command is used to control the presentation of an unsolicited result code +CREG: <stat> when <n>=1
    # and there is a change in the ME network registration status, or code +CREG: <stat>[,<lac>,<ci>] when
    # <n>=2 and there is a change of the network cell.
    # 1 registered, home network.
    # 2 not registered, but ME is currently searching a new operator to
    # register to.
    # 3 registration denied.
    # 4 unknown.
    # 5 registered, roaming.
    # 6 registered for "SMS only", home network (applicable only when E-UTRAN)
    at_expected_answer = '+CREG: 0,5'
    at_expected_answer = 'OK'
    at_answer = send_at(at_command, at_expected_answer, 2)
    if at_answer != 0:
        print('Result code +CREG: ', at_answer)
    else:
        modem_reset()

    at_command = 'AT+CPSI?\r\n'
    # This command is used to return the UE system information.
    # If camping on a lte cell:
    # +CPSI: <System Mode>,<Operation Mode>[,<MCC>-<MNC>,<TA
    # C>,<SCellID>,<PCellID>,<Frequency Band>,<earfcn>,<dlbw>,<
    # ulbw>,<RSRQ>,<RSRP>,<RSSI>,<RSSNR>]


    at_expected_answer = 'OK'
    at_answer = send_at(at_command, at_expected_answer, 2)
    at_answer = at_answer.replace(': ', ',')

    if at_answer != 0:
        print('---------UE system information--------------')
        print('System Mode: ', at_answer.split(',')[1])
        print('Operation Mode: ', at_answer.split(',')[2])
        print('Mobile Country Code (MCC): ', at_answer.split(',')[3])
        print('Mobile Network Code (MNC): ', at_answer.split(',')[3])
        print('Tracing Area Code (TAC): ', at_answer.split(',')[4])
        print('Cell ID in decimal format for serving cell (SCellID): ', at_answer.split(',')[5])
        print('Physical Cell ID  (PCellID): ', at_answer.split(',')[6])
        print('Frequency Band: ', at_answer.split(',')[7])
        print('E-UTRA absolute radio frequency channel number for searching LTE cells (earfcn): ',
              at_answer.split(',')[8])
        print('Transmission bandwidth configuration of the serving cell on the downlink  (dlbw): ',
              at_answer.split(',')[9])
        print('Transmission bandwidth configuration of the serving cell on the uplink  (ulbw): ',
              at_answer.split(',')[10])
        print('Current reference signal receive quality as measured by L1 (RSRQ): ', at_answer.split(',')[11])
        print('Current reference signal received power in -1/10 dBm. Available for LTE (RSRP): ',
              at_answer.split(',')[12])
        print('RSSI: ', at_answer.split(',')[13])
        print('Average reference signal signal-to-noise ratio of the serving cel (RSSNR): ', at_answer.split(',')[14])
    else:
        modem_reset()



def make_call(phone_number):
    while True:
        send_at('ATD' + phone_number + ';', 'OK', 1)
        time.sleep(20)
        ser.write('AT+CHUP\r\n'.encode())
        print('Call disconnected')


if __name__ == "__main__":
    phone_number = '00447783153933'  # ********** change it to the phone number you want to call
    text_message = '101'
    modem_init(pin='')
    make_call(phone_number)
