from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # pretrained YOLO11n model

# Run batched inference on a list of images
results = model("dog_img.jpg")  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    print("boxes:")
    print(boxes)
    masks = result.masks  # Masks object for segmentation masks outputs
    print("masks:")
    print(masks)
    keypoints = result.keypoints  # Keypoints object for pose outputs
    print("keypoints:")
    print(keypoints)
    probs = result.probs  # Probs object for classification outputs
    print("probs:")
    print(probs)
    obb = result.obb  # Oriented boxes object for OBB outputs
    print("obb:")
    print(obb)
    result.show()  # display to screen
    result.save(filename="result.jpg")  # save to disk
