import numpy as np
import nibabel as nib
from ipywidgets import interact, interactive, IntSlider, ToggleButtons

import matplotlib.pyplot as plt
# %matplotlib inline
import matplotlib # 注意这个也要import一次

import seaborn as sns
sns.set_style('darkgrid')

image_path = "./source/nifti/images/25.nii.gz"

#读取图像
image_obj = nib.load(image_path)
# print(f'Type of the image {type(image_obj)}')

#提取 numpy 数组
image_data = image_obj.get_fdata()
# type(image_data)

#查看图像大小
height, width, depth = image_data.shape
# print(f"The image object height: {height}, width:{width}, depth:{depth}")

#查看图像值范围
# print(f'image value range: [{image_data.min()}, {image_data.max()}]')

#查看图像成像信息
print(image_obj.header.keys())
print(image_obj.header['slice_end'])

#图像分辨率
# pixdim =  image_obj.header['pixdim']
# print(f'z轴分辨率： {pixdim[3]}')
# print(f'in plane 分辨率： {pixdim[1]} * {pixdim[2]}')

#实际扫描范围：pixdim * shape
# z_range = pixdim[3] * depth
# x_range = pixdim[1] * height
# y_range = pixdim[2] * width
# print(x_range, y_range, z_range)

#可视化图像

#随机显示某一层
# i = np.random.randint(0, depth)
# # Define a channel to look at
# print(f"Plotting z Layer {i} of Image")
# plt.imshow(image_data[:, :, i], cmap='gray')
# plt.axis('off');

#交互显示
# def explore_3dimage(layer):
#     plt.figure(figsize=(10, 5))
#     plt.imshow(image_data[:, :, layer], cmap='gray');
#     plt.title('Explore Layers of adrenal', fontsize=20)
#     plt.axis('off')
#     return layer
#
# interact(explore_3dimage, layer=(0, image_data.shape[-1]));


