import os
import cv2
import shutil

# 이미지 및 라벨 폴더 경로
image_folder = "../rawData/training/image_02"
label_folder = "../rawData/label_02"

# 출력 폴더 경로
output_folder = "yolov5/dataset"

output_train_image_folder = os.path.join(output_folder, "images/train")
output_test_image_folder = os.path.join(output_folder, "images/test_dataset")

output_train_label_folder = os.path.join(output_folder, "labels/train")
output_test_label_folder = os.path.join(output_folder, "labels/test_dataset")

# 출력 폴더 생성
os.makedirs(output_train_image_folder, exist_ok=True)
os.makedirs(output_test_image_folder, exist_ok=True)

os.makedirs(output_train_label_folder, exist_ok=True)
os.makedirs(output_test_label_folder, exist_ok=True)

# train, validation, test 데이터셋 폴더 범위
train_range = range(18)
test_range = range(18, 21)

def convert_to_yolo_format(image_width, image_height, x_min, y_min, x_max, y_max):
    # YOLO 포맷으로 변환(+normalization)
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min

    x_center /= image_width
    y_center /= image_height
    width /= image_width
    height /= image_height

    return x_center, y_center, width, height

# txt 파일 생성 및 이미지 복사, 이름 변경
def create_yolo_txt(image_folder, label_file, output_image_folder, output_label_folder):
    # 라벨 파일 이름에서 프레임 번호 추출
    frame_number = label_file.split('.')[0]

    count = label_file.split('.')[0]

    # 폴더명(4자리 숫자)
    folder_number = frame_number.zfill(4)

    # 파일명(6자리 숫자)
    frame_number = frame_number.zfill(6)

    # 이미지 파일 이름 생성
    image_file = frame_number + '.png'

    # 이미지 파일 경로
    image_path = os.path.join(image_folder, folder_number, image_file)

    # 이미지 읽기
    image = cv2.imread(image_path)
    if image is None:
        return

    # 이미지의 크기 가져오기
    image_height, image_width, _ = image.shape

    # 라벨 파일 경로
    label_path = os.path.join(label_folder, label_file)

    # 프레임 번호를 기준으로 딕셔너리 초기화
    frame_labels = {}

    # 라벨 파일 읽기
    with open(label_path, 'r') as label_file:
        lines = label_file.readlines()

    for line in lines:
        elements = line.split()

        frame_number = elements[0]
        class_label = elements[2]

        x_min = float(elements[6])
        y_min = float(elements[7])
        x_max = float(elements[8])
        y_max = float(elements[9])

        x_center, y_center, width, height = convert_to_yolo_format(image_width, image_height, x_min, y_min, x_max, y_max)

        if class_label == 'Car':
            new_line = f"{0} {x_center} {y_center} {width} {height}\n"
        else:
            new_line = ""

        # 프레임 번호를 기준으로 딕셔너리에 추가
        if frame_number in frame_labels:
            frame_labels[frame_number].append(new_line)
        else:
            frame_labels[frame_number] = [new_line]

    for frame_number, labels in frame_labels.items():
        # 출력 파일 이름을 6자리 숫자로 만들기
        output_filename = f"{folder_number}_{frame_number.zfill(6)}.txt"

        # 출력 폴더 선택
        if int(count) in train_range:
            output_folder = output_train_label_folder
            output_img_folder = output_train_image_folder
        else:
            output_folder = output_test_label_folder
            output_img_folder = output_test_image_folder

        # 출력 파일 경로 설정
        output_path = os.path.join(output_folder, output_filename)

        # 라벨을 텍스트 파일에 기록
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.writelines(labels)

        # 해당 라벨 파일에 대응하는 이미지를 복사
        img_file = frame_number.zfill(6) + '.png'
        old_image_path = os.path.join(image_folder, folder_number, img_file)
        new_image_name = f"{folder_number}_{frame_number.zfill(6)}.png"
        new_image_path = os.path.join(output_img_folder, new_image_name)
        shutil.copy(old_image_path, new_image_path)

    print("{} done!\n".format(frame_number))


# 모든 라벨 파일에 대해 처리
for label_file in os.listdir(label_folder):
    if label_file.endswith(".txt"):
        create_yolo_txt(image_folder, label_file, output_train_image_folder, output_train_label_folder)
        create_yolo_txt(image_folder, label_file, output_test_image_folder, output_test_label_folder)

print("done")