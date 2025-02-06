import cv2
from ultralytics import YOLO

camera = cv2.VideoCapture(0)
model = YOLO("yolo11n.pt")

while True:
    # 读取一帧图像
    ret, frame = camera.read()

    # 如果读取成功，显示图像
    if ret:
        results = model.track(frame, stream=True, persist=True)
        results = next(results)
        """
        if results:
            boxes = results.boxes.cpu().numpy()
            max_area = 1
            index = 1
            finall_box = None
            print("boxes.xywh",boxes.xywh)
            for box in boxes.xywh:
                print("box",box)
                area = box[2]*box[3]
                print(index,"area",area)
                index += 1
                if area > max_area:
                    max_area = area
                    finall_box = box
            print("area",finall_box[2]*finall_box[3])
            frame = cv2.circle(results.plot(), (int(finall_box[0]), int(finall_box[1])), 5, (0, 0, 255), -1)
        """
        if results:
            results = results.cpu().numpy()  # 将results转换为numpy数组
            max_area = 1
            index = 1
            finall_result = None
            for result in results:
                box = result.boxes.xywh[0]
                area = box[2] * box[3]
                print(index, "area", area)
                index += 1
                if area > max_area:
                    max_area = area
                    finall_result = result
            finall_box = finall_result.boxes.xywh[0]
            print("area", finall_box[2] * finall_box[3])
            frame = cv2.circle(
                finall_result.plot(),
                (int(finall_box[0]), int(finall_box[1])),
                5,
                (0, 0, 255),
                -1,
            )
        cv2.imshow("Camera", frame)

    # 检测按键，如果是'q'，退出循环
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 释放摄像头资源
camera.release()

# 关闭所有OpenCV窗口
cv2.destroyAllWindows()
