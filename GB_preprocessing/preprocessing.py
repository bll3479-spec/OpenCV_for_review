#임포트
import cv2, os
import numpy as np
import matplotlib.pyplot as plt



#함수
#딥러닝 강건성 올려줄 'augmentation(증강)'
#1. 사이즈 수정
# 사이즈 수정 함수 -> input: image_path / -> output: 크기가 수정된 이미지
def image_resize(image, target_size, option = 1):
    #image = cv2.imread(image_path)

    inter = {1: cv2.INTER_NEAREST,
             2: cv2.INTER_LINEAR,
             3: cv2.INTER_CUBIC,
             4: cv2.INTER_AREA,
             5: cv2.INTER_LANCZOS4}

    option = inter[option]

    #이미지가 경로에 없거나, 오류 -> image = none
    if image is not None:
        #target_size=(224,224) 형태로
        image = cv2.resize(image, target_size, interpolation=option)
    else:
        print(f'이미지가 경로에 없습니다.')
    return image

#2. 회전
#image: 회전 시킬 이미지 (ndarray)
#angle: 회전 시킬 각도 (int)
#scale: 회전 후 전체 사이즈 변경 시(float)
def image_rotate(image, angle, scale = 1.0):
    h, w = image.shape[:2]                                                          #image.shape(h,w,c)
    center = (w//2, h//2)                                                           #'//': 나누어 떨어지게 하기 (몫)
    M = cv2.getRotationMatrix2D(center,angle,scale)                                 #center, angle, scale 알아서 생성
    print(M)
    return cv2.warpAffine(image, M, (w,h))


#3. shear 변환
def image_shear(image, shear_ratio=0.2):
    h,w = image.shape[:2]                                                            #원본에 같은 w,h를 저장해두는 편이 좋음
                       
                        #이미지 왼쪽 위, 오른쪽 위, 왼쪽 아래                             #아핀변환에는 3가지 포인트가 필요해~ (-1의 이유: 파이썬 순서니꽈,,)
    src_pts = np.float32([[0,0],[w-1, 0], [0,h-1]])                                  #시작(source points)
    dst_pts = np.float32([[0,0],[w-1, 0], [int(shear_ratio*w),h-1]])                 #끝(destination points)

    M = cv2.getAffineTransform(src_pts, dst_pts)
    return cv2.warpAffine(image, M, (w,h))


#4. 좌우반전 (flip)
def image_flip(image, flip_num =1):
    return cv2.flip(image, flip_num)                                                #flip_num옵션: 1(좌우반전) / 0 (상하반전) / -1(좌우, 상하반전)

#5. ROI(Region of Interest) -> Crop
def image_crop(image, ratio):
    h,w =image.shape[:2]
    margin=(1-ratio)/2

    #ratio 중앙에서 몇 %까지만 픽셀 살릴지 결정
    x1 = int(w*margin) 
    y1 = int(h*margin)
    x2 = int(w*(1-margin))
    y2 = int(h*(1-margin))
    image = image[y1:y2, x1:x2]
    return image


#진입점
# if __name__ == '__main__':
#     #이미지 경로, target_size
#     image_path = r'C:\Users\user\Desktop\Git\OpenCV\GB1.JPG'
#     image1 = image_resize(image_path, (100,100), 4)
    
#     #rotate확인 :image = image_rotate(image1, 180)
#     #image = image_shear(image1, 0.5)
#     image = image_crop(image1, 0.5)
#     image = image_flip(image, 1)
#     plt.imshow(image)
#     plt.show()
    
    
    #print(type(image1), type(image2))                          #결과: <class 'numpy.ndarray'> <class 'numpy.ndarray'> -> 픽셀 값이 2,3,4의 함수들로 들어감

    # 옵션 2개 설정한 화면 동시에 
    # fig, ax = plt.subplots(1,2)
    # ax[0].imshow(image1)
    # ax[1].imshow(image2)
    # plt.show()

