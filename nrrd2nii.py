'''
本代码有问题
无法保留nrrd的原始信息，替代方案使用itk-snap完成nrrd2nii转换
'''


import os
from glob import glob

import nrrd
import nibabel as nib
import numpy as np

# nrrd 文件保存路径
nrrd_path=r'E:\bigorgs\Conary\3D\Conary\labels\nrrd'
save_path='E:\\bigorgs\\cardiovascular\\workspace\\Medical_tools\\output\\nifty'

files = glob(nrrd_path+'/*.nrrd')
for file in files:
    data,options=nrrd.read(file)  # 读取 nrrd 文件

    img=nib.Nifti1Image(data,np.eye(4)) # 将 nrrd 文件转换为 .nii 文件

    filename = os.path.basename(file)
    path = os.path.join(save_path, filename[:-5] + '.nii.gz')

    nib.save(img,path) # 保存 nii 文件

print("Finish!")