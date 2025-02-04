# 引入 app 相关库文件
from gui import PygameGUI
from holder import Holder
from controler import Controler
from uart import Uart

# 引入 pygame 相关库
import pygame
import pygame.camera
from pygame.locals import *  # noqa: F403

# 引入其他库文件
import time


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
        # pygame.time.set_timer(UARTEVENT, 100)  # 配置定时器（暂未启用）
        self.clock = pygame.time.Clock()  # 设置FPS
        self.mouse_rel_buffer = [0, 0]  # 鼠标相对位置
        self.joystick_position_buffer = [0, 0, 0, 0, -1, -1]  # 创建手柄位置缓冲区
        self.pressed_button_buffer = []  # 创建按下按钮缓冲区

    def run(self):
        while True:
            self.clock.tick(60)
            # print(self.clock.get_fps())
            self.gui.update()  # 更新GUI对象
            self._event()  # 读取事件
            self._poll()  # 更新对象

    def _event(self):
        for event in pygame.event.get():  # 事件循环
            """
            定时器事件(暂未启用)
            if event.type == UARTTYPE:
                uart_massage = ";".join(
                    [f"{rel:+.2f}" for rel in self.mouse_rel_buffer]
                    + [f"{position:+.2f}" for position in self.joystick_position_buffer]
                    + self.pressed_button_buffer
                )
                print(uart_massage)
                self.uart.send(uart_massage)
            """

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
            手柄按键读取
            """
            if event.type == pygame.JOYBUTTONDOWN:
                self.joystick = self.joysticks[event.instance_id]  # 获取手柄控制对象
                self.pressed_button_buffer.append(XBOX[event.button])
            elif event.type == pygame.JOYBUTTONUP:
                self.pressed_button_buffer.remove(XBOX[event.button])

            """
            鼠标按键控制读取
            """
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.pressed_button_buffer.append("MOUSE_LEFT")
                elif event.button == pygame.BUTTON_MIDDLE:
                    self.pressed_button_buffer.append("MOUSE_MIDDLE")
                elif event.button == pygame.BUTTON_RIGHT:
                    self.pressed_button_buffer.append("MOUSE_RIGHT")
                elif event.button == pygame.BUTTON_X1:
                    self.pressed_button_buffer.append("MOUSE_X1")
                elif event.button == pygame.BUTTON_X2:
                    self.pressed_button_buffer.append("MOUSE_X2")
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.pressed_button_buffer.remove("MOUSE_LEFT")
                elif event.button == pygame.BUTTON_MIDDLE:
                    self.pressed_button_buffer.remove("MOUSE_MIDDLE")
                elif event.button == pygame.BUTTON_RIGHT:
                    self.pressed_button_buffer.remove("MOUSE_RIGHT")
                elif event.button == pygame.BUTTON_X1:
                    self.pressed_button_buffer.remove("MOUSE_X1")
                elif event.button == pygame.BUTTON_X2:
                    self.pressed_button_buffer.remove("MOUSE_X2")
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.pressed_button_buffer.append("MOUSE_WHEEL_UP")
                elif event.y < 0:
                    self.pressed_button_buffer.append("MOUSE_WHEEL_DOWN")
            """
            键盘按键读取
            """
            if event.type == pygame.KEYDOWN:
                self.pressed_button_buffer.append(str(event.key))
            if event.type == pygame.KEYUP:
                self.pressed_button_buffer.remove(str(event.key))

    def _poll(self):
        self.joystick_position_buffer = (
            self.joystick.get_joystick_data()
        )  # 获取手柄数据
        self.joystick_hat_buffer = list(self.joystick.get_hat_data())  # 获取HAT数据
        self.mouse_rel_buffer = pygame.mouse.get_rel()  # 获取鼠标数据
        uart_massage = ";".join(
            [f"{rel:+.2f}" for rel in self.mouse_rel_buffer]
            + [f"{position:+.2f}" for position in self.joystick_position_buffer]
            + [f"{hat:+.2f}" for hat in self.joystick_hat_buffer]
            + self.pressed_button_buffer
        )  # 组合数据
        print(uart_massage)
        self.uart.send(uart_massage)  # 发送数据

        # 移除鼠标滚轮
        if "MOUSE_WHEEL_UP" in self.pressed_button_buffer:
            self.pressed_button_buffer.remove("MOUSE_WHEEL_UP")
        if "MOUSE_WHEEL_DOWN" in self.pressed_button_buffer:
            self.pressed_button_buffer.remove("MOUSE_WHEEL_DOWN")

    def stop():
        pass


if __name__ == "__main__":
    app = APP()
    app.run()
