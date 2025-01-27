# Filename: main.py
# Raspberry Pi Pico W
# 导入Pico W MicroPython模块
import rp2 # 导入rp2模块，该模块包含专门用于RP2040的函数和类
import network  # 导入network模块，用于连接WiFi
import ubinascii # 导入ubinascii模块，用于将MAC地址转换为十六进制字符串
import machine # 导入machine模块，用于GPIO控制
import urequests as requests # 导入urequests模块，用于HTTP请求
import time # 导入time模块，用于延时
import socket # # 导入socket模块，用于建立套接字

# 设置国家/地区代码以避免发生可能的错误
rp2.country('CN') # 这里设置Pico W的国家/地区代码为中国
wlan = network.WLAN(network.STA_IF) # 创建WLAN连接对象
wlan.active(True) # 激活WLAN接口

# 查看Pico W开发板无线WiFi的MAC地址
# 获取MAC地址，并将其转换为十六进制字符串
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('Pico W MAC=' + mac)   # 显示Pico W开发板十六进制MAC地址

ssid = "Redmi Note 11T Pro"
password = "77528888"

wlan.connect(ssid, password)  # 连接到WiFi网络

timeout = 10   # 设置最长等待连接时间为10秒
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3: # 如果WiFi连接成功或者失败
        break # 跳出循环
    timeout -= 1
    print('Wifi connecting...')
    time.sleep(1) # 延时1秒

# 定义Pico W板载LED闪亮函数
def onboard_led_blink(blink_numbers):
    onboard_led = machine.Pin('LED', machine.Pin.OUT) # 创建GPIO控制对象
    for i in range(blink_numbers):
        onboard_led.value(1)  # 点亮LED
        # onboard_led.on()  # 另一种点亮LED的方法
        time.sleep(0.5)  
        onboard_led.value(0) # 熄灭LED
        # onboard_led.off() # 另一种熄灭LED的方法
        time.sleep(0.5)

wlan_status = wlan.status() # 获取当前WiFi连接状态
onboard_led_blink(wlan_status) # 根据WiFi连接状态控制LED

# 处理连接错误
if wlan_status != 3: # 如果WiFi连接失败
    pass
    #raise RuntimeError('Wifi connect failed.') # 抛出异常
else:
    print('Wifi connect success.')
    status = wlan.ifconfig() # 获取WiFi接口配置信息
    print('IP:' + status[0]) # 输出IP地址

# 定义加载HTML页面函数  
def get_html(html_name):
    with open(html_name, 'r') as file: # 打开HTML文件
        html = file.read() # 读取HTML内容
    return html

# 打开HTTP Web服务器套接字socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1] # 获取IP地址和端口号
s = socket.socket() # 创建socket对象
s.bind(addr) # 绑定socket到IP地址和端口号
# 开始监听端口号，最多只允许1个客户端连接
s.listen(10)

print(wlan.ifconfig())
print('lestening on', addr)

onboard_led = machine.Pin('LED', machine.Pin.OUT)

# 进入循环，监听连接
while True:
    try:
        # 接受客户端连接，获取连接和地址
        cl, addr = s.accept()
        print('cilent connected from', addr)
        # 接收客户端请求消息
        r = cl.recv(1024)
        r = str(r)
        
        # 在请求消息中查找是否有开/关LED的命令
        onboard_led_on = r.find('?onboard_led=1')
        onboard_led_off = r.find('?onboard_led=0')
        print('LED=', onboard_led_on)
        print('LED=', onboard_led_off)
        # 若找到'?onboard_led=1'，则开LED
        if onboard_led_on > -1:
            print('open LED')
            onboard_led.value(1)
        # 若找到'?onboard_led=0'，则关LED
        if onboard_led_off > -1:
            print('close LED')
            onboard_led.value(0)
        
        # 获取HTML文件内容
        response = get_html('index.html')
        # 发送HTTP响应头
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        # 发送HTML文件内容
        cl.send(response)
        # 关闭客户端套接字
        cl.close()
    # 若发生OSError错误，则关闭客户端套接字并输出相关信息
    except OSError as e:
        cl.close()
        print(e)
        print('connection closed')
