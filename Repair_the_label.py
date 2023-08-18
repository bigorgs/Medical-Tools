#重新制作Mask标签
"""
根据斑块标签补充冠脉标签
有斑块的地方必有冠脉
"""
import os
from glob import glob

import SimpleITK as sitk  #读取nii文件

import numpy as np



coronary_Dir="E:\\bigorgs\\Conary\\3D\\Conary\\labels\\nifty/"

plaque_Dir="E:\\bigorgs\\Conary\\3D\\3Dseg\\label\\unnormal/"

dst_path="./output/repair_coronary/"

coronary_files = glob(coronary_Dir+'/*.nii.gz')

for coronary_file in coronary_files:

    filename = os.path.basename(coronary_file)              #带后缀，如：1.nii.gz

    plaque_path=plaque_Dir+filename

    coronary_sitkImage = sitk.ReadImage(coronary_file)          #读取冠脉nii.gz文件
    plaque_sitkImage = sitk.ReadImage(plaque_path)          #读取斑块nii.gz文件

    coronary_npImage = sitk.GetArrayFromImage(coronary_sitkImage)    #simpleITK 转换成numpy
    plaque_npImage = sitk.GetArrayFromImage(plaque_sitkImage)    #simpleITK 转换成numpy

    coronaryImage_copy=coronary_npImage.copy()

    depth,  height, width = coronary_npImage.shape
    # for i in range(depth):
    #     for j in range(height):
    #         for k in range(width):
    #             if plaque_npImage[i,j,k] == 1 and coronary_npImage[i,j,k] == 0:
    #                 coronaryImage_copy[i,j,k] = 1

    coronary_npImage[plaque_npImage == 1] =1                       #把斑块等于1的标签冠脉都变成1，使冠脉包含斑块

    # cor_gray_img = np.rot90(coronary_npImage, k=2)

    outImage = sitk.GetImageFromArray(coronary_npImage)     #numpy 转换成simpleITK

    outImage.SetSpacing(coronary_sitkImage.GetSpacing())    #设置和原来nii.gz文件一样的像素空间
    outImage.SetOrigin(coronary_sitkImage.GetOrigin())      #设置和原来nii.gz文件一样的原点位置

    sitk.WriteImage(outImage,os.path.join(dst_path,filename))#保存文件

    print(filename+"修改完成！")

print("finish!all in !!!")