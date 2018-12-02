

import gprs
import machine

gprs.init_gprs_and_http()
heater_on = gprs.check_heater_on()

print("heater: " + str(heater_on))

if heater_on:
    pin = machine.Pin(13, machine.Pin.OUT)
    pin.value(1)
