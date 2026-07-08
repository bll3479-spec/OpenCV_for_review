#-*- coding : uft-8 -*-

#임포트
import os
import shutil
import preprocessing as pre
import matplotlib.pyplot as plt
import numpy as np
import cv2

#경로 컨트롤
from pathlib import Path
#이미지 -> 읽고 -> 넘겨주기 (1,2,3,4)
def encode_path(image_path):
    #파일을 읽어줌 -> binary 형식으로 자료를 읽음
    stream = np.fromfile(image_path, dtype = np.uint8)
    image = cv2.imdecode(stream, cv2.IMREAD_COLOR)
    return image


#진입점
if __name__ == '__main__':
    #전처리할 원본 소스가 존재하는 폴더 위치
    origin = r'C:\Users\user\Desktop\shKim\8주차_딥러닝\음식_이미지\원천데이터\합본_양추정_이미지_TRAIN\image\김밥\Q3'

    #전처리 한 결과물이 이동할 폴더 위치
    dst = r'C:\Users\user\Desktop\shKim\8주차_딥러닝\음식_이미지\원천데이터\합본_양추정_이미지_TRAIN\image\김밥\Q3_result'

    #내가 갖고 있는 파일의 이름 확인
    #os.listdir(경로): 경로에 존재하는 모든 파일 출력
    #os.path.join(경로 1, 경로 2): 경로 1, 2를 하나의 경로로 합침
    #origin 폴더 안에 있는 '모든 이미지'가 image_list 변수 안으로 저장
    image_list = ([os.path.join(origin, x) for x in os.listdir(origin)])
    print(len(image_list))

    #샘플 파일
    # image_list[0] # -> preprocessing의 1번 (2, 3, 4...)

    # #그림을 읽어오고, image로 변환
    for i in range(len(image_list)):
        image = encode_path(image_list[i])
        image = pre.image_resize(image, (224,224))

        #변환된 이미지(사이즈가 변경된 것)를 다른 디렉토리로 옮김
        temp_path = './temp.jpg'        #변경된 이미지 저장
        cv2.imwrite(temp_path, image)   #cv2로 만든 numpy 자료형을 '이미지'로 저장함

        #결과물 폴더로 보내기 전에: 폴더가 없을 경우를 고려해서 생성함. (dst) 폴더 있는지 여부를 묻고 없으면 생성
        if not os.path.exists(dst):
            os.makedirs(dst)
        #
        if 'top' in image_list[i]:
            filename = 'top' + image_list[i].split('Q')[-1]
            final_path = os.path.join(dst, filename)
        else:
            filename = 'side' + image_list[i].split('Q')[-1]
            final_path = os.path.join(dst, filename)

        shutil.copy2('./temp.jpg', final_path)


    #plt.imshow(image)
    #plt.show()