from glob import glob

import numpy as np
import nrrd
import os
import cv2

nrrd_filename='nrrd\\images'
save_path='nrrd_output\\images'
patient_id='1'
files = glob(nrrd_filename+'/*.nrrd')
for file in files:
    nrrd_data, nrrd_options = nrrd.read(file)
    h, w, slides_num = nrrd_data.shape
    filename = os.path.basename(file)
    for i in range(slides_num):
        img = nrrd_data[:, :, slides_num - i - 1] * 255
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cv2.imwrite(save_path + '/' + filename[-7:-5] + '_' + str(i + 1) + '.png', img)

print("nrrd转png完成!")

