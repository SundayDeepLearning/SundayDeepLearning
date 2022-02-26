import glob
import os.path as osp
import torch.utils.data as data
from torchvision import models, transforms
from PIL import Image


class ImageTransform():
    """
    이미지 전처리 클래스, 훈련/추론 시의 동작이 다름
    이미지 크기 리사이즈 및 색상 표준화
    훈련 시 RandomResizedCrop 및 RandomHorizontalFlip을 통한 데이터 augmentation 진행


    Attributes
    ----------
    resize : int
        크기 변경 전의 이미지 크기
    mean : (R, G, B)
        각 생상 채널의 평균값
    std : (R, G, B)
        각 색상 채널의 표준편차
    """

    def __init__(self, resize, mean, std):
        self.data_transform = {
            'train': transforms.Compose([
                transforms.RandomResizedCrop(
                    resize, scale=(0.5, 1.0)),  
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),  
                transforms.Normalize(mean, std)  
            ]),
            'val': transforms.Compose([
                transforms.Resize(resize),  
                transforms.CenterCrop(resize),  
                transforms.ToTensor(),  
                transforms.Normalize(mean, std)  
            ])
        }

    def __call__(self, img, phase='train'):
        """
        Parameters
        ----------
        phase : 'train' or 'val'
            전처리 모드 설정
        """
        return self.data_transform[phase](img)


def make_datapath_list(phase="train"):
    """
    데이터 경로를 저장한 리스트 작성

    Parameters
    ----------
    phase : 'train' or 'val'
        훈련 데이터 또는 검증 데이터 지정

    Returns
    -------
    path_list : list
        데이터 경로를 지정한 리스트 작성
    """

    rootpath = "./data/hymenoptera_data/"
    target_path = osp.join(rootpath+phase+'/**/*.jpg')
    print(target_path)

    path_list = [] 

    for path in glob.glob(target_path):
        path_list.append(path)

    return path_list


class HymenopteraDataset(data.Dataset):
    """
    개미와 벌 화상의 Dataset클래스. PyTorch의 Dataset클래스 상속

    Attributes
    ----------
    file_list : 리스트
        이미지 경로를 저장한 리스트
    transform : object
        전처리 클래스의 인스턴스
    phase : 'train' or 'val'
        train, val 분류
    """

    def __init__(self, file_list, transform=None, phase='train'):
        self.file_list = file_list  
        self.transform = transform  
        self.phase = phase  

    def __len__(self):
        '''이미지 개수 반환'''
        return len(self.file_list)

    def __getitem__(self, index):
        '''
        전처리한 이미지의 Tensor데이터와 라벨 추출
        '''

        img_path = self.file_list[index]
        img = Image.open(img_path)  

        img_transformed = self.transform(
            img, self.phase)  

        if self.phase == "train":
            label = img_path[30:34]
        elif self.phase == "val":
            label = img_path[28:32]

        if label == "ants":
            label = 0
        elif label == "bees":
            label = 1

        return img_transformed, label
