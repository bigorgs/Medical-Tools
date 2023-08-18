#多个图像按照z轴进行叠加，2D变成3D图像

import os
from glob import glob
import SimpleITK as sitk
import nibabel as nib
import numpy as np
import re

from PIL import Image
import numpy as np
from scipy.ndimage import rotate

source_path="./output/sagittal/"
save_path="./output"

files = glob(source_path+'/*.png')

def natural_sort(l):        #排序
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

files=natural_sort(files)
# files.reverse()



flag=True
for file in files:

    filename = os.path.basename(file)

    image = Image.open(file)  # 用PIL中的Image.open打开图像              与原始图像不一致，是否是读取的问题
    image_arr = np.array(image)  # 转化成numpy数组
    # image_arr = np.fliplr(image_arr)  # 左右翻转
    # image_arr = np.rot90(image_arr, -1)



    if flag :                     #默认等于第一张的numpy矩阵
        data=image_arr
        flag=False
    else :
        # data_shape=data.shape
        # image_arr_shape = image_arr.shape

        data_dim=data.ndim
        image_dim=image_arr.ndim

        if data_dim ==2 :
            data = np.expand_dims(data, axis=2)

        if image_dim ==2 :
            image_arr = np.expand_dims(image_arr, axis=2)

        # image_arr = np.resize(image_arr, data_shape)
        # data=np.stack((data,image_arr),axis=2)

        data=np.concatenate((data, image_arr), axis = 2)


print(data.shape)

# a = np.zeros((131,512,512)).astype(np.uint8)

#数组变换
#旋转
# data = np.rot90(data,-1)        #旋转90，负数顺时针

#翻转
# data=np.flipud(data)     #上下翻转
# data = np.fliplr(data)         #左右翻转

# data=np.flip(data,axis=0)
# data=np.flip(data,axis=1)

#维度交换

# data = data.swapaxes(1,2)
data = data.swapaxes(0,2)

#转置
# data = data.transpose((0, 2, 1))
# data = data.transpose((1, 2, 0))

# data=data[:,::-1,:]



# print(data.shape)

img = nib.Nifti1Image(data, np.eye(4))

nib.save(img, os.path.join(save_path,  'sagittal.nii.gz'))
