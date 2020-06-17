# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 00:06:50 2020

@author: michaely
"""


import os
import sys
sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts")
from seg_resampling import segmentation_resampling
import SimpleITK as sitk



# Getting the image_path
dicom_rootdir = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM"
dicom_list= os.listdir(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM")

images_paths = {}



for po in dicom_list:
    if 'x' in po:
        x = dicom_rootdir +  '\\' + po
        x_dir = x
        x_list = os.listdir(x)

        for i in x_list:
            image_path = x_dir  +  '\\' + i + '\kidney.nii'
            images_paths[i+'_x'] = image_path
            
    else:
        image_path = dicom_rootdir +  '\\' + po + '\kidney.nii'
        images_paths[po] = image_path
        
        
        

# Function to resample all segmentation in a folder. 

def resample_all(path):
    alist =os.listdir(path)
    
    for key, image_path in images_paths.items():
        for keyz in alist:
            if key ==keyz:
                print("Resampling:", key, "...")
                out_seg_path = path + '\\' + keyz
                seg_path = out_seg_path + '\Segmentation.seg.nii'
                
                segmentation_resampling(seg_path = seg_path, image_path = image_path, 
                                         out_seg_path = out_seg_path)
                print("Resampling ",key, " successful.")
                
                
                
                
Phlebolithen = resample_all(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Phlebolithen")

Steine = resample_all(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine")
                
Steine_Phlebolithen = resample_all(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine+Phlebolithen")



                
                


