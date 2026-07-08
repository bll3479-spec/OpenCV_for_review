import cv2
import numpy as np
import random

#설계
#마우스가 눌렸는지?
is_pressed = False

#사각형을 그리는지, 원을 그리는지?(토글)
is_rectangle = False

#도형 그리기 전에 "깨끗한 좌표" (초기화)
start_x, start_y, = -1, -1

#색깔
color = (255,255,255)


#마우스가 '눌려있다면' -> 이벤트를 감지할 함수 필요
#'콜백 함수'
def mouse_callback(event, x, y, flags, param):
    #전역 변수를 함수 내에서도 적용
    global color, start_x, start_y,is_pressed, is_rectangle

    #1. 이벤트 분류
    #지금 마우스가 움직이는가?
    if event == cv2.EVENT_MOUSEMOVE:
        if is_pressed == True:
        #사각형 그리기 모드
            if is_rectangle:
                cv2.rectangle(image, (start_x, start_y), (x,y), color, -1)      #마우스 시작점, 현재 마우스가 움직인 곳, 랜덤 컬러, 채워진 사각형 그리기(-1)
            #원 그리기 모드
            else:
                cv2.circle(image, (start_x, start_y), max(abs(start_x-x), abs(start_y-y)), color, -1)
    #1. 지금 왼쪽 버튼을 눌렀는가? (드래그)
    #왼쪽 버튼을 눌렀다 -> 그리기의 시작
    elif event == cv2.EVENT_LBUTTONDOWN:
        is_pressed = True                   #버튼 눌림 상태
        start_x, start_y = x, y             #누른 곳? 좌표
        #randrange(값): 0~1까지의 정수 랜덤값 만듦
        color = (
            random.randrange(256),      #R
            random.randrange(256),      #G
            random.randrange(256)       #B
        )
    #지금 눌린 상태가 해제되었는가?
    elif event == cv2.EVENT_LBUTTONUP:
        is_pressed = False
        #그림 완성
        #사각형 그리기 == True면 사각형, 그렇지 않으면 원
        if is_rectangle:                #전역변수로 정의하기를 false였는데?
            #이미지(캔버스)에, 지정한 시작점, 현재 마우스를 놓은 지점, 랜덤 지정 색, 선 두께
            cv2.rectangle(image, (start_x, start_y), (x,y), color, -1)
        else:
            #이미지에, 센터(시작된 지점 = 원의 중앙), 반지름, 원의 색깔, 선의 두께
            cv2.circle(image, (start_x,start_y), max(abs(start_x-x), abs(start_y-y)),color, -1)
    #오른쪽 마우스 버튼을 눌렀는가?
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        is_rectangle = not is_rectangle

#창 띄우기
cv2.namedWindow('Canvas')
image = np.zeros((512,512,3), np.uint8)         #(512,512,3): 세로, 가로, 채널
cv2.setMouseCallback('Canvas', mouse_callback)
while True:
    cv2.imshow('Canvas', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()