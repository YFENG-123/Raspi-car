import machine
import json

class Uart:
    def __init__(self):
        Pin0 = machine.Pin(0,machine.Pin.OUT)
        Pin1 = machine.Pin(1,machine.Pin.IN)
        uart = machine.UART(0, baudrate=115200,tx=Pin0,rx=Pin1)