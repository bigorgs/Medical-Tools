import os
import nibabel as nib
import numpy as np
from tqdm import tqdm
import cv2

def listdir(path):
    dirs = os.listdir(path)
    dirs.sort()  # 扫描和标签的文件名不完全相同，对两个目录下的所有文件进行排序可以保证二者能匹配上
    return dirs

scan_dir = "nii.gz\\images" # CT扫描数据路径
label_dir = "nii.gz\\labels" # 病灶分割标签所在路径
output_dir = "niigz_output"
scan_output = os.path.join(output_dir, "images") # CT图片输出路径
label_output = os.path.join(output_dir, "labels") # 标签图片输出路径

if not os.path.exists(scan_output):
    os.makedirs(scan_output)
if not os.path.exists(label_output):
    os.makedirs(label_output)

wl, wh = (90, 750) # 对CT进行窗口化的强度范围

scan_fnames = listdir(scan_dir)
label_fnames = listdir(label_dir)

for case_ind in tqdm( range(len(scan_fnames)) ):
    scan_fname = scan_fnames[case_ind]
    label_fname = label_fnames[case_ind]

    scanf = nib.load(os.path.join(scan_dir, scan_fname)) # 使用nibabel库读入数据
    scan = scanf.get_fdata()
    # (x, y, z) = scan.shape
    labelf = nib.load(os.path.join(label_dir, label_fname))
    label = labelf.get_fdata()

    scan = np.rot90(scan,k=3) # 对读入数据的方向进行矫正，逆时针旋转90度
    label = np.rot90(label,k=3)


    # 窗口化操作，将范围转换到 0~255，便于存入图片
    scan = scan.clip(wl, wh).astype(np.uint8)
    scan = ( (scan - wl)/(wh - wl) * 256)

    for sli_ind in range(label.shape[2]):
        scan_slice_path = os.path.join(scan_output, "{}_{}.png".format(scan_fname.rstrip(".nii.gz"), sli_ind ) )
        label_slice_path = os.path.join(label_output, "{}_{}.png".format(scan_fname.rstrip(".nii.gz"), sli_ind ) )
        cv2.imwrite(scan_slice_path, scan[:,:,sli_ind])
        cv2.imwrite(label_slice_path, label[:,:,sli_ind])

print("niigztopng图片转换完成!!!!")