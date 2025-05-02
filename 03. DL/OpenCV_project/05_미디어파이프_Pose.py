import sys 
import cv2 
import mediapipe as mp 

# Mediapipe의 Pose Landmark를 추출.그리기 위한 설정
mp_pose = mp.solutions.pose 
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles 

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

vcap = cv2.VideoCapture(0)

while True:
    # ret : 작동 여부
    # frame : 카메라로 받은 이미지지
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다")
        sys.exit()
    
    # 좌우 반전
    frame = cv2.flip(frame, 1)

    ########## Pose ##########
    # 포즈 그리기 설정
    frame.flags.writeable = True
    
    # 포즈 감지 수행
    results = pose.process(frame)

    # 그리기
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )
    ########## Pose ##########

    # 사진 보여주기
    cv2.imshow("webcam", frame)

    # 꺼지는 조건 설정
    key = cv2.waitKey(1)
    # ESC누르면 꺼짐 - ASCII 코드
    if key == 27:
        break 

vcap.release()
cv2.destroyAllWindows()