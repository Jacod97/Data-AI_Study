import sys 
import cv2 
import mediapipe as mp 
import csv 
import os

# Mediapipe Hand 설정
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False, 
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 데이터 설정
file_path = "./hand_data.csv"

## 파일이 존재하지 않을 때만 새로 생성
if not os.path.exists(file_path):
    with open(file_path, "w") as file:
        writer = csv.writer(file)

vcap = cv2.VideoCapture(0)

while True:
    # ret: 카메라 작동 상태, frame: 카메라 이미지
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다")
        sys.exit()

    # 좌우 반전
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape 

    # 손 감지
    results = hands.process(frame)

    # 랜드마크 추출
    if results.multi_hand_landmarks:
        one_hand = results.multi_hand_landmarks[0]

        # 좌표 모으기(21개)
        # landmark_list = [point1.x, point1.y, point1.z, ........]
        landmark_list = []
        for landmark in one_hand.landmark:
            landmark_list.extend([landmark.x, landmark.y, landmark.z])
            cv2.circle(frame, (int(width * landmark.x), int(height * landmark.y)), 2, (0,0,255), 2)

        # 데이터 저장하기(1번 키 누르면 주먹 저장, 2번 키 누르면 가위 저장, 3번 키 누르면 보 저장)
        key = cv2.waitKey(1)
        if key == ord("1"):
            landmark_list.append("rock")
            with open(file_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(landmark_list)
                cv2.putText(frame, "Save Rock Data!", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        elif key == ord("2"):
            landmark_list.append("scissors")
            with open(file_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(landmark_list)
                cv2.putText(frame, "Save scissors Data!", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        elif key == ord("3"):
            landmark_list.append("paper")
            with open(file_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(landmark_list)
                cv2.putText(frame, "Save paper Data!", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Webcam", frame)

    # ESC 누르면 종료
    key = cv2.waitKey(1)
    if key == 27:
        break

# 리소스 정리
vcap.release()
cv2.destroyAllWindows()