import cv2
import numpy as np

video_path = r'C:\Users\user\Desktop\Git\OpenCV\bird.mp4'

#비디오 컨트롤 시 주의사항
#비디오 == 연속된 싱글 이미지(이미지를 시간 순서에 따라 빠르게 출력)
#fps(초당 프레임 수)
#동영상을 열기 위하 '스크린' 준비
cap = cv2.VideoCapture(video_path)

while True:
    #imread()랑 비슷
    #ret(동영상 읽기가 성공했는지: T/F)
    #image(그 초에 해당하는 이미지 한 장)
    ret, image = cap.read()

    if ret == False:
        print('동영상 읽기 실패')
        break
    #동영상 읽기 성공(True)이라면, 동영상 재생
    cv2.imshow('video', image)

    #창을 띄운 후 - 끄는 코드
    key = cv2.waitKey(1)        #1ms 기다림(비가시)
    if key==27:     #키보드 -> ASCII, 'Esc'
        break

#영상을 출력하지 않으면 '자원 해제(릴리즈)'
#이 데이터가 RAM에 올라갔다!
cap.release()
cv2.destroyAllWindows()