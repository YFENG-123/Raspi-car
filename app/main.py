# 引入 pygame 相关库
import pygame
from pygame.locals import *  # noqa: F403

# 引入其他库文件
import time
import json

# 引入 app 相关库文件
from gui import PygameGUI
from controler import Controler
from uart import Uart
import schema as schema
from camera import PygameCamera
from ultralytics import YOLO

JOYBUTTONREPEAT = pygame.event.custom_type()
UARTTYPE = pygame.event.custom_type()
UARTEVENT = pygame.event.Event(UARTTYPE)


class APP:
    def __init__(self):
        self.model = YOLO("/home/YFENG/Desktop/Raspi-car/yolov8n_100e.pt")
        self.uart = Uart()  # 创建串口对象
        self.gui = PygameGUI()  # 创建GUI对象
        self.camera = PygameCamera()  # 初始化摄像头
        self.joystick: Controler = None  # 声明手柄对象
        self.joysticks = {}  # 创建手柄字典
        # pygame.time.set_timer(UARTEVENT, 100)  # 配置定时器（暂未启用）
        self.clock = pygame.time.Clock()  # 设置FPS
        self.json_buffer = schema.Json_buffer()  # 创建json对象

    def run(self):
        while True:
            self.clock.tick(30)
            # print(self.clock.get_fps())

            self._event()  # 读取事件
            self._poll()  # 更新对象

            surface_frame = self.camera.get_image()  # 获取摄像头图像
            rgb_frame = pygame.surfarray.array3d(surface_frame)
            results = self.model.track(rgb_frame, stream=True, persist=True, conf=0.1)
            # results = self.model.predict(rgb_frame, stream=True)
            results = next(results)
            if results:
                results = results.cpu().numpy()  # 将results转换为numpy数组
                max_area = 1
                index = 1
                finall_box = None
                for result in results:
                    box = results.boxes.xywh[0]
                    area = box[2] * box[3]
                    index += 1
                    if area > max_area:
                        max_area = area
                        finall_result = result
                finall_box = finall_result.boxes.xywh[0]
                frame = finall_result.plot()
                surface_frame = pygame.surfarray.make_surface(frame)
                print("y x :", int(finall_box[0]), int(finall_box[1]))
                pygame.draw.circle(
                    surface_frame,
                    (0, 0, 255),
                    (int(finall_box[1]), int(finall_box[0])),
                    5,
                )
                self.json_buffer.virtual_controler.holder_control = list(
                    [
                        (640 / 2 - int(finall_box[1])) / (640 / 2),
                        (480 / 2 - int(finall_box[0])) / (640 / 2),
                    ]
                )
            else:
                self.json_buffer.virtual_controler.holder_control = [0, 0]
            self.gui.update(surface_frame)  # 更新GUI对象

    def _poll(self):
        self.json_buffer.mouse.relative = list(
            pygame.mouse.get_rel()
        )  # 获取鼠标位移数据
        if self.joystick is not None:
            self.json_buffer.joystick.position = list(
                self.joystick.get_joystick_data()
            )  # 获取手柄axis数据
            self.json_buffer.joystick.hat = list(
                self.joystick.get_hat_data()
            )  # 获取HAT数据
        else:
            self.json_buffer.joystick = schema.Joystick()

        uart_massage = self.json_buffer.model_dump_json()  # 将数据转换为json格式
        print(uart_massage)
        self.uart.send(uart_massage)  # 发送数据

        # 恢复鼠标滚轮
        self.json_buffer.mouse.whell = 0

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
                if self.joystick == self.joysticks[event.instance_id]:
                    self.joystick = None
                del self.joysticks[event.instance_id]  # 删除字典中手柄对象
                print("手柄【" + str(event.instance_id) + "】已断开")

            """
            手柄按键读取
            """
            if event.type == pygame.JOYBUTTONDOWN:
                self.joystick = self.joysticks[event.instance_id]  # 获取手柄控制对象
                self.json_buffer.joystick.buttons.append(str(event.button))
            elif event.type == pygame.JOYBUTTONUP:
                self.json_buffer.joystick.buttons.remove(str(event.button))

            """
            鼠标按键控制读取
            """
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.json_buffer.mouse.buttons.append(str(event.button))
            elif event.type == pygame.MOUSEBUTTONUP:
                self.json_buffer.mouse.buttons.remove(str(event.button))
            elif event.type == pygame.MOUSEWHEEL:  # 鼠标滚轮控制读取
                self.json_buffer.mouse.whell = event.y

            """
            键盘按键读取
            """
            if event.type == pygame.KEYDOWN:
                self.json_buffer.keyboard.keys.append(str(event.key))
            elif event.type == pygame.KEYUP:
                self.json_buffer.keyboard.keys.remove(str(event.key))

    def stop():
        pass


if __name__ == "__main__":
    app = APP()
    app.run()
