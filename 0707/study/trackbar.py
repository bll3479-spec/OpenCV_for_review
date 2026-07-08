import cv2
import numpy as np

#슬라이더 동작 시 '비어있는 함수' 필요
#콜백 함수: 미리 등록되어 있는 함수.
#사용자가 창에 있는 슬라이더를 움직임 -> 움직임을 x라 하고 이 x를 실제 값에 전달해줌.
def on_trackbar(x):
    #이 함수가 실질적으로 뭔가 동작을 하는 것은 아님 
    pass

#'이런 이름'을 가진 창을 하나 띄워줌
cv2.namedWindow("사용자 인터랙션")
#cv2.createTrackbar(a,b,c,d,e)
#a: 트랙바 이름, b: 트랙바 '창'의 이름,
#c: 트랙바 최소값, d:최대값,
#e: 연결된 콜백 함수
cv2.createTrackbar('Low', "사용자 인터랙션", 0, 255, on_trackbar)
cv2.createTrackbar('High', "사용자 인터랙션", 0, 255, on_trackbar)

image_path = r'C:\Users\user\Desktop\Git\OpenCV\tomato.jpg'
#이미지를 가져옴
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image, (700,400))
while True:
    #변화
    low = cv2.getTrackbarPos('Low', "사용자 인터랙션")
    high = cv2.getTrackbarPos('High', "사용자 인터랙션")
    print(f'낮은 값 {low}, 높은 값 {high}')

    image_canny = cv2.Canny(image, low, high)
    
    #이미지를 보여줌
    cv2.imshow('사용자 인터랙션', image_canny)

    #종료 관련
    cv2.waitKey(1)
    #0xFF : 키가 눌렸다면 검사
    #== ord('q'): 눌린 키가 'q'키인지?
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()