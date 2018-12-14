

import gprs
import machine
import time

one_quarter = 900000
one_minute = 60000

pin_3g = machine.Pin(15, machine.Pin.OUT, value=1)
remote_on = machine.Pin(33, machine.Pin.OUT, value=1)
remote_off = machine.Pin(27, machine.Pin.OUT, value=1)


def turn_heater_on():
    remote_on.value(0)
    time.sleep(2)
    remote_on.value(1)


def turn_heater_off():
    remote_off.value(0)
    time.sleep(2)
    remote_off.value(1)


def read_from_3g():
    pin_3g.value(1)
    time.sleep(20)
    gprs.init_gprs_and_http()
    return gprs.check_heater_on()


while True:

    heater_on = read_from_3g()
    print("heater: " + str(heater_on))

    if heater_on:
        turn_heater_on()
    else:
        turn_heater_off()

    pin_3g.value(0)
    machine.deepsleep(one_quarter)

