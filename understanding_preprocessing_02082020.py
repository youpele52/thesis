# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 00:53:13 2020

@author: michaely
"""


import os
import numpy as np
import nibabel as nib
from shutil import copyfile
import matplotlib.pyplot as plt
from scipy import stats


# kidney = r"C:\Users\michaely\Documents\hiwi\kits19\data\case_00000\new_image.nii"
# seg = r"C:\Users\michaely\Documents\hiwi\kits19\data\case_00000\new_segmentation.nii"


root_path = r"C:\Users\michaely\Documents\hiwi\kits19\data"
root_output_path=r"C:\Users\michaely\Documents\hiwi\kits19\mean0std1"


if not os.path.exists(root_output_path):
    os.mkdir(root_output_path)
    
caselist=os.listdir(root_path)


for case in caselist:
    print(case)
    root_path_case=os.path.join(root_path,case)
    if os.path.isdir(root_path_case):
        serieslist=os.listdir(root_path_case)
        
        for series in serieslist:
            print(series)
            example_filename = os.path.join(root_path_case, series)
            if 'new_seg' in series:
                img = nib.load(example_filename)
                seriesstam=series.split('.')
                print(os.path.join(root_output_path_case,seriesstam[0])+'.nii')
                nib.save(img, os.path.join(root_output_path_case,seriesstam[0])+'.nii')       
            elif 'new_image' in series:
                img = nib.load(example_filename)
                I=img.get_fdata()
                #Define brain mask
                brain_mask=(I>-900) # I also tried -900
                plt.imshow(brain_mask[:,:,100])
                plt.show()
                plt.imshow(I[:,:,100])
                plt.show()
                #stats.tmean(I)
                #stats.tstd(I)
                
                # tmeanI=0
                # tstdI=1
                tmeanI=stats.tmean(I, (0.01,np.max(I)))
                tstdI=stats.tstd(I, (0.01,np.max(I)))   
                
                img_new=(I-tmeanI)/tstdI
                # img_new=(I-101)/76.9
                
                new_img = nib.Nifti1Image(img_new, img.affine, img.header)
                root_output_path_case=os.path.join(root_output_path,case)
                if not os.path.exists(root_output_path_case):
                    os.mkdir(os.path.join(root_output_path_case))
                seriesstam=series.split('.')
                print(os.path.join(root_output_path_case,seriesstam[0])+'_mean0std1ROI.nii')
                nib.save(new_img, os.path.join(root_output_path_case,seriesstam[0])+'_mean0std1ROI.nii')
            
        img_brain_mask = nib.Nifti1Image(brain_mask, img.affine, img.header)
        print(os.path.join(root_output_path_case,'kidney_mask')+'.nii')
        nib.save(img_brain_mask, os.path.join(root_output_path_case,'kidney_mask')+'.nii') # saved in nii instead of .gz   
    


