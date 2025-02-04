# 引入 app 相关库文件
from gui import PygameGUI
from holder import Holder
from controler import Controler

# 引入 pygame 相关库
import pygame
import pygame.camera
from pygame.locals import *  # noqa: F403

# 引入其他库文件
import time
from threading import Timer
from uart import Uart


class APP:
    def __init__(self):
        self.uart = Uart()
        self.gui = PygameGUI()  # 创建GUI对象
        self.holder = Holder()  # 创建云台对象
        self.Joysticks = {}  # 创建手柄字典
        pygame.time.set_timer(pygame.USEREVENT, 100)  # 配置定时器
        self.joystick_time = time.time()  # 手柄轮询时间
        self.uart_massage = ""

    def run(self):
        while True:
            self.gui.update()  # 更新GUI对象
            self._event()  # 读取事件
            self._poll()  # 更新对象

    def uartSetMassage(self, data):
        self.uart_massage = data

    def _event(self):
        for event in pygame.event.get():  # 事件循环
            """
            定时器事件
            """
            if event.type == pygame.USEREVENT:
                self.uart.send(self.uart_massage)
                self.uart_massage = ""

            """
            窗口关闭方式
            """
            if event.type == pygame.QUIT:  # 窗口关闭方式
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:  # 列表按键方式
                if event.mod & pygame.KMOD_LSHIFT:  # 列表取修饰键方式
                    if event.key == pygame.K_ESCAPE:  # 列表取键盘方式
                        pygame.quit()
                        break

            """
            热插拔手柄
            """
            if event.type == pygame.JOYDEVICEADDED:  # 手柄连接事件
                self.joystick = Controler(event.device_index)  # 创建手柄控制对象
                self.Joysticks[self.joystick.get_id()] = self.joystick  # 添加到字典中
                print("手柄【" + str(event.device_index) + "】已连接")
            elif event.type == pygame.JOYDEVICEREMOVED:  # 手柄断开事件
                del self.Joysticks[event.instance_id]  # 删除字典中手柄对象
                print("手柄【" + str(event.instance_id) + "】已断开")

            """
            手柄选择
            """
            if event.type == pygame.JOYAXISMOTION:
                self.joystick = self.Joysticks[event.instance_id]  # 获取手柄控制对象
                print(
                    "joystick",
                    self.joystick.get_id(),
                    ":",
                    self.joystick.get_joystick_data_str(),
                )
            elif event.type == pygame.JOYBUTTONDOWN:
                self.joystick = self.Joysticks[event.instance_id]  # 获取手柄控制对象
                print(
                    "joystick",
                    self.joystick.get_id(),
                    ":",
                    self.joystick.get_joystick_data_str(),
                )

            """
            鼠标控制读取
            """
            if event.type == pygame.MOUSEMOTION:  # 鼠标移动
                # print(event)
                pass

            """
            键盘读取
            """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mouse_visible = not self.mouse_visible
                    mouse_grab = not self.mouse_grab
                    pygame.mouse.set_visible(mouse_visible)  # 隐藏鼠标
                    pygame.event.set_grab(mouse_grab)  # 锁定鼠标

    def _poll(self):
        # 手柄轮询
        if self.Joysticks is not None:
            print(
                "joystick",
                self.joystick.get_id(),
                ":",
                self.joystick.get_joystick_data_str(),
            )
            msg = "1;" + self.joystick.get_joystick_data_str()
            self.uartSetMassage(msg)

        # 键盘轮询
        keys = pygame.key.get_pressed()  # 轮询取按键方式
        if keys[pygame.K_w]:
            msg = "2;w"
            self.uartSetMassage(msg)
        elif keys[pygame.K_s]:
            
            msg = "2;s"
            self.uartSetMassage(msg)
        elif keys[pygame.K_a]:
            msg = "2;a"
            self.uartSetMassage(msg)
        elif keys[pygame.K_d]:
            msg = "2;d"
            self.uartSetMassage(msg)
        ##########################

    def stop():
        pass


if __name__ == "__main__":
    app = APP()
    app.run()
