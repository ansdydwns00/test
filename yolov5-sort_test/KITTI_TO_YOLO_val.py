import os
import shutil
from glob import glob
import random

# 경로 설정
images_path = 'yolov5/dataset/images/train'
labels_path = 'yolov5/dataset/labels/train'

train_images_output_path = 'yolov5/dataset/images/train_dataset'
train_labels_output_path = 'yolov5/dataset/labels/train_dataset'
valid_images_output_path = 'yolov5/dataset/images/valid_dataset'
valid_labels_output_path = 'yolov5/dataset/labels/valid_dataset'

# 출력 경로에 폴더가 없으면 생성
for path in [train_images_output_path, train_labels_output_path, valid_images_output_path, valid_labels_output_path]:
    os.makedirs(path, exist_ok=True)

# 경로에 있는 모든 이미지 파일 리스트 불러오기
image_files = glob(os.path.join(images_path, '*.png'))

# 랜덤하게 섞기
random.shuffle(image_files)

# 7대 3 비율로 나누기
num_train = int(len(image_files) * 0.7)
train_files = image_files[:num_train]
valid_files = image_files[num_train:]

# 함수 정의: 파일 복사 및 라벨 복사
def copy_files(files, images_output_path, labels_output_path, labels_path):
    for file in files:
        basename = os.path.basename(file)
        shutil.copy(file, os.path.join(images_output_path, basename))
        
        label_file = os.path.join(labels_path, basename.replace('.png', '.txt'))
        if os.path.exists(label_file):
            shutil.copy(label_file, os.path.join(labels_output_path, os.path.basename(label_file)))

# train 파일 복사
copy_files(train_files, train_images_output_path, train_labels_output_path, labels_path)

# valid 파일 복사
copy_files(valid_files, valid_images_output_path, valid_labels_output_path, labels_path)

print(f"완료: train 이미지 {len(train_files)}개, valid 이미지 {len(valid_files)}개 복사 완료.")

