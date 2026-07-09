# 특징자 + 템플릿 매칭으로 '유사한 형태' 위치 찾기
# '이미지 피라미드'와 '자동 회전' 활용하기
import cv2
import numpy as np
import matplotlib.pyplot as plt

#특징자 -> ORB, SIFT / AKAZE, HOG.. :특징 추출
# 1. 특징 추출(배경 + 타겟)
# 2. 추출한 특징 매칭 -> 매칭 알고리즘 Brute Force / Flann 
# 3. 매칭한 결과 시각화
#4. + 이미지 피라미드, 자동 회전
def match_descriptor(back, target):
    back_image = cv2.imread(back)
    back_image = cv2.cvtColor(back_image, cv2.COLOR_BGR2GRAY)

    target_image = cv2.imread(target)
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    #특징을 sift 방법으로 추출할 객체(SIFT_create)를 만듦
    sift = cv2.SIFT_create()

    #특징 (detectAndCompute) -> 매처 (Brute Force, Flann) = 굿 매치 선택
    kp1, des1 = sift.detectAndCompute(back_image, None)
    kp2, des2 = sift.detectAndCompute(target_image, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    #좋은 매칭점 찾기
    good_matches = []
    # m(첫번째로 가까운), n(두번째로 가까운)
    for m,n in matches:
        # 첫번째 거리< 0.75*두번째 거리
        if m.distance <0.75 * n.distance:
            good_matches.append(m)
    print(f'좋은 매칭 개수: {len(good_matches)}')


    #시각화
    MIN_MATCH_COUNT = 10
    if len(good_matches) < MIN_MATCH_COUNT:
        print('매칭 개수가 충분하지 않습니다.')
        match_mask = None
    else:
        #reshape: 내가 원하는 형태로 배열 변형
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)
        #마스크 만들기 (시작점, 끝점의 범위에서 찾기)
        #ransac: 두 이미지 사이의 공간관계를 찾는 알고리즘. src와 dst 사이의 위치. 5는 오차범위
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        
        matches_mask = mask.ravel().tolist()        #reshape() 형태 변환

        ht, wt =back_image.shape
        corners = np.float32([[0,0], [0,ht], [wt,0],[wt,ht]]).reshape(-1,1,2)
        #perspective 변환: 길이 변화 있음
        transforms = cv2.perspectiveTransform(corners, M)
        cv2.polylines(back_image, [np.int32(transforms)], True, (0,255,0), 5)
                        #선 색깔, 단일 점 색상, 마스크의 위치(전달), 2 = 매칭 안된 점 무시
    draw_params = dict(matchColor = (255, 0, 0), singlePointColor = None, matchesMask = matches_mask, flags =2)
    
    #배경과 타겟을 나란히 놓고 그림
    match_image = cv2.drawMatches(back_image, kp1, target_image, kp2, good_matches, None, **draw_params)        
    #**(언패킹, 변수 이름): 위에 정의한 변수 갖다 쓰쇼. -> 나열할 수 있는 매개변수값을 하나로 붂어서 함수 안에 '풀어서 써' 전달.

    plt.imshow(match_image)
    plt.show()


#템플릿 매칭
def match_template(back, target):
    back_image = cv2.imread(back)
    back_image = cv2.cvtColor(back_image, cv2.COLOR_BGR2GRAY)

    target_image = cv2.imread(target)
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(back_image, target_image,cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    h,w = target_image.shape

    top_left = max_loc
    bottom_right = (top_left[0]+w, top_left[1] + h)

    print(f'최대 유사도: {max_val:.4f}(1에 가까울수록 일치 높음)')

    temp_image = back_image.copy()
    cv2.rectangle(temp_image, top_left, bottom_right, (255,255,0), 5)


    #중간점검(1행 2열로 시각화)
    fig, ax = plt.subplots(1,2)
    ax[0].imshow(temp_image)
    ax[1].imshow(result, cmap = 'hot')
    plt.show()

if __name__ == '__main__':
    background_image = r'C:\Users\user\Desktop\Git\OpenCV\0707\practice_0707\card.png'
    target_image = r'C:\Users\user\Desktop\Git\OpenCV\0707\practice_0707\card_part.png'

    #템플릿 매칭
    #match_template(background_image, target_image)

    #특징자 매칭
    match_descriptor(background_image, target_image)