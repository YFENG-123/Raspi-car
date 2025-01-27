'''
引入库文件
'''
# 引入 pygame 相关库
import pygame
import pygame.camera
from pygame.locals import *  # noqa: F403

# 引入GPIO相关库
from gpiozero import PWMOutputDevice
from time import sleep
from signal import pause

'''
初始化
'''
# 初始化pygame
pygame.init()
pygame.camera.init()
cameras = pygame.camera.list_cameras()
print(cameras)
camera = pygame.camera.Camera(cameras[0])
camera.start()
display = pygame.display.set_mode((1280, 720))  # 设置窗口

mouse_visible = False
mouse_grab = True
pygame.mouse.set_visible(mouse_visible)  # 隐藏鼠标
pygame.event.set_grab(mouse_grab)  # 锁定鼠标


# 定义GPIO
frequency = 50
horizon_location = 7.5 
vertical_location = 7.5 
P14 = PWMOutputDevice(14,initial_value = horizon_location  /100,frequency=frequency)
P15 = PWMOutputDevice(15,initial_value = vertical_location / 100,frequency=frequency)


'''
设置
'''

'''
进入主程序
'''
while True:
    frame = camera.get_image()
    display.blit(frame, (0, 0))
    pygame.display.flip()
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
                    break
            if event.key == pygame.K_ESCAPE:
                mouse_visible = not mouse_visible
                mouse_grab = not mouse_grab
                pygame.mouse.set_visible(mouse_visible)  # 隐藏鼠标
                pygame.event.set_grab(mouse_grab)  # 锁定鼠标
            if event.key == pygame.K_w:
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
                print("horizon_location:" + str(horizon_location))
        elif event.type == pygame.USEREVENT:
            P14.value = horizon_location /100
            P15.value = vertical_location /100
            print("horizon_location:" + str(horizon_location) + "vertical_location:" + str(vertical_location))

    clock.tick(60)  # 60 FPS
    '''# 键盘控制移动方式
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
        print("horizon_location:" + str(horizon_location))'''

