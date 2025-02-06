import pygame
import time


class Xbox:
    def __init__(self):
        self.BUTTON_A = 0
        self.BUTTON_B = 1
        self.BUTTON_X = 3
        self.BUTTON_Y = 4
        self.BUTTON_LB = 6
        self.BUTTON_RB = 7
        self.BUTTON_L = 13
        self.BUTTON_R = 14
        self.BUTTON_MAP = 10
        self.BUTTON_MANUAL = 11
        self.BUTTON_SHARE = 15


class Controler:
    def __init__(self, device_index):
        # 手柄初始化
        self.Joystick = pygame.joystick.Joystick(device_index)
        print("手柄【" + str(device_index) + "】初始化成功，信息:")
        print("     名称:" + str(self.Joystick.get_name()))
        print("     电源状态:" + str(self.Joystick.get_power_level()))
        print("     按钮x" + str(self.Joystick.get_numbuttons()))
        print("     轴x" + str(self.Joystick.get_numaxes()))
        print("     实例ID:" + str(self.Joystick.get_instance_id()))
        print("     GUID:" + str(self.Joystick.get_guid()))
        print("当前位置:")
        print(
            "       左摇杆X轴当前位置(轴ID:0):"
            + str(round(self.Joystick.get_axis(0), 2))
        )
        print(
            "       左摇杆Y轴当前位置(轴ID:1):"
            + str(round(self.Joystick.get_axis(1), 2))
        )
        print("     左扳机位置(轴ID:2):" + str(round(self.Joystick.get_axis(2), 2)))
        print(
            "       右摇杆X轴当前位置(轴ID:3):"
            + str(round(self.Joystick.get_axis(3), 2))
        )
        print(
            "       右摇杆Y轴当前位置(轴ID:4):"
            + str(round(self.Joystick.get_axis(4), 2))
        )
        print("     右扳机位置(轴ID:5):" + str(round(self.Joystick.get_axis(5), 2)))
        print("震动测试...")
        self.Joystick.rumble(0.1, 0.1, 1)
        time.sleep(1)
        self.Joystick.rumble(0.1, 10, 1)
        time.sleep(1)
        self.Joystick.rumble(10, 0.1, 1)
        time.sleep(1)
        self.Joystick.stop_rumble()
        print("测试完成")

    def get_id(self):
        return self.Joystick.get_instance_id()

    def get_joystick_data(self):
        return [round(self.Joystick.get_axis(i), 2) for i in range(6)]

    def get_hat_data(self):
        return self.Joystick.get_hat(0)


if __name__ == "__main__":
    pygame.init()
    controler = Controler(0)
    while True:
        for event in pygame.event.get():  # 列表方式
            if event.type == pygame.QUIT:  # 窗口关闭方式
                pygame.quit()
                break
        data_format = controler.get_joystick_data_str()
        print(data_format)
        time.sleep(0.1)
