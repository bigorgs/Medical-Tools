#重新分割图像
"""
根据冠脉标签分割原始图像
so：原始图像只包含冠脉，之后作为分割钙化的数据集
"""
import os
from glob import glob

import SimpleITK as sitk  #读取nii文件

import numpy as np


coronary_Dir="E:\\bigorgs\\Conary\\3D\\3Dseg\\cta\\unnormal/"

coronarylabel_Dir="E:\\bigorgs\\Conary\\3D\\Conary\\labels\\repair_coronary/"

dst_path="./output/nifty/"

coronary_files = glob(coronary_Dir+'/*.nii.gz')

for coronary_file in coronary_files:

    filename = os.path.basename(coronary_file)              #带后缀，如：1.nii.gz

    coronarylabel_path=coronarylabel_Dir+filename

    coronary_sitkImage = sitk.ReadImage(coronary_file)          #读取原始图像nii.gz文件
    coronarylabel_sitkImage = sitk.ReadImage(coronarylabel_path)          #读取冠脉nii.gz文件

    coronary_npImage = sitk.GetArrayFromImage(coronary_sitkImage)    #simpleITK 转换成numpy
    coronarylabel_npImage = sitk.GetArrayFromImage(coronarylabel_sitkImage)    #simpleITK 转换成numpy

    # coronaryImage_copy=coronary_npImage.copy()
    # depth,  height, width = coronary_npImage.shape

    coronary_npImage[coronarylabel_npImage == 0] = coronary_npImage.min()                      #把冠脉等于0的位置都等于最小HU值，使原始图像只有冠脉

    # cor_gray_img = np.rot90(coronary_npImage, k=2)

    outImage = sitk.GetImageFromArray(coronary_npImage)     #numpy 转换成simpleITK

    outImage.SetSpacing(coronary_sitkImage.GetSpacing())    #设置和原来nii.gz文件一样的像素空间
    outImage.SetOrigin(coronary_sitkImage.GetOrigin())      #设置和原来nii.gz文件一样的原点位置

    sitk.WriteImage(outImage,os.path.join(dst_path,filename))#保存文件

    print(filename+"修改完成！")

print("finish!all in !!!")