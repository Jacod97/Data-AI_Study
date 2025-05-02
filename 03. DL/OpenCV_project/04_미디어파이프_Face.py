import sys 
import cv2 
import mediapipe as mp 

# Mediapipe의 Face Landmark를 추출.그리기 위한 설정
mp_face_detection = mp.solutions.face_detection 
mp_drawing = mp.solutions.drawing_utils 
mp_face_mesh = mp.solutions.face_mesh

face_detection = mp_face_detection.FaceDetection(
    model_selection=0,      # 0: 근거리, 1: 원거리
    min_detection_confidence=0.5
)

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    refine_landmarks=True       # iris tracking 기능 추가
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
    flipped_frame = cv2.flip(frame, 1)

    ########## Face ##########
    # 얼굴 그리기 설정
    frame.flags.writeable = True 

    # 얼굴 감지 수행 
    detection_results = face_detection.process(frame)

    # 얼굴 Mesh 감지 수행
    mesh_results = face_mesh.process(frame)

    # 그리기 - Face 찾기
    # if detection_results.detections:
    #     for detection in detection_results.detections:
    #         mp_drawing.draw_detection(frame, detection)
    
    # 그리기 - Mesh 
    if mesh_results.multi_face_landmarks:
        for face_landmarks in mesh_results.multi_face_landmarks:
            # mp_drawing.draw_landmarks(
            #     image=frame,
            #     landmark_list=face_landmarks,
            #     connections=mp_face_mesh.FACEMESH_TESSELATION,
            #     landmark_drawing_spec=None,
            #     connection_drawing_spec=mp_drawing.DrawingSpec(
            #         color=(0,255,0),
            #         thickness=1,
            #         circle_radius=1
            #     )
            # )

            # 그리기 - 직접 그리기
            height, width, _ = frame.shape 
        
            select_list = [469, 470, 471, 472, 474, 475, 476, 477]
            for idx in select_list:
                x = face_landmarks.landmark[idx].x
                y = face_landmarks.landmark[idx].y

                point_x = int(x * width)
                point_y = int(y * height)

                cv2.circle(frame, (point_x, point_y), 1, (0,0,255), 2, lineType=cv2.LINE_AA)
    ########## Face ##########

    # 사진 보여주기
    cv2.imshow("webcam", frame)

    # 꺼지는 조건 설정
    key = cv2.waitKey(1)
    # ESC누르면 꺼짐 - ASCII 코드
    if key == 27:
        break 

vcap.release()
cv2.destroyAllWindows()