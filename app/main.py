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

JOYBUTTONREPEAT = pygame.event.custom_type()
UARTTYPE = pygame.event.custom_type()
UARTEVENT = pygame.event.Event(UARTTYPE)
XBOX = [
    "BUTTON_A_0",
    "BUTTON_B_1",
    "UNKNOWN_2",
    "BUTTON_X_3",
    "BUTTON_Y_4",
    "UNKNOWN_5",
    "BUTTON_LB_6",
    "BUTTON_RB_7",
    "UNKNOWN_8",
    "UNKNOWN_9",
    "BUTTON_MAP_10",
    "BUTTON_MANUAL_11",
    "BUTTON_L_12",
    "BUTTON_R_13",
    "UNKNOWN_14",
    "BUTTON_SHARE_15",
]


class APP:
    def __init__(self):
        self.uart = Uart()  # 创建串口对象
        self.gui = PygameGUI()  # 创建GUI对象
        self.holder = Holder()  # 创建云台对象
        self.joystick: Controler = None  # 声明手柄对象
        self.joysticks = {}  # 创建手柄字典
        pygame.time.set_timer(UARTEVENT, 100)  # 配置定时器
        self.joystick_position_buffer = [0, 0, 0, 0, -1, -1]  # 创建手柄位置缓冲区
        self.pressed_button_buffer = []  # 创建按下按钮缓冲区

    def run(self):
        while True:
            self.gui.update()  # 更新GUI对象
            self._event()  # 读取事件
            self._poll()  # 更新对象

    def _event(self):
        for event in pygame.event.get():  # 事件循环
            """
            定时器事件
            """
            if event.type == UARTTYPE:
                uart_massage = ";".join(
                    [f"{self.joystick_position_buffer[i]:+.2f}" for i in range(6)]
                    + self.pressed_button_buffer
                )
                print(uart_massage)
                self.uart.send(uart_massage)

            """
            系统事件
            """
            if event.type == pygame.QUIT:  # 窗口关闭方式
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:  # 列表按键方式
                # 退出程序
                if event.mod & pygame.KMOD_LSHIFT:  # 列表取修饰键方式
                    if event.key == pygame.K_ESCAPE:  # 列表取键盘方式
                        pygame.quit()
                        break
                # 显示鼠标
                if event.key == pygame.K_ESCAPE:
                    mouse_visible = not self.mouse_visible
                    mouse_grab = not self.mouse_grab
                    pygame.mouse.set_visible(mouse_visible)  # 隐藏鼠标
                    pygame.event.set_grab(mouse_grab)  # 锁定鼠标

            """
            热插拔手柄
            """
            if event.type == pygame.JOYDEVICEADDED:  # 手柄连接事件
                self.joystick = Controler(event.device_index)  # 创建手柄控制对象
                self.joysticks[self.joystick.get_id()] = self.joystick  # 添加到字典中
                print("手柄【" + str(event.device_index) + "】已连接")
            elif event.type == pygame.JOYDEVICEREMOVED:  # 手柄断开事件
                del self.joysticks[event.instance_id]  # 删除字典中手柄对象
                print("手柄【" + str(event.instance_id) + "】已断开")

            """
            手柄事件
            """
            if event.type == pygame.JOYAXISMOTION:
                self.joystick = self.joysticks[event.instance_id]  # 获取手柄控制对象
                self.joystick_position_buffer = self.joystick.get_joystick_data()  # 获取手柄数据
            elif event.type == pygame.JOYBUTTONDOWN:
                self.joystick = self.joysticks[event.instance_id]  # 获取手柄控制对象
                self.pressed_button_buffer.append(XBOX[event.button])
            elif event.type == pygame.JOYBUTTONUP:
                self.pressed_button_buffer.remove(XBOX[event.button])

            """
            print(event)
            print(self.joystick_position_buffer)
            print(self.pressed_button_buffer)
            """

            """
            鼠标控制读取
            """
            if event.type == pygame.MOUSEMOTION:  # 鼠标移动
                pass
            """
            键盘读取
            """
            if event.type == pygame.KEYDOWN:
                self.pressed_button_buffer.append(event.key)

    def _poll(self):
        pass

    def stop():
        pass


if __name__ == "__main__":
    app = APP()
    app.run()
