import network
import binascii

wlan = network.WLAN(network.STA_IF) 
wlan.active(True) 
access_points = wlan.scan()

# 按信号强弱排序
access_points.sort(key=lambda x:x[3], reverse=True)
 
for ssid, bssid, channel, RSSI, security, hidden in access_points:
    print(ssid, binascii.hexlify(bssid), channel, RSSI, security, hidden)
    print(ssid.decode())