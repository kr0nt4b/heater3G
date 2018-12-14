# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import gc
import network
import webrepl

SSID = 'secret squirrel'
PASSWORD = 's0m3sp3c1al'

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
if ap_if.active():
	ap_if.active(False)
if not sta_if.isconnected():
	print('connecting to network...')
	sta_if.active(True)
	sta_if.connect(SSID, PASSWORD)
	while not sta_if.isconnected():
		pass
print('Network configuration:', sta_if.ifconfig())

webrepl.start()
gc.collect()
