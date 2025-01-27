import network
import rp2

rp2.country('CN')

ssid = "Redmi Note 11T Pro"
password = "77528888"

wlan = network.WLAN(network.STA_IF) 
wlan.active(True) 
access_points = wlan.scan()

wlan.connect(ssid, password)
if wlan.isconnected():
    print("Wifi connect successful.")
else:
    print("Wifi connect failed.")