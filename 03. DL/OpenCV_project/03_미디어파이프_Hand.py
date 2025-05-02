# pip install mediapipe
import sys 
import cv2 
import mediapipe as mp 

# Mediapipe의 Hand Landmark를 추출.그리기 위한 설정
mp_hands = mp.solutions.hands 
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles 

hands = mp_hands.Hands(
    static_image_mode = False, 
    max_num_hands = 1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

vcap = cv2.VideoCapture(0)

while True:
    # ret : 작동 여부
    # frame : 카메라로 받은 이미지
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다")
        sys.exit()

    # 좌우 반전
    frame = cv2.flip(frame, 1)

    ########## Hands ##########
    # 손 그리기 설정
    frame.flags.writeable = True

    # 손 감지 수행
    results = hands.process(frame)

    # 그리기 
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 그려주는 기능 사용할 때
            # mp_drawing.draw_landmarks(
            #     frame,
            #     hand_landmarks,
            #     mp_hands.HAND_CONNECTIONS,
            #     mp_drawing_styles.get_default_hand_landmarks_style(),
            #     mp_drawing_styles.get_default_hand_connections_style()
            # )

            # 내가 직접 그리고 싶을 때
            height, width, _ = frame.shape

            select_list = [4, 8, 12, 16, 20]
            for idx in select_list:
                x = hand_landmarks.landmark[idx].x
                y = hand_landmarks.landmark[idx].y

                point_x = int(x * width) 
                point_y = int(y * height)
                cv2.circle(frame, (point_x, point_y), 5, (0,0,255), 2, lineType=cv2.LINE_AA)

        ##### 프린트 테스트 #####
        # print(len(results.multi_hand_landmarks))        # 손을 잘 감지하는지에 대한 출력 테스트
        one_hand = results.multi_hand_landmarks[0]
        # print("몇 개?", len(one_hand.landmark))
        # for landmark in one_hand.landmark:
        #     print(landmark)
        ### 미션
        # 1번. landmark 좌표들 중 index 12의 위치를 (x, y, z)로 출력되게 해주세요
        # index = 12
        # landmark = one_hand.landmark[index]
        # print(f"탐지 결과: \n\t")
        # print(landmark.x, landmark.y, landmark.z)
        # 2번. 4, 8, 12, 16, 20번의 좌표를 담은 리스트를 만들어주세요
        # [(x,y), (x,y), (x,y), (x,y), (x,y)]
        # height, width, _ = frame.shape

        # collect_xy = []
        # select_list = [4, 8, 12, 16, 20]
        # for idx in select_list:
        #     x = one_hand.landmark[idx].x
        #     y = one_hand.landmark[idx].y
        #     collect_xy.append((x,y))

        #     point_x = int(x * width) 
        #     point_y = int(y * height)
        #     cv2.circle(frame, (point_x, point_y), 5, (0,0,255), 2, lineType=cv2.LINE_AA)
        # print(collect_xy)
        ##### 프린트 테스트 #####

    ########## Hands ##########

    # 사진 보여주기
    cv2.imshow("webcam", frame)

    # 꺼지는 조건 설정
    key = cv2.waitKey(1)
    # ESC누르면 꺼짐 - ASCII 코드
    if key == 27:
        break 

vcap.release()
cv2.destroyAllWindows()