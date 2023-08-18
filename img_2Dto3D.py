#多个图像按照z轴进行叠加，2D变成3D图像
import os
from glob import glob
import SimpleITK as sitk
import nibabel as nib
import numpy as np
import re

from PIL import Image
import numpy as np

source_path="E:\\bigorgs\\cardiovascular\\workspace\\Medical_tools\\output\\coronal/"
save_path="E:\\bigorgs\\cardiovascular\\workspace\\Medical_tools\\output"

files = glob(source_path+'/*.png')


def natural_sort(l):        #排序
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

files=natural_sort(files)


images = []

for file in files:

    filename = os.path.basename(file)

    image = Image.open(file)  # 用PIL中的Image.open打开图像              与原始图像不一致，是否是读取的问题
    image_arr = np.array(image)

    images.append(image_arr)

data = np.asarray(images)


#axis change setting
#none

#saggittal change setting
# data = data.swapaxes(0,1)
# data = data.swapaxes(1,2)
# data=np.flipud(data)     #上下翻转

#coronal change setting
data = data.swapaxes(0,1)
data=np.flipud(data)     #上下翻转


data_img=sitk.GetImageFromArray(data)

save_path = "E:\\bigorgs\\cardiovascular\\workspace\\Medical_tools\\output"
sitk.WriteImage(data_img,os.path.join(save_path, 'coronal.nii.gz'))


# np.savez( os.path.join(save_path,  'sagittal.npz'),data)

# img = nib.Nifti1Image(data, np.eye(4))
# nib.save(img, os.path.join(save_path,  'axis.nii.gz'))
