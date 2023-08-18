import os
from glob import glob

import cv2
import numpy as np
import nibabel as nib

import SimpleITK as sitk

#读取mhd
def read_mhd(mhd_dir):
    import SimpleITK as sitk
    # mhd_file = os.path.join(mhd_dir, '24.mhd')
    itkimage = sitk.ReadImage(mhd_dir)
    ct_value= sitk.GetArrayFromImage(itkimage)  # 这里一定要注意，得到的是[z,y,x]格式,
    direction = itkimage.GetDirection()  # mhd文件中的TransformMatrix
    origin = np.array(itkimage.GetOrigin())
    spacing = np.array(itkimage.GetSpacing())  # 文件中的ElementSpacing

    return ct_value


#设置窗宽、窗位
def set_window(img_data, win_width, win_center):
    img_temp = img_data
    min = (2 * win_center - win_width) / 2.0 + 0.5
    max = (2 * win_center + win_width) / 2.0 + 0.5
    dFactor = 255.0 / (max - min)

    img_temp = ((img_temp - min) * dFactor).astype(np.int)
    img_temp = np.clip(img_temp, 0, 255)
    return img_temp

#转换ElementSpacing空间
def resample(image, spacing, new_spacing=[1, 1, 1]):
    import scipy

    raw_shape = image.shape
    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape).astype(np.int)  # 返回浮点数x的四舍五入值。
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor
    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor, mode='nearest')  # 使用所请求顺序的样条插值来缩放数组。

#获取CT_VALUE
file_path="E:\\bigorgs\\Coronary\\3D\\CT\\normal\\"
axis_save_path='E:\\bigorgs\\cardiovascular\\workspace\\Medical_tools\\output\\axis\\'
cor_save_path='E:\\bigorgs\\cardiovascular\\workspace\\Medical_tools\\output\\coronal\\'
sag_save_path='E:\\bigorgs\\cardiovascular\\workspace\\Medical_tools\\output\\sagittal\\'

files = glob(file_path + '/*.nii.gz')

for file in files:
    ct_value=read_mhd(file)

    test=sitk.GetImageFromArray(ct_value)       #numpy to cta

    # save_path = "E:\\bigorgs\\cardiovascular\\workspace\\Medical_tools\\output"
    # sitk.WriteImage(test,os.path.join(save_path, 'test.nii.gz'))
    # nib.save(test, os.path.join(save_path, 'test.nii.gz'))

    # print(ct_value)

    #获取文件名
    filename = os.path.basename(file)


    #转换CT、ElementSpacing空间
    # image = resample(ct_value, spacing[::-1])  # spacing[::-1]是因为ct_value的顺序是[z,y,x]，而读入的spacing是[x,y,z]

    #获取图像三个切面图片
    ct_value_new = set_window(ct_value,750,90)            #窗宽：750；窗位（窗中心）：90


    # img = nib.Nifti1Image(ct_value_new, np.eye(4))
    # nib.save(img, os.path.join(save_path, 'axis_1.nii.gz'))

    # # k取DimSize 中的值
    # tar_img = ct_value_new[k, :, :] # 水平面
    # cor_img = ct_value_new[:, k, :] # 冠状面
    # sag_img = ct_value_new[:, :, k] # 矢状面

    a = ct_value.shape[0]
    b = ct_value.shape[1]
    c = ct_value.shape[2]


    print("---------开始转化------")
    #水平面
    for k in range(ct_value.shape[0]):
        # image
        # img_axis=ct_value_new[k, :, :]
        axis_gray_img = ct_value_new[k, :, :].astype(np.uint8)
        # axis_gray_img = ct_value[k, :, :].astype(np.uint8)
        # label
        # axis_gray_img = ct_value[k, :, :].astype(np.uint8)

        #标签图片需要*255
        # axis_gray_img=axis_gray_img *255

        #image-jpg,label-png
        cv2.imwrite(axis_save_path+filename[:-7] + '_'+str(k+1)+'.png', axis_gray_img )

        #nii
        # axis_gray_img = np.rot90(axis_gray_img, k=3)
        # img = nib.Nifti1Image(axis_gray_img, np.eye(4))
        # nib.save(img, 'E:\\bigorgs\\medical_data\\Conary\\Hospital\\dongbei\\2D\\images\\axis\\' + '1_' + str(k + 1) + ".nii")  # 保存 nii 文件
        # nib.save(img, axis_save_path+filename[:-7] + '_'+str(k+1)+'.nii')  # 保存 nii 文件

    print("---------水平面转化完成------")

    #冠状面
    for k in range(ct_value.shape[1]):
        # image
        # cor_gray_img = ct_value[:, k, :].astype(np.uint8)
        cor_gray_img = ct_value_new[:, k, :].astype(np.uint8)
        # label
        # cor_gray_img = ct_value[:, k, :].astype(np.uint8)

        # png
        # sag_gray_img = np.fliplr(sag_gray_img)  # 左右翻转
        cor_gray_img=np.flipud(cor_gray_img)                 #上下翻转
        # cor_gray_img=cor_gray_img * 255

        cv2.imwrite(cor_save_path+filename[:-7] + '_'+str(k+1)+'.png', cor_gray_img )

        #nii
        # cor_gray_img = np.rot90(cor_gray_img, k=3)
        # cor_gray_img = np.fliplr(cor_gray_img) # 左右翻转
        # img = nib.Nifti1Image(cor_gray_img, np.eye(4))
        # nib.save(img,'E:\\bigorgs\\medical_data\\Conary\\Hospital\\dongbei\\2D\\images\\cornal\\' + '1_' + str(k + 1) + ".nii")
        # nib.save(img,cor_save_path+filename[:-7] + '_'+str(k+1)+'.nii')

    print("---------冠状面转化完成------")

    #矢状面
    for k in range(ct_value.shape[2]):
        #image
        # sag_gray_img = ct_value[:, :, k].astype(np.uint8)
        sag_gray_img = ct_value_new[:, :, k].astype(np.uint8)
        #label
        # sag_gray_img = ct_value[:, :, k].astype(np.uint8)

        #png
        sag_gray_img=np.flipud(sag_gray_img)           #上下翻转
        # sag_gray_img=sag_gray_img * 255

        cv2.imwrite(sag_save_path+filename[:-7] + '_'+str(k+1)+'.png', sag_gray_img )

        #nii
        # sag_gray_img = np.flipud(sag_gray_img)
        # sag_gray_img = np.rot90(sag_gray_img, k=3)
        # img = nib.Nifti1Image(sag_gray_img, np.eye(4))
        # nib.save(img, 'E:\\bigorgs\\medical_data\\Conary\\Hospital\\dongbei\\2D\\images\\sagittal\\' + '1_' + str(k + 1) + ".nii")
        # nib.save(img, sag_save_path+filename[:-7] + '_'+str(k+1)+'.nii')

    print("---------矢状面转化完成------")

print("---------全部转化完成------")




