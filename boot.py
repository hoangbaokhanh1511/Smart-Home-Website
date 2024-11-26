try:
    import usocket as socket
except:
    import socket

import network
import esp


esp.osdebug(None)

import gc


gc.collect()

ssid = 'ImAo'
password = '12345678'

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid, password)

while sta.isconnected() == False:
    pass
print('Ket noi mang Wifi thanh cong!')
print(sta.ifconfig())

#0108675083
