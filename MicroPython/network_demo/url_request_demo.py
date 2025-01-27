import network
import rp2
import time
import urequests

rp2.country('CN')

ssid = "Redmi Note 11T Pro"
password = "77528888"

wlan = network.WLAN(network.STA_IF) 
wlan.active(True) 
wlan.connect(ssid, password)

time.sleep(1)

if wlan.isconnected():
    print("Wifi connect successful.")
else:
    print("Wifi connect failed.")

r = urequests.get('http://www.baidu.com/')
print(r.content)
r.close()
