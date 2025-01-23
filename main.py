# 引入 pygame 相关库
import pygame
from pygame.locals import *  # noqa: F403

# 引入GPIO相关库
from gpiozero import PWMOutputDevice
from time import sleep
from signal import pause

# 引入OpenCV相关库
import cv2


# 初始化pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))  # 设置窗口
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)  # 隐藏鼠标
pygame.event.set_grab(True)  # 锁定鼠标

# 定义GPIO
frequency = 50
horizon_location = 7.5 
vertical_location = 7.5 
P14 = PWMOutputDevice(14,initial_value = vertical_location  /100,frequency=frequency)
P15 = PWMOutputDevice(15,initial_value = horizon_location / 100,frequency=frequency)

# 定义摄像头
video = cv2.VideoCapture(0) # 打开摄像头

# 定时器
pygame.time.set_timer( pygame.USEREVENT, 500)

while True:

    # 事件循环
    for event in pygame.event.get():  # 列表方式
        if event.type == pygame.QUIT:  # 窗口关闭方式
            pygame.quit()
            break
        elif event.type == pygame.MOUSEMOTION:  # 鼠标移动方式
            #print(event)
            pass
        elif event.type == pygame.KEYDOWN:  # 列表按键方式
            if event.mod & pygame.KMOD_LSHIFT:  # 列表取修饰键方式
                if event.key == pygame.K_ESCAPE:  # 列表取键盘方式
                    pygame.quit()

            '''if event.key == pygame.K_w:
                vertical_location -= 0.1
                print("vertical_location:" + str(vertical_location))
            if event.key == pygame.K_s:
                vertical_location += 0.1
                print("vertical_location:" + str(vertical_location))
            if event.key == pygame.K_a:
                horizon_location += 0.1
                print("horizon_location:" + str(horizon_location))
            if event.key == pygame.K_d:
                horizon_location -= 0.1
                print("horizon_location:" + str(horizon_location))'''

        elif event.type == pygame.USEREVENT:
            P14.value = vertical_location /100
            P15.value = horizon_location /100
            #print("horizon_location:" + str(horizon_location))
            #print("vertical_location:" + str(vertical_location))

    clock.tick(60)  # 60 FPS

    # 键盘控制移动方式
    keys = pygame.key.get_pressed()  # 轮询取按键方式
    if keys[pygame.K_w]:
        vertical_location -= 0.1
        print("vertical_location:" + str(vertical_location))
    if keys[pygame.K_s]:
        vertical_location += 0.1
        print("vertical_location:" + str(vertical_location))
    if keys[pygame.K_a]:
        horizon_location += 0.1
        print("horizon_location:" + str(horizon_location))
    if keys[pygame.K_d]:
        horizon_location -= 0.1
        print("horizon_location:" + str(horizon_location))

    ret, frame = video.read() # 读取一帧
    cv2.imshow("Video Stream", frame) # 显示一帧

    if cv2.waitKey(1) & 0xFF == 27:# 按ESC键退出
        break

video.release() # 释放摄像头