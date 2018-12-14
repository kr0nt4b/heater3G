
import machine
import time
from debug import debug
import re

ser = machine.UART(1, baudrate=115200, rx=16, tx=17, timeout=10)


def __send_and_read_reply__(cmd):
    cmd_to_write = bytearray(cmd + '\r')
    ser.write(cmd_to_write)
    debug('CMD: ' + cmd)
    time.sleep(.5)

    raw_reply = ''

    while True:
        next_reply = ser.read()
        if next_reply is None:
            break

        raw_reply += next_reply.decode("utf-8")
        time.sleep(.5)

    return raw_reply


def __send_and_wait_reply__(cmd):
    cmd_to_write = bytearray(cmd + '\r')
    ser.write(cmd_to_write)
    debug('CMD: ' + cmd)
    time.sleep(2)

    raw_reply = ''

    while ser.any():
        next_reply = ser.read()
        debug('next: %s' % next_reply)
#        if next_reply is None:
#            break
        raw_reply += next_reply.decode("utf-8")
        time.sleep(2)

    return raw_reply


def __send_and_ok__(cmd):
    reply = __send_and_read_reply__(cmd)
    debug("REPLY: " + reply.strip())
    return reply.find('OK') > 0


def __send_and_validate__(cmd, regex):
    reply = __send_and_read_reply__(cmd)
    return re.match(regex, reply)


def init_gprs_and_http():
    __set_echo_off__()
    # Set the connection type to GPRS
    __send_and_ok__('AT+SAPBR=3,1,"Contype","GPRS"')

    # Set the APN to to "internet"
    __send_and_ok__('AT+SAPBR=3,1,"APN","internet"')

    # Enable the GPRS
    __send_and_ok__('AT+SAPBR=1,1')

    # Query if the connection is setup properly, if we get back a IP address then we can proceed
    __send_and_ok__('AT+SAPBR=2,1')
    # return: +SAPBR: 1,1,"100.120.204.132"

    # We were allocated a IP address and now we can proceed by enabling the HTTP mode
    __send_and_ok__('AT+HTTPINIT')

    # ONLY IF URL is HTTPS or SSL enabled: Also Remove the http:// part in the HTTPPARA="URL",xxxx command
    __send_and_ok__('AT+HTTPSSL=1')

    # Start by setting up the HTTP bearer profile identifier
    __send_and_ok__('AT+HTTPPARA="CID",1')

    # Basic auth = izzeme:yucanTcatchm4
    __send_and_ok__('AT+HTTPPARA="USERDATA","Authorization: Basic aXp6ZW1lOnl1Y2FuVGNhdGNobTQ="')


def ___http_read__(url):
    # Set the url  to the address of the webpage you want to access
    __send_and_ok__('AT+HTTPPARA="URL","https://geo.totalize.nl/' + url + '"')

    # Start the HTTP GET session, by giving this command
    __send_and_ok__('AT+HTTPACTION=0')
    '''
    # The below output from module indicates it  has read 654 bytes of data and
    # the response of the HTTP GET request is 200, which means success
    # return +HTTPACTION:0,200,654')
    time.sleep(1)
    ser.write(bytearray('AT+HTTPREAD\r'))
    time.sleep(1)
    reply = ser.read()
    time.sleep(1)
    debug('REPLY: ' + reply.decode('UTF-8'))
    return reply.decode('UTF-8')
'''
    time.sleep(1)
    reply = __send_and_wait_reply__('AT+HTTPREAD')
    reply = __send_and_wait_reply__('AT+HTTPREAD')
    return reply


def check_heater_on():
    response = ___http_read__('heater')
    http_response = __parse_http_action__(__delegate_heater_on__, response)
    __send_and_ok__('AT+HTTPTERM')
    return http_response


def __delegate_heater_on__(message):
    return 'heater on' in message


def __parse_http_action__(delegate_read, at_response):
    at_response_tokens = at_response.split('\r\n')
    debug('tokens: %s' % len(at_response_tokens))
    result =  False
    iterable = iter(at_response_tokens)
    for item in iterable:
        debug('Item: ' + item)
        if item.startswith('+HTTPACTION:'):
            http_code = item.split(',')[1]
            debug("HTTP return code: " + http_code)
        if item.startswith('+HTTPREAD:'):
            message = next(iterable)
            debug('Message: ' + message)
            result = delegate_read(message)
            print ("result: " + str(result))
    return result


def __set_echo_off__():
    __send_and_ok__('ATE0')


def enable_network_time():
    ser.write(bytearray('AT+CLTS=1\r'))
    time.sleep(1)
    ser.write(bytearray('AT&W'))

