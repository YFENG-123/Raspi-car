import serial
import serial.tools.list_ports
import time


class Uart:
    def __init__(self):
        ports_list = list(serial.tools.list_ports.comports())
        if len(ports_list) <= 0:
            print("无串口设备")
        else:
            print("可用的串口设备如下：")
            for comport in ports_list:
                print(list(comport)[0], list(comport)[1])

        self.uart = serial.Serial(
            "/dev/ttyAMA0",
            3000000,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS,
        )  # 打开/dev/ttyAMA0，将波特率配置为115200，其余参数使用默认值
        if self.uart.isOpen():  # 判断串口是否成功打开
            print("打开串口成功")
            print(self.uart.name)  # 输出串口号
        else:
            print("打开串口失败")

    def send(self, data):
        self.uart.write(data.encode())


if __name__ == "__main__":
    uart = Uart()
    print(uart.uart)
    x1 = 1
    x2 = 1
    x3 = 1
    y1 = 1
    y2 = 1
    y3 = 1
    print(f"1{x1:2}1")
    #uart.send("{x1:1} \r\n")
    time.sleep(0.1)
    uart.send(" 1.00; 1.00; 1.00; 1.00; 1.00; 1.00")
    time.sleep(0.1)
    uart.send(" 1.00; 1.00; 1.00; 1.00; 1.00; 1.00")
    time.sleep(0.1)
    uart.send(" 1.00; 1.00; 1.00; 1.00; 1.00; 1.00")

