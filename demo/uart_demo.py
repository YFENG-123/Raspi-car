import serial
import serial.tools.list_ports
import time

# 获取所有串口设备实例。
# 如果没找到串口设备，则输出：“无串口设备。”
# 如果找到串口设备，则依次输出每个设备对应的串口号和描述信息。


"""
获取所有串口设备实例。
"""
ports_list = list(serial.tools.list_ports.comports())
if len(ports_list) <= 0:
    print("无串口设备。")
else:
    print("可用的串口设备如下：")
    for comport in ports_list:
        print(list(comport)[0], list(comport)[1])

"""
打开串口，将波特率配置为115200，其余参数使用默认值。
"""
ser = serial.Serial(
    "/dev/ttyAMA0", 115200
)  # 打开/dev/ttyAMA10，将波特率配置为115200，其余参数使用默认值
if ser.isOpen():  # 判断串口是否成功打开
    print("打开串口成功。")
    print(ser.name)  # 输出串口号
else:
    print("打开串口失败。")


"""
循环发送数据，并接收数据。
"""
while True:
    ser.write(b"hello")  # write 5 bytes
    buf = ser.read_all()
    print(buf)  # read up to 5 bytes
    time.sleep(1)


ser.close()
if ser.isOpen():  # 判断串口是否关闭
    print("串口未关闭。")
else:
    print("串口已关闭。")
