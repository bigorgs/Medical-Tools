from PIL import Image
import numpy as np
import os

if __name__ == '__main__':
    work_dir = "E:\\bigorgs\\cardiovascular\\workspace\\Camouflage_target_detection\\ZoomNet-main\\output\\Calcification\\1\\Calcification_te\\"  # 图像所处文件夹
    file_names = os.listdir(work_dir)
    for file_name in file_names:
        # print(file_name) # ISIC_0000000_Segmentation.png
        file_path = os.path.join(work_dir, file_name)

        image = Image.open(file_path)
        img = np.array(image)
        img[img >0] = 255

        # 重新保存
        image = Image.fromarray(img, 'L')
        new_name = file_name[:-4]
        # new_name = new_name.strip("_Segmentation")  # 文件名处理成和图像一样的名字
        target_path="E:\\bigorgs\\cardiovascular\\workspace\\Camouflage_target_detection\\ZoomNet-main\\output\\Calcification\\1\\2\\"

        image.save(target_path + new_name +'.png')
