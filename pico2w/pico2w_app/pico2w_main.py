"""引入通信模块"""
from pico2w_uart import Uart
from pico2w_schema import Json_data
'''引入云台模块'''
from pico2w_holder import Holder

'''引入控制模块'''
from pico2w_joystick import Joystick
from pico2w_keyboard import Keyboard
from pico2w_mouse import Mouse
from pico2w_virtual_controler import Virtual_controler





"""引入系统模块"""
import machine
import time
import json


MOUSE = ["MOUSE_LEFT_1", "MOUSE_MIDDLE_2", "MOUSE_RIGHT_3", "MOUSE_X1_4", "MOUSE_X2_5"]

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

KEY = {
    119: "KEY_W",
    115: "KEY_S",
    97: "KEY_A",
    100: "KEY_D",
    1073741906: "KEY_UP",
    1073741905: "KEY_DOWN",
    1073741904: "KEY_LEFT",
    1073741903: "KEY_RIGHT",
    113: "KEY_Q",
    101: "KEY_E",
    32: "KEY_SPACE",
    "MOUSE_WHEEL_UP": "MOUSE_WHEEL_UP",
    "MOUSE_WHEEL_DOWN": "MOUSE_WHEEL_DOWN",
}


class APP:
    def __init__(self):
        """初始化设备"""
        self.holder = Holder()  # 初始化云台
        """初始化控制器"""
        self.mouse = Mouse()  # 初始化鼠标
        self.joystick = Joystick()  # 初始化手柄
        self.keyboard = Keyboard()  # 初始化键盘
        self.virtual_controler = Virtual_controler()
        self.json_data = Json_data()
        
        """初始化数据接口"""
        self.uart = Uart()  # 初始化UART
        self.uart.irq(self._uart_interrupted)  # 监听UART
        self.data_ready = False

    def _uart_interrupted(self, uart_info):
        massage = self.uart.readline()  # 读取串口数据
        json_buffer = json.loads(massage)  # 字节流转为json
        print(json_buffer)
        try:
            self.json_data.load_data(json_buffer)  # json 数据转对象
            self.joystick.set_data(self.json_data.joystick_data)
            self.keyboard.set_data(self.json_data.keyboard_data)
            self.mouse.set_data(self.json_data.mouse_data)
            self.virtual_controler.set_data(self.json_data.virtual_controler_data)
            self.data_ready = True
        except Exception as e:
            print(e)

    def run(self):
        while True:
            if self.data_ready:
                self.data_ready = False
                self.holder.read_move(self.joystick, self.mouse, self.keyboard,self.virtual_controler)
                self.holder.update()
            else:
                time.sleep(0.01)


if __name__ == "__main__":
    app = APP()
    app.run()
