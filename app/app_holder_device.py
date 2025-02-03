# 引入GPIO相关库
import gpiozero
import pygame
import time
import serial
import serial.tools.list_ports
from app_controler import Controler
from app_uart import Uart

# gpiozero.Device.pin_factory = gpiozero.pins.lgpio.LGPIOFactory()


class Holder:
    def __init__(self):
        self.uart = Uart()

    def update(self, data_format):
        self.uart.send(data_format)


if __name__ == "__main__":
    pygame.init()
    controler = Controler(0)
    holder = Holder()
    last_time = time.time()
    while True:
        for event in pygame.event.get():  # 列表方式
            if event.type == pygame.QUIT:  # 窗口关闭方式
                pygame.quit()
                break
        if time.time() - last_time > 0.01:
            last_time = time.time()
            data_format = controler.get_joystick_data_str()
            print(data_format)
            holder.update(data_format)
