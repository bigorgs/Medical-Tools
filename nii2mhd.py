import os
from glob import glob

import SimpleITK as sitk

def listdir(path):
    dirs = os.listdir(path)
    dirs.sort()  # 扫描和标签的文件名不完全相同，对两个目录下的所有文件进行排序可以保证二者能匹配上
    return dirs

scan_dir = "E:\\bigorgs\\Coronary\\3D\\CTA\\plaque\\cta\\normal\\" # CT扫描数据路径
# scan_dir="E:\\bigorgs\\cardiovascular\\workspace\\Medical_tools\\output"

output_dir = "labels"
# scan_output = os.path.join(output_dir, "images") # CT图片输出路径

# if not os.path.exists(scan_output):
#     os.makedirs(scan_output)


def nii2mhd(file_path,save_path):
    path=save_path
    files = glob(file_path + '/*.nii.gz')

    for file in files:
        itk_img = sitk.ReadImage(file)
        # shape=itk_img.shape
        filename = os.path.basename(file)
        save_path=os.path.join(path, filename[-10:-7] + '.mhd')
        sitk.WriteImage(itk_img, save_path)
        print('convert success:'+save_path)


nii2mhd(scan_dir,output_dir)


