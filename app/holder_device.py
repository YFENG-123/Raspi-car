# 引入GPIO相关库
from gpiozero import PWMOutputDevice
import time
from time import sleep
from signal import pause

class Holder():
    def __init__(self):
        self.frequency = 50
        self.horizon_location = 7.5 
        self.vertical_location = 7.5 
        self.P14 = PWMOutputDevice(14,initial_value = self.horizon_location  /100,frequency=self.frequency)
        self.P15 = PWMOutputDevice(15,initial_value = self.vertical_location / 100,frequency=self.frequency)
    
    def turn_left(self):
        self.horizon_location += 0.1
        self.update()
    def turn_right(self):
        self.horizon_location -= 0.1
        self.update()

    def turn_up(self):
        self.vertical_location += 0.1
        self.update()

    def turn_down(self):
        self.vertical_location -= 0.1
        self.update()

    def update(self):
        self.P14.value = self.horizon_location / 100
        self.P15.value = self.vertical_location / 100
        print("horizon_location:" + str(self.horizon_location) + "vertical_location:" + str(self.vertical_location))

if __name__ == '__main__':
    holder = Holder()
    while True:
        holder.turn_up()
        time.sleep(0.1)
        holder.turn_down()
        time.sleep(0.1)
        holder.turn_left()
        time.sleep(0.1)
        holder.turn_right()
        time.sleep(0.1)