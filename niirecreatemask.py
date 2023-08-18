
#重新制作Mask标签
import os
from glob import glob

import SimpleITK as sitk  #读取nii文件

def createNewMask(file_path,dst_path):
    file_base_name = os.path.basename(file_path)
    sitkImage = sitk.ReadImage(file_path)          #读取nii.gz文件
    npImage = sitk.GetArrayFromImage(sitkImage)    #simpleITK 转换成numpy
    npImage_1=npImage.copy()
    # npImage_2=npImage.copy()
    npImage[npImage_1 >= 1 ] =1                       #把大于0的标签都变成1，就是所有病区都要
    # npImage[npImage_1 == 0 ] =1                       #把大于0的标签都变成1，就是所有病区都要
    outImage = sitk.GetImageFromArray(npImage)     #numpy 转换成simpleITK
    outImage.SetSpacing(sitkImage.GetSpacing())    #设置和原来nii.gz文件一样的像素空间
    outImage.SetOrigin(sitkImage.GetOrigin())      #设置和原来nii.gz文件一样的原点位置
    sitk.WriteImage(outImage,os.path.join(dst_path,file_base_name))#保存文件

baseDir="E:\\bigorgs\\cardiovascular\\workspace\\Unet\\Cac_Unet\\output\\compare\\CCTA\\caijianlabels/"
dst_path="./output/nifty"
files = glob(baseDir+'/*.nii.gz')

for file in files:
    createNewMask(file,dst_path)

print("finish!")