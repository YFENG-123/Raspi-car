import machine
import time

from pico2w_mouse import Mouse
from pico2w_joystick import Joystick
from pico2w_keyboard import Keyboard


class Holder:
    def __init__(self):
        self.pin2 = machine.Pin(2)  # 初始化引脚
        self.pin3 = machine.Pin(3)  # 初始化引脚
        self.pwm2 = machine.PWM(  # 初始化PWM
            self.pin2, freq=50, duty_u16=int(65535 * 7.5 / 100)
        )
        self.pwm3 = machine.PWM(  # 初始化PWM
            self.pin3, freq=50, duty_u16=int(65535 * 7.5 / 100)
        )
        self.horizon_duty = 7.5  # 初始化水平占空比（位置）
        self.vertical_duty = 7.5  # 初始化垂直占空比（位置）
        self.horizon_move = 0  # 初始化水平移动
        self.vertical_move = 0  # 初始化垂直移动

    def read_move(self, joystick: Joystick, mouse: Mouse, keyboard: Keyboard):
        left_axis = joystick.get_left_axis()
        self.horizon_move = left_axis[0]
        self.vertical_move = left_axis[1]

    def update_horizon(self):
        self.horizon_duty = (  # 更新水平占空比（位置）
            self.horizon_duty - self.horizon_move * 0.35
        )

        """限制水平占空比（位置）"""
        if self.horizon_duty > 12.5:
            self.horizon_duty = 12.5
        elif self.horizon_duty < 2.5:
            self.horizon_duty = 2.5

        self.pwm2.duty_u16(  # 更新水平占空比（位置）
            int(65535 * self.horizon_duty / 100)
        )

    def update_vertical(self):
        self.vertical_duty = (  # 更新垂直占空比（位置）
            self.vertical_duty + self.vertical_move * 0.35
        )
        """限制垂直占空比（位置）"""
        if self.vertical_duty > 12.5:
            self.vertical_duty = 12.5
        elif self.vertical_duty < 2.5:
            self.vertical_duty = 2.5

        self.pwm3.duty_u16(  # 更新垂直占空比（位置）
            int(65535 * self.vertical_duty / 100)
        )

    def update(self):
        self.update_horizon()
        self.update_vertical()


if __name__ == "__main__":
    holder = Holder()
    holder.horizon_duty = 2.5
    holder.vertical_duty = 2.5
    holder.update()
    while True:
        for i in range(int(2.5 / 0.5), int(12.5 / 0.5), int(0.5 / 0.5)):
            holder.horizon_duty = i * 0.5
            holder.vertical_duty = i * 0.5
            holder.update()
            time.sleep(0.1)
        for i in range(int(2.5 / 0.5), int(12.5 / 0.5), int(0.5 / 0.5)):
            holder.horizon_duty = 12.5 - i * 0.5
            holder.vertical_duty = 12.5 - i * 0.5
            holder.update()
            time.sleep(0.1)
