try:
    import usocket as socket
except:
    import socket

import network
import esp


esp.osdebug(None)

import gc


gc.collect()

ssid = 'dangky3G'
password = 'moinoixong'

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid, password)

while sta.isconnected() == False:
    pass
print('Ket noi mang Wifi thanh cong!')
print(sta.ifconfig())

#0108675083
