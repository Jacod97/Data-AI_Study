import sys 
import cv2 
import mediapipe as mp 
import json
import socket   # 내장 모듈

# UDP 소켓 설정
SERVER_IP = "127.0.0.1"  # 서버 주소 (로컬 테스트)
SERVER_PORT = 5005  # 서버 포트
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 소켓 설정

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

# 비디오 캡처 설정
vcap = cv2.VideoCapture(0)

# 카메라 작동
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
            landmark_list.append({"x":landmark.x, "y":landmark.y, "z":landmark.z})
            cv2.circle(frame, (int(width * landmark.x), int(height * landmark.y)), 5, (0,0,255), 2)

        # 데이터 보내기
        data = json.dumps(landmark_list) + "END"
        sock.sendto(data.encode("utf-8"), (SERVER_IP, SERVER_PORT))

    cv2.imshow("Webcam", frame)

    # ESC 누르면 종료
    key = cv2.waitKey(1)
    if key == 27:
        break

# 리소스 정리
vcap.release()
cv2.destroyAllWindows()
sock.close()