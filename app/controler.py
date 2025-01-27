import pygame
import time


class Controler:
    def __init__(self, device_index):
        # 手柄初始化
        self.Joystick = pygame.joystick.Joystick(device_index)
        self.Joystick.init()
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
        print("       左扳机位置(轴ID:2):" + str(round(self.Joystick.get_axis(2), 2)))
        print(
            "       右摇杆X轴当前位置(轴ID:3):"
            + str(round(self.Joystick.get_axis(3), 2))
        )
        print(
            "       右摇杆Y轴当前位置(轴ID:4):"
            + str(round(self.Joystick.get_axis(4), 2))
        )
        print("       右扳机位置(轴ID:5):" + str(round(self.Joystick.get_axis(5), 2)))
        print("震动测试...")
        self.Joystick.rumble(0.1, 0.1, 1)
        time.sleep(0.5)
        self.Joystick.rumble(0.1, 10, 1)
        time.sleep(0.5)
        self.Joystick.rumble(10, 0.1, 1)
        time.sleep(0.5)
        print("测试完成")

    def get_id(self):
        return (self.Joystick.get_instance_id())

    def get_left_x(self):
        return (self.Joystick.get_axis(0))

    def get_left_y(self):
        return (self.Joystick.get_axis(1))

    def get_left_z(self):
        return (self.Joystick.get_axis(2))

    def get_right_x(self):
        return (self.Joystick.get_axis(3))

    def get_right_y(self):
        return self.Joystick.get_axis(4)

    def get_right_z(self):
        return self.Joystick.get_axis(5)

    def get_joystick_data(self):
        return [self.Joystick.get_axis(i) for i in range(6)]


if __name__ == "__main__":
    pygame.init()
    controler = Controler(0)
    print(controler.get_joystick_data())
    while True:
        event = pygame.event.get()
        for e in event:
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
                break
            if e.type == pygame.JOYAXISMOTION:
                print(controler.get_joystick_data())
            if e.type == pygame.JOYBUTTONDOWN:
                print(controler.get_joystick_data())
