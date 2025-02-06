import pygame
from pygame.locals import *  # noqa: F403

# 初始化pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))  # 设置窗口
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)  # 隐藏鼠标
pygame.event.set_grab(True)  # 锁定鼠标

# 玩家初始位置
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# 手柄初始化
print("手柄数量：" + str(pygame.joystick.get_count()))
Joystick = pygame.joystick.Joystick(0)
Joystick.init()
print("手柄名称：")
print(Joystick.get_name())
print("手柄按钮数量：" + str(Joystick.get_numbuttons()))
print("手柄轴数量：" + str(Joystick.get_numaxes()))
print("手柄电源状态：" + str(Joystick.get_power_level()))
axes = Joystick.get_numaxes()
print("手柄轴数量：" + str(axes))


# 主函数
def main():
    dt = 0
    speedX = 0
    speedY = 0
    # 主循环
    while True:
        # 事件循环
        for event in pygame.event.get():  # 列表方式
            if event.type == QUIT:  # 窗口关闭方式
                pygame.quit()
                return
            elif event.type == MOUSEMOTION:  # 鼠标移动方式
                print(event)
            elif event.type == KEYDOWN:  # 列表按键方式
                if event.mod & KMOD_LSHIFT:  # 列表取修饰键方式
                    if event.key == K_ESCAPE:  # 列表取键盘方式
                        pygame.quit()
                        return

        # 键盘控制移动方式
        keys = pygame.key.get_pressed()  # 轮询取按键方式
        if keys[pygame.K_w]:
            player_pos.y -= dt
        if keys[pygame.K_s]:
            player_pos.y += dt
        if keys[pygame.K_a]:
            player_pos.x -= dt
        if keys[pygame.K_d]:
            player_pos.x += dt

        # 手柄控制移动方式
        print(
            "手柄左摇杆X轴当前位置："
            + str(round(Joystick.get_axis(0), 2))
            + "手柄左摇杆Y轴当前位置："
            + str(round(Joystick.get_axis(1), 2))
            + "手柄右摇杆X轴当前位置："
            + str(round(Joystick.get_axis(2), 2))
            + "手柄右摇杆Y轴当前位置："
            + str(round(Joystick.get_axis(3), 2))
        )
        speedX = Joystick.get_axis(0)
        speedY = Joystick.get_axis(1)
        player_pos.x += speedX * 10
        player_pos.y += speedY * 10

        # 刷新背景
        screen.fill("black")

        # 将帧数显示在屏幕左上角
        font = pygame.font.Font(None, 36)
        text = font.render(str(clock.get_fps()), True, "white")
        screen.blit(text, (10, 10))

        # 绘制玩家位置
        pygame.draw.circle(screen, "white", player_pos, 40)
        pygame.display.flip()
        dt = clock.tick(60)  # 60 FPS


# Execute game:
main()
