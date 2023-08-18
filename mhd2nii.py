import os
from glob import glob

import SimpleITK as sitk

baseDir = os.path.normpath('E:\\bigorgs\\Conary\\Challenge\\orcascore\\Raw_OrCaScore\\train\\labels')
outputDir = os.path.normpath('E:\\bigorgs\\cardiovascular\\workspace\\Calcification\\dataset\\CT\\labels')
files = glob(baseDir+'/*.mhd')

# img = sitk.ReadImage("1.mhd")
# sitk.WriteImage(img, "mhd2nii_output\\1.nii")

for file in files:
    print(file)
    #load mhd
    img = sitk.ReadImage(file)
    #save nii
    filename=os.path.basename(file)

    sitk.WriteImage(img, os.path.join(outputDir, filename[:-4] + '.nii.gz'))

print("finish!")


