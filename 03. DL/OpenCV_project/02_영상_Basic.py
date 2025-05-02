import sys 
import cv2 

vcap = cv2.VideoCapture(0)

while True:
    # ret : 작동 여부
    # frame : 카메라로 받은 이미지지
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다")
        sys.exit()
    
    # print(type(frame))
    # print(frame)

    # 좌우 반전
    flipped_frame = cv2.flip(frame, 1)

    # 사진 보여주기
    cv2.imshow("webcam", flipped_frame)

    # 꺼지는 조건 설정
    key = cv2.waitKey(1)
    # ESC누르면 꺼짐 - ASCII 코드
    if key == 27:
        break 

vcap.release()
cv2.destroyAllWindows()