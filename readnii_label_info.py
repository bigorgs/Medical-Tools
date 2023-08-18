import numpy as np
import nibabel as nib
from ipywidgets import interact, interactive, IntSlider, ToggleButtons


#查看标签
label_path = "./source/nifti/labels/25.nii.gz"
label_obj = nib.load(label_path)
label_array = label_obj.get_fdata()

#查看 label 里面有几种值 使用 np.unique()
print(f'With the unique values: {np.unique(label_array)}')

#更进一步，查看每个标签对应多少像素
print(np.unique(label_array, return_counts=True))