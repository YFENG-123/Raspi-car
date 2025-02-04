import machine
import time


class Holder:
    def __init__(self):
        self.pin2 = machine.Pin(2)  # 初始化引脚
        self.pin3 = machine.Pin(3)  # 初始化引脚
        self.pwm2 = machine.PWM(
            self.pin2, freq=50, duty_u16=int(65535 * 7.5 / 100)
        )  # 初始化PWM
        self.pwm3 = machine.PWM(
            self.pin3, freq=50, duty_u16=int(65535 * 7.5 / 100)
        )  # 初始化PWM
        self.horizon_duty = 7.5  # 初始化水平占空比（位置）
        self.vertical_duty = 7.5  # 初始化垂直占空比（位置）
        self.left_X_move = 0  # 初始化左侧摇杆X轴移动量
        self.left_Y_move = 0  # 初始化左侧摇杆Y轴移动量

    def readMove(self,controler, buffer):
        # print("buffer",buffer)
        buffer_format = buffer.split(";")
        # print("buffer_format",buffer_format)
        try:
            print("buffer_format[0]",buffer_format[0])
            print("buffer_format[1]",buffer_format[1])
            if controler == "1":
                self.left_X_move = float(buffer_format[1])  # 读取左侧摇杆X轴移动量
                self.left_Y_move = float(buffer_format[2])  # 读取左侧摇杆Y轴移动量
            elif controler == "2":
                if buffer_format[1] == "w":
                    self.left_Y_move = 1
                elif buffer_format[1] == "s":
                    self.left_Y_move = -1
                elif buffer_format[1] == "a":
                    self.left_X_move = -1
                elif buffer_format[1] == "d":
                    self.left_X_move = 1
                ###########################


        except Exception as e:
            print(e)
            return

    def updateHorizon(self):
        #print("left_X_move", self.left_X_move)
        #print("left_X_move*0.35", self.left_X_move * 0.35)

        # 添加死区
        if abs(self.left_X_move) < 0.05:
            self.left_X_move = 0
        # 更新水平占空比（位置）
        self.horizon_duty = self.horizon_duty - self.left_X_move * 0.35
        # 限制水平占空比（位置）
        if self.horizon_duty > 12.5:
            self.horizon_duty = 12.5
        elif self.horizon_duty < 2.5:
            self.horizon_duty = 2.5
        # 更新水平占空比（位置）
        self.pwm2.duty_u16(int(65535 * self.horizon_duty / 100))

    def updateVertical(self):
        # 添加死区
        if abs(self.left_Y_move) < 0.05:
            self.left_Y_move = 0
        # 更新垂直占空比（位置）
        self.vertical_duty = self.vertical_duty + self.left_Y_move * 0.35
        # 限制垂直占空比（位置）
        if self.vertical_duty > 12.5:
            self.vertical_duty = 12.5
        elif self.vertical_duty < 2.5:
            self.vertical_duty = 2.5
        # 更新垂直占空比（位置）
        self.pwm3.duty_u16(int(65535 * self.vertical_duty / 100))

    def update(self):
        self.updateHorizon()
        self.updateVertical()


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
