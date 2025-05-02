# frame 을 계속해서 가져온다.
# model에 frame을 넣는다
# 나온 결과를 가지고 그림을 그린다(Box와 Label)
from ultralytics import YOLO
import sys 
import cv2 

class_name = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", 
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", 
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", 
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", 
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", 
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", 
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", 
    "chair", "couch", "potted plant", "bed", "dining table", "toilet", "TV", "laptop", 
    "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", 
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", 
    "toothbrush"
]

vcap = cv2.VideoCapture(0)

model = YOLO("yolo11n.pt")

# 카메라 작동
while True:
    # ret: 카메라 작동 여부, frame: 이미지
    ret, frame = vcap.read()
    # print(type(frame))

    # 좌우 반전
    frame = cv2.flip(frame, 1)

    # 모델에 input하여 예측값 얻기
    results = model(frame, stream=True)
    for result in results:
        # print(len(result.boxes))  # Detection이 된 개수
        boxes = result.boxes
        for box in boxes:
            # print(box.cls)
            # print(class_name[int(box.cls)])
            # print(box.xyxy)

            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # print(x1, y1, x2, y2)

            # 사각형 1. 이미지 - 왼.위 - 오.아래 - 색상 - 두께 - (옵션)라인타입
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # 이미지 - 삽입할 텍스트 - 위치 - 폰트 - 크기 - 색상 - 두께
            cv2.putText(frame, class_name[int(box.cls)], (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
        

    # 카메라 띄우기
    cv2.imshow("Webcam", frame)

    key = cv2.waitKey(1)
    # ESC를 누르면 break 되도록 설정(ASCII코드, ord('q'))
    if key == 27:
        break 

vcap.release()              # 카메라 장치 해제
cv2.destroyAllWindows()     # 모든 OpenCV 창 닫기
