from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import PWMOutputDevice, DigitalOutputDevice

# 引入 pygame 相关库
import pygame
from pygame.locals import *  # noqa: F403

# 引入其他库文件
import time
import json
import cv2

# 引入 app 相关库文件
from window import Window
from controler import Controler
from uart import Uart
import schema as schema
from camera import OpenCVCamera
#from audio import AudioInput, AudioOutput
#from model import Model


JOYBUTTONREPEAT = pygame.event.custom_type()
UARTTYPE = pygame.event.custom_type()
UARTEVENT = pygame.event.Event(UARTTYPE)


class APP:
    def __init__(self):
        self.factory = LGPIOFactory()
        self.pin18 = DigitalOutputDevice(18, pin_factory=self.factory)
        self.pin18.on()
        self.pin4 = DigitalOutputDevice(4, pin_factory=self.factory)
        self.pin4.off()
        self.pin3 = DigitalOutputDevice(3, pin_factory=self.factory)
        self.pin3.off()
        self.pin3_tag = False
        """创建相关对象"""
        self.uart = Uart()  # 创建串口对象
        self.window = Window()  # 创建GUI对象
        self.camera = OpenCVCamera()  # 创建摄像头对象
        self.clock = pygame.time.Clock()  # 创建时钟对象
        self.json_buffer = schema.Json_buffer()  # 创建json对象

        """创建带线程对象"""
        #self.model = Model()  # 创建模型对象
        #self.model.set_frame(self.camera.get_frame())
        #self.model.start_predict_thread()
        #self.audio_input = AudioInput()  # 创建音频输入对象
        #self.audio_output = AudioOutput()  # 创建音频输出对象
        #self.audio_input.aim = 1
        

        """声明空对象"""
        self.joystick: Controler = None  # 声明手柄对象
        self.joysticks = {}  # 创建手柄字典

        """设置 pygame 相关参数"""
        self.mouse_visible = False  # 鼠标是否可见
        self.mouse_grab = False  # 鼠标是否锁定
        pygame.mouse.set_visible(self.mouse_visible)  # 隐藏鼠标
        pygame.event.set_grab(self.mouse_grab)  # 锁定鼠标
        # pygame.time.set_timer(UARTEVENT, 100)  # 配置定时器

        """设置运行标志 """
        self.is_running = True

        self.last_result = None

    def run(self):
        while self.is_running:
            self.clock.tick(60)  # 刷新率
            self._event()  # 事件
            self._poll()  # 轮询
            self._update()  # 更新
            self._uart_send()  # 发送数据

    def _update(self):
        frame = self.camera.get_frame()  # 获取摄像头图像
        '''self.model.set_frame(frame)  # 设置模型输入
        result = self.model.get_result()  # 获取模型输出
        frame = result.plot(img=frame)  # 绘制框
        self.aim = self.audio_input
        if 39 in result.boxes.cls.tolist() and result != self.last_result:
            if len(result.boxes.xywh) > 0:
                """获取最大面积的框 """
                max_area = 1
                index = 1
                finall_box = None
                for boxes in result.boxes:
                    if boxes.cls.tolist()[0] != 39:
                        continue
                    box = boxes.xywh.tolist()[0]
                    area = box[2] * box[3]
                    # print("area", area)
                    index += 1
                    if area > max_area:
                        max_area = area
                        finall_box = box

                """画圆"""
                frame = cv2.circle(
                    frame,
                    (int(finall_box[0]), int(finall_box[1])),  # 圆心坐标
                    5,  # 半径
                    (255, 0, 0),  # 颜色
                    -1,  # 线宽
                )

                """移动到中心"""
                if (
                    self.json_buffer.joystick.position == [0, 0, 0, 0, -1, -1]
                    and self.audio_input.aim == 1
                ):
                    print(finall_box[0], finall_box[1])
                    self.json_buffer.joystick.position = list(
                        [
                            (int(finall_box[0] - 640 / 2)) / (640),
                            (480 / 2 - int(finall_box[1])) / (480),
                            0,
                            0,
                            -1,
                            -1,
                        ]
                    )
                    print(self.json_buffer.joystick.position)
                else:
                    pass
                    # self.json_buffer.joystick.position = [0, 0, 0, 0, -1, -1]
        self.last_result = result
        if self.audio_input.fire == 1:
            self.pin4.on()
            time.sleep(0.5)
            self.pin4.off()
            self.audio_input.fire = 0'''
        self.window.update(frame)  # 更新GUI对象

    def _poll(self):
        self.json_buffer.mouse.relative = list(
            pygame.mouse.get_rel()
        )  # 获取鼠标位移数据
        if self.joystick is not None:
            self.json_buffer.joystick.position = list(
                self.joystick.get_joystick_data()
            )  # 获取手柄axis数据
            if (
                abs(self.json_buffer.joystick.position[0]) < 0.05
                and abs(self.json_buffer.joystick.position[1]) < 0.05
                and abs(self.json_buffer.joystick.position[2]) < 0.05
                and abs(self.json_buffer.joystick.position[3]) < 0.05
                and self.json_buffer.joystick.position[4] < -0.95
                and self.json_buffer.joystick.position[5] < -0.95
            ):
                self.json_buffer.joystick.position = [0, 0, 0, 0, -1, -1]
            self.json_buffer.joystick.hat = list(
                self.joystick.get_hat_data()
            )  # 获取HAT数据
        else:
            self.json_buffer.joystick = schema.Joystick()

    def _uart_send(self):
        uart_massage = self.json_buffer.model_dump_json()  # 将数据转换为json格式
        self.uart.send(uart_massage)  # 发送数据
        print(uart_massage)

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

            """系统事件"""
            if event.type == pygame.QUIT:  # 窗口关闭方式
                self.is_running = False

            if event.type == pygame.KEYDOWN:  # 列表按键方式
                # 退出程序
                if event.mod & pygame.KMOD_LSHIFT:  # 列表取修饰键方式
                    if event.key == pygame.K_ESCAPE:  # 列表取键盘方式
                        self.model.stop_predict_thread()  # 停止模型线程
                        self.is_running = False

                # 显示鼠标
                if event.key == pygame.K_ESCAPE:
                    self.mouse_visible = not self.mouse_visible
                    self.mouse_grab = not self.mouse_grab
                    pygame.mouse.set_visible(self.mouse_visible)  # 隐藏鼠标
                    pygame.event.set_grab(self.mouse_grab)  # 锁定鼠标

            """热插拔手柄"""
            if event.type == pygame.JOYDEVICEADDED:  # 手柄连接事件
                self.joystick = Controler(event.device_index)  # 创建手柄控制对象
                self.joysticks[self.joystick.get_id()] = self.joystick  # 添加到字典中
                print("手柄【" + str(event.device_index) + "】已连接")
            elif event.type == pygame.JOYDEVICEREMOVED:  # 手柄断开事件
                if self.joystick == self.joysticks[event.instance_id]:
                    self.joystick = None
                del self.joysticks[event.instance_id]  # 删除字典中手柄对象
                print("手柄【" + str(event.instance_id) + "】已断开")

            """手柄按键读取"""
            if event.type == pygame.JOYBUTTONDOWN:
                self.joystick = self.joysticks[event.instance_id]  # 获取手柄控制对象
                self.json_buffer.joystick.buttons.append(str(event.button))
                if event.button == 0:  # 列表取按键方式
                    self.pin4.on()
                if event.button == 1:
                    self.audio_input.stream.start_stream()
                if event.button == 3:
                    self.pin3_tag = not self.pin3_tag
                    if self.pin3_tag is True:
                        self.pin3.on()
                    elif self.pin3_tag is False:
                        self.pin3.off()
                print(self.pin3)

            elif event.type == pygame.JOYBUTTONUP:
                self.json_buffer.joystick.buttons.remove(str(event.button))
                if event.button == 0:  # 列表取按键方式
                    self.pin4.off()
                if event.button == 1:
                    self.audio_input.stream.stop_stream()

            """鼠标按键控制读取"""
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.json_buffer.mouse.buttons.append(str(event.button))
            elif event.type == pygame.MOUSEBUTTONUP:
                self.json_buffer.mouse.buttons.remove(str(event.button))
            elif event.type == pygame.MOUSEWHEEL:  # 鼠标滚轮控制读取
                self.json_buffer.mouse.whell = event.y

            """键盘按键读取"""
            if event.type == pygame.KEYDOWN:
                self.json_buffer.keyboard.keys.append(str(event.key))
            elif event.type == pygame.KEYUP:
                self.json_buffer.keyboard.keys.remove(str(event.key))


if __name__ == "__main__":
    app = APP()
    app.run()
    print("程序结束")
