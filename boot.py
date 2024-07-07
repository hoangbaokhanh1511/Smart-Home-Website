try:
    import usocket as socket
except:
    import socket

import network
import esp
import urequests
import utime

esp.osdebug(None)

import gc


gc.collect()

ssid = 'Dao Ngan'
password = '0108675083'

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid, password)

while sta.isconnected() == False:
    pass
print('Ket noi mang Wifi thanh cong!')
print(sta.ifconfig())

#0108675083


current_time = utime.time()
data = {
  'timestamp': current_time,
  'temperature': 30,
  'humidity': 88
}


url = "https://script.google.com/macros/s/AKfycbzb_Wlz7Qk8AXy61u_tloiwCKNLokwu1QnghTLh3RwyDsKQ_h2C0us_QILmOeUGuNC_8A/exec"
headers = {'Content-Type': 'application/json'}
response = urequests.post(url, json=data, headers=headers)