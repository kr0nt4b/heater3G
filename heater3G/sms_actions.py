import time


def send_sms(recipient, message):
    time.sleep(1)
    ser.write(bytearray('ATZ\r'))
    time.sleep(1)
    ser.write(bytearray('AT+CMGF=1\r'))
    time.sleep(1)
    ser.write('''AT+CMGS="''' + recipient + '''"\r\n''')
    time.sleep(1)
    ser.write(message + "\r\n")
    time.sleep(1)
    ser.write(bytearray(chr(26)))
    time.sleep(1)
    reply = ser.readline()
    print(reply)
    print("message sent!")


def listen_for_sms():
    ser.write(bytearray('"AT+CMGF=1\r')) # set to text mode
    time.sleep(1)
    ser.write(bytearray('AT+CMGDA="DEL ALL"\r')) # delete all SMS
    time.sleep(1)
    reply = ser.read() # Clear buffer
    print(reply)
    print("Listening for incoming SMS...")
    while True:
        reply = ser.read()
        if reply != "":
            ser.write(bytearray('AT+CMGR=1\r'))
            time.sleep(1)
            reply = ser.read()
            print("SMS received. Content:")
            print(reply)
            time.sleep(.500)
            ser.write(bytearray('AT+CMGDA="DEL ALL"\r')) # delete all sms
            time.sleep(.500)
            recv = ser.read() # Clear buffer
            print(recv)
            time.sleep(.500)


# ser.write('AT+CMGR=1')
def delete_all_sms():
    ser.write(bytearray('AT+CMGDA="DEL ALL"\r')) # delete all sms
    time.sleep(.500)
    recv = ser.read() # Clear buffer

#Read unread
# ser.write('AT+CMGL="REC UNREAD"\r')

def check_all_sms():
    ser.write(bytearray('AT+CMGL="ALL"\r'))    # read all sms
    time.sleep(.500)
    sms = ser.read()
    print(sms)
    #print(sms.split(b'\r\n'))