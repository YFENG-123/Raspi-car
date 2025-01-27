import network

ap = network.WLAN(network.AP_IF)
ap.config(essid='pico',password='12345678')
ap.active(True)   