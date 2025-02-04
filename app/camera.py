import pygame

class PygameCamera():
    def __init__(self):
        pygame.camera.init()
        print("初始化摄像头...")
        self.cameras = pygame.camera.list_cameras() # 摄像头列表
        print("摄像头列表:",self.cameras)
        print("启动摄像头:",self.cameras[0])
        self.camera = pygame.camera.Camera(self.cameras[0]) # 获取/注册摄像头
        self.camera.start() # 启动摄像头
        print("摄像头启动成功")

    def get_image(self):
        return self.camera.get_image()