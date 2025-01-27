
import rp2 # 导入rp2模块，该模块包含专门用于RP2040的函数和类
import network  # 导入network模块，用于连接WiFi
import socket # # 导入socket模块，用于建立套接字
import time # 导入time模块，用于延时
import machine # 导入machine模块，用于GPIO控制

# 设置国家/地区代码以避免发生可能的错误
rp2.country('CN') # 这里设置Pico W的国家/地区代码为中国
wlan = network.WLAN(network.STA_IF) # 创建WLAN连接对象
wlan.active(False)
wlan.active(True) # 激活WLAN接口
wlan.disconnect()

# 保存要连接的WiFi名称和密码
ssid = "Redmi Note 11T Pro"
password = "77528888"
wlan.connect(ssid, password)  

while 1:
    if not wlan.isconnected():
        # 连接/重连WiFi
        wlan.connect(ssid, password)
        count = 0

        # 读取HTML文件
        html = ""
        with open("index.html", "r") as file:
            html = file.read()

        # 创建套接字并绑定到端口80
        Socket = socket.socket()
        Socket.bind(('0.0.0.0', 80))
        Socket.listen(5)

        # 创建LED对象
        onboard_led = machine.Pin('LED', machine.Pin.OUT)

        # 循环，直到连接成功
        while not wlan.isconnected():
            count += 1
            print("WIFI status:", wlan.status())
            print("WIFI connecting..." + str(count))
            print("Aim to connect to: ", ssid, "with password: ", password, "\n")
            time.sleep(1)
        print("WIFI connected!")
        print(wlan.ifconfig())

        
    else:
        print(wlan.status("rssi"))
        time.sleep(1)
        """try:
            # 接收客户端的连接请求
            connection,address = Socket.accept()
            print("connection:"+str(connection))
            print("address:" + str(address))

            # 接收客户端请求数据
            received_data = connection.recv(1024)
            r = received_data.decode()
            print("received_data:" + r)

            # 数据中查找信息
            onboard_led_on = r.find('?onboard_led=1')
            onboard_led_off = r.find('?onboard_led=0')

            # 若找到'?onboard_led=1'，则开LED
            if onboard_led_on > -1:
                print('open LED')
                onboard_led.value(1)
            # 若找到'?onboard_led=0'，则关LED
            if onboard_led_off > -1:
                print('close LED')
                onboard_led.value(0)

            connection.send(html)
            connection.close()
        except Exception as e:
            print(e)
            time.sleep(1)"""


        