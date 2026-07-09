#1.임포트
import os, cv2
import matplotlib.pyplot as plt 
import numpy as np

#2.함수
#1.이미지 피라미드 => 타겟이미지의 크기를 자동으로 작->큰 변환하면서 비교
#타겟이미지가 배경이미지보다 크거나, 너무 작은 경우 탐색을 잘 하기 위해서 크기를 변경
def image_pyramid(target_image, scale=0.8, min_size=(10, 10)):
    #이미지를 크기별로 축소->확대
    #이 이미지를 리스트에 담아서 보관
    pyramid = []                    #이미지 샘플 리스트 만듦
    pyramid.append(target_image)    #원본 이미지가 먼저 들어감

    #일정한 비율로 줄이거나 늘림 => 일정한 비율(scale)로 줄임
    while True:
        #피라미드에 가장 마지막으로 들어간 이미지를 temp라고 부름
        temp = pyramid[-1] 
        #temp의 가로 * 0.8, temp의 세로 * 0.8 ....> 마지막 10, 10보다 작아지면 중단
        h, w = temp.shape[:2]
        new_h = int(h*0.8)
        new_w = int(w*0.8)
        #새로 찾은 new_w, new_h가 최소 사이즈(10,10)보다 작은가? 
        #작으면 -> break
        if new_h < min_size[1] or new_w < min_size[0]:
            break
        resized = cv2.resize(temp, (new_w, new_h))
        pyramid.append(resized)

    return pyramid


#2.슬라이딩 윈도우
#input = 배경이미지 + 타겟이미지 + 옆으로 몇 칸 밀면서 비교할거니?(step)
def sliding(back, target, step=4):
    #배경이미지의 크기가 타겟 이미지의 크기보다 커야함.
    bh, bw = back.shape[:2]
    th, tw = target.shape[:2]
    if bh < th or bw < tw: #배경이미지가 타겟이미지보다 작은경우
        return -1, None   #2개의 '실패'값을 돌려줌
    
    #정교한 비교 < 정규화(normalized) 0~1 일정한 범위내로 만듦 0~255
    #(원본 - 평균 / 표준편차)
    target_f = target.astype('float32')
    target_n = target_f - target_f.mean() #원본 - 평균
    target_std = target_f.std() + 1e-5 #표준편차 구하기

    #초기화(리턴할 값 / 최고 유사도, 최고의 위치) 
    #-1, None, => 관련없는 값으로 '초기화'
    best_score, best_loc = -1, None

    for y in range(0, bh-th+1, step):
        for x in range(0, bw-tw+1, step):
            window = back[y:y+th, x:x+tw].astype('float32')
            window_n = window - window.mean()
            window_std = window.std() + 1e-5
            #데이터 간의 상관관계 구하기
            score = np.sum(window_n * target_n) / (window_std * target_std * th * tw)

            if score > best_score:
                best_score = score
                best_loc = (x, y)
    return best_score, best_loc


#따로 함수로 만들것인가? -> 함수가 image_pyramid, sliding 관리
#그냥 진입점에서 실행시킬 것인가? image_pyramid, sliding 실행
def sliding_scan(back, target):
    #1. 이미지 피라미드를 실행해서 이미지 샘플을 얻는다.
    #pyramid = [target, target*0.8, target*0.8*0.8, ...]
    pyramid = image_pyramid(target, 
                  scale=0.8, 
                  min_size=(10, 10))
    
    #모든 샘플 이미지를 통틀어서 가장 좋은 결과
    best_score = -1
    best_loc = None 
    
    #최종 시각화, 몇 배율 가장 좋았니? / 최종 샘플 너비*높이
    best_scale = 1.0
    best_shape = None #(x, y)

    #2. 이미지 피라미드 안의 샘플(사이즈)별로 스캔(슬라이딩)을 한다.
    for sample in pyramid:
        score, loc = sliding(back, sample)
        #기존 sample의 best보다 현재 sample의 score가 더 좋은경우
        #현재 score로 best를 갱신
        if best_score < score :
            best_score = score 
            best_loc = loc
            best_scale = back.shape[1] / sample.shape[1]
            best_shape = sample.shape
    print(f'최고 유사도 {best_score:.2f}, 축소배율 : {best_scale:.2f}')

    #3.최종적으로 best matching을 얻는다.
    return best_score, best_loc

#3.진입점
if __name__ == '__main__':
    #함수 -> input(자료형), output(자료형)
    target_path = r'C:\Users\jeong\Desktop\OpenCV_L\round.jpg'
    target_image = cv2.imread(target_path)
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    back_path = r'C:\Users\jeong\Desktop\OpenCV_L\hidePic.jpg'
    back_image = cv2.imread(back_path)
    back_image = cv2.cvtColor(back_image, cv2.COLOR_BGR2GRAY)
    best_score, best_loc = sliding_scan(back_image, target_image)




    #target_image -> numpy배열로 변환된 이미지 -> image_pyramid
    #pyramid = image_pyramid(target_image)
    # print(target_image.shape)
    # print(len(pyramid))
    # print(pyramid[-1].shape)
