import cv2
import numpy as np

#경로: 절대/상대
#파라미터: image_path (내가 읽을 이미지 경로)
def image_read(image_path):
    image = cv2.imread(image_path)
    print(f'이미지 shape {image.shape}')

    #image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    #코랩에서는 cv2_imshow()였는데
    #로컬에서는 다음과 같이.
    #cv2.imshow(창의 이름, 창에 띄울 이미지)
    cv2.imshow('Hello, Image', image)
    cv2.waitKey(0)                          #입력이 새로 들어올 때까지 무한정 기다림.
    cv2.destroyAllWindows()                 #입력이 들어오면 창을 닫음

#진입점
if __name__ == '__main__':
    #함수 호출
    #경로는 다양한데(\ or // or (원화표시)), r'경로'로 설정하면 경로로 인식시킬 수 있음
    path = r'C:\Users\user\Desktop\Git\OpenCV\tomato.jpg'
    image_read(path)