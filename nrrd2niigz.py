import os
from glob import glob
import nrrd #pip install pynrrd, if pynrrd is not already installed
import nibabel as nib #pip install nibabeModuleNotFoundError: No module named 'nrrd'l, if nibabel is not already installed
import numpy as np

baseDir = os.path.normpath('./source/nrrd')
outputDir = os.path.normpath('./output')
files = glob(baseDir+'/*.nrrd')

for file in files:
#load nrrd
  _nrrd = nrrd.read(file)
  data = _nrrd[0]
  header = _nrrd[1]

#save nifti
  img = nib.Nifti1Image(data, np.eye(4))
  filename=os.path.basename(file)
  nib.save(img,os.path.join(outputDir, filename[-8:-5] + '.nii.gz'))
  # nib.save(img,os.path.join(outputDir,  '.nii.gz'))

print("finish!")
