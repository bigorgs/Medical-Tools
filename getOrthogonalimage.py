'''
三维转二维切片，保存为nii格式
'''

import pydicom
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import os
import cv2
import nibabel as nib

#获取根目录文件
def get_root_file(root_file):
    list_file = os.listdir(root_file)
    list_file.sort(key=lambda x: str(x.split('.')[0]))
    return list_file

# root_dicom="E:\\bigorgs\\Datasets\\1\\"
root_dicom="E:\\bigorgs\\medical_data\\Conary\\test\\dicom\\"
list_dicom = get_root_file(root_dicom)
num_dicom = len(list_dicom)
files = []
for i in range(num_dicom):
    file_root = root_dicom + list_dicom[i]
    dcm = pydicom.dcmread(file_root,force=True)
    dcm.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    # print(dcm)
    # print("loading: {}".format(file_root))
    # files.append(pydicom.dcmread(file_root,force=True))
    files.append(dcm)



# load the DICOM files
# files = []
# print('glob: {}'.format(sys.argv[1]))
# for fname in glob.glob(sys.argv[1], recursive=False):
#     print("loading: {}".format(fname))
#     files.append(pydicom.dcmread(fname))

# print("file count: {}".format(len(files)))

# skip files with no SliceLocation (eg scout views)
slices = []
skipcount = 0


for f in files:
    slices.append(f)
    # if hasattr(f, 'SliceLocation'):          #切片位置
    #     slices.append(f)
    # else:
    #     skipcount = skipcount + 1

# print("skipped, no SliceLocation: {}".format(skipcount))

# ensure they are in the correct order
# slices = sorted(slices, key=lambda s: s.SliceLocation)

# pixel aspects, assuming all slices are the same
# ps = slices[0].PixelSpacing                 #像素间距
# ss = slices[0].SliceThickness              #切片厚度
# ax_aspect = ps[1]/ps[0]
# sag_aspect = ps[1]/ss
# cor_aspect = ss/ps[0]
# print(slices[0].pixel_array.shape)
# create 3D array
img_shape = list(slices[0].pixel_array.shape)
img_shape.append(len(slices))
img3d = np.zeros(img_shape)

# fill 3D array with the images from the files
for i, s in enumerate(slices):
    img2d = s.pixel_array
    img3d[:, :, i] = img2d

    #横轴面
    ax=img3d[:, :, img_shape[2]//2]              #3
    ax = np.rot90(ax,k=3)
    # ax = ax.astype(np.uint8)
    # print(ax.dtype)
    # cv2.imwrite("E:\\bigorgs\\medical_data\\Conary\\mhdtoimage\\axis\\10.png",ax)
    img=nib.Nifti1Image(ax,np.eye(4))
    nib.save(img,"E:\\bigorgs\\medical_data\\Conary\\mhdtoimage\\axis\\"+"axis"+str(i)+".nii") # 保存 nii 文件

    #冠状面
    cor=img3d[img_shape[0]//2, :, :]              #1
    # cor = np.rot90(cor,k=3)
    img=nib.Nifti1Image(cor,np.eye(4))
    nib.save(img,"E:\\bigorgs\\medical_data\\Conary\\mhdtoimage\\cornal\\"+"cor"+str(i)+".nii")

    #矢状面
    sag=img3d[:, img_shape[1]//2, :]                #2
    # sag = np.rot90(sag,k=3)
    img=nib.Nifti1Image(sag,np.eye(4))
    nib.save(img,"E:\\bigorgs\\medical_data\\Conary\\mhdtoimage\\sagittal\\"+"sag"+str(i)+".nii")
