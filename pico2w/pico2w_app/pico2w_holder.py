import machine
import time


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

    def update(self):
        """限制垂直占空比（位置）"""
        if self.vertical_duty > 11.5:  # 12.5
            self.vertical_duty = 11.5
        elif self.vertical_duty < 4.5:  # 2.5
            self.vertical_duty = 4.5
        """更新垂直占空比（位置）"""
        self.pwm2.duty_u16(  # 更新垂直占空比（位置）
            int(65535 * self.vertical_duty / 100)
        )

        """限制水平占空比（位置）"""
        if self.horizon_duty > 12.5:
            self.horizon_duty = 12.5
        elif self.horizon_duty < 2.5:
            self.horizon_duty = 2.5
        """更新水平占空比（位置）"""
        self.pwm3.duty_u16(  # 更新水平占空比（位置）
            int(65535 * self.horizon_duty / 100)
        )

    def set_position(self, x, y):
        self.horizon_duty = x
        self.vertical_duty = y
        self.update()

    def move(self, x, y):
        self.horizon_duty = self.horizon_duty + x * 1.0  # 更新水平占空比（位置）
        self.vertical_duty = self.vertical_duty + y * 1.0  # 更新垂直占空比（位置）
        print("horizon_duty, vertical_duty : ", self.horizon_duty, self.vertical_duty)
        self.update()


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
            time.sleep(0.5)
        for i in range(int(2.5 / 0.5), int(12.5 / 0.5), int(0.5 / 0.5)):
            holder.horizon_duty = 12.5 - i * 0.5
            holder.vertical_duty = 12.5 - i * 0.5
            holder.update()
            time.sleep(0.5)
