import cv2


video = cv2.VideoCapture(0)  # 打开摄像头


fps = video.get(cv2.CAP_PROP_FPS)  # 获取FPS数值
print(f"FPS: {fps}")


size = (
    int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
)  # 获取图片长宽
print(f"Size: {size}")

while True:
    ret, frame = video.read()  # 读取一帧
    cv2.imshow("Video Stream", frame)  # 显示一帧

    if cv2.waitKey(1) & 0xFF == 27:  # 按ESC键退出
        break

video.release()  # 释放摄像头
cv2.destroyAllWindows()  # 销毁所有窗口
