#1. 커스텀 데이터셋 제작 방법
import os, cv2
import torch    #파이토치
#나의 커스텀 데이터 -> pytorch 형태로 변환
from torch.utils.data import Dataset, DataLoader

#클래스
class SimpleDataset(Dataset):
    #데이터셋의 기본 세팅에 필요한 내용을 전달
    def __init__(self,t):         #초기화, 객체를 만들때 세팅해줌(폴더, 참조 세팅 등 데이터셋에 필요한 재료)
        self.t =t
        #1. 이미지 폴더 경로 알려줌
        #오리진 폴더 안의 모든 이미지가 이미지 리스트 변수 안으로 저장됨.
        # image_list = [os.path.join('이미지 경로', x) for x in os.listdir('이미지 경로')]
        #2. 라벨 폴더 경로 알려줌

    def __len__(self):          #데이터셋이 갖고 있는 데이터의 개수
        return self.t
        #데이터셋 길이 변환이 필요한 이유: 딥러닝 데이터 엄청 많음
        #훈련에 쓰이는 '데이터'의 순서, 배치 사이즈 관련 역할 수행
        
    def __getitem__(self,idx):      #딥러닝 훈련시, '몇번째'에 해당하는 이미지+라벨 쌍 전달. 'idx': 몇번째
        return torch.LongTensor([idx])
        
        
#진입점
if  __name__ == '__main__':
    #SimpleDataset이라는 데이터셋을 만듦(객체 생성)
    #나의 10만개 데이터를 전처리해서 들고 있음
    ds1 = SimpleDataset(7)
    #한번에 훈련시킬 양만큼(1000) 떼어서 모델에게 전달
    dataloader = DataLoader(dataset = ds1, batch_size = 2, shuffle = True, drop_last = True)      
    #실제 훈련에 쓸 데이터셋 / 데이터셋을 쪼갤 기준(10의 n제곱, 2의 n제곱) / 데이터셋 학습시 편향 방지 위한 셔플 / 배치 사이즈만큼 묶어주고 남은 것도 안쓸건지 여부(지금은 7이라 1이 남음)

    for i in range(3):
        print(f'에포크 수:{i}')
        for batch in dataloader:
            print(batch)
            print(type(batch))



#openCV 시각화, 제작