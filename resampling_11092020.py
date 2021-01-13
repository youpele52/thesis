# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 13:46:46 2020

@author: michaely
"""

import pandas as pd
from skimage.measure import label
from skimage.measure import regionprops
import SimpleITK as sitk
import os
import sys
# from datetime import datetime
sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts\stones_phlebolith")
from resample_spacing_for_stone_and_phlebolith import resample
from get_info import get_info



#Seperates a 4D image into the two 3D images which makes it up

# Phlebolithen
dataset_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Phlebolithen"

# Steine
dataset_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine"

# Steine+Phlebolithen
dataset_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine+Phlebolithen"




dataset_list = os.listdir(dataset_path)
for case in dataset_list:
    case_path = os.path.join(dataset_path, case)
    case_list = os.listdir(case_path)
    
    for content in case_list:
        if "Segmentation.seg.nii.gz" in content:
            seg_path = os.path.join(case_path, content)
            image_path = seg_path
            out_image_path = case_path
            
            # separating the two images
            image3D_label1_path = os.path.join(case_path, "image3D_label1.nii.gz") 
            image3D_label2_path = os.path.join(case_path, "image3D_label2.nii.gz")
            
            reader = sitk.ImageFileReader()
            reader.SetFileName(image_path)
            image = reader.Execute();
            data = sitk.GetArrayFromImage(image)
            data.shape
            data3D_label1=data[:,:,:,0]
            data3D_label2=data[:,:,:,1]
            
            image3D_label1 = sitk.GetImageFromArray(data3D_label1)
            image3D_label1.SetSpacing(image.GetSpacing())
            image3D_label1.SetOrigin(image.GetOrigin())
            writer = sitk.ImageFileWriter()
            writer.SetFileName(image3D_label1_path)
            writer.Execute(image3D_label1)
            
            image3D_label2 = sitk.GetImageFromArray(data3D_label2)
            image3D_label2.SetSpacing(image.GetSpacing())
            image3D_label2.SetOrigin(image.GetOrigin())
            writer = sitk.ImageFileWriter()
            writer.SetFileName(image3D_label2_path)
            writer.Execute(image3D_label2)
            
            # resampling the separated images individually
            resample(image_path = image3D_label1_path ,
                     out_image_path = out_image_path,
                     segmentation_or_image = "segmentation_01", is_label=True)
            
            resample(image_path = image3D_label2_path , 
                     out_image_path = out_image_path, 
                     segmentation_or_image = "segmentation_02", is_label=True)
            
            # combining the two resampled images
            resampled_segmentation_01_path = os.path.join(case_path, "resampled_segmentation_01.nii")
            reader = sitk.ImageFileReader()
            reader.SetFileName(resampled_segmentation_01_path)
            image1 = reader.Execute();

            resampled_segmentation_02_path = os.path.join(case_path, "resampled_segmentation_02.nii")
            reader = sitk.ImageFileReader()
            reader.SetFileName(resampled_segmentation_02_path)
            image2 = reader.Execute();
            
            # writing the combined image
            combine_image = 1 * image1 + 2 * image2
            combine_image_path = os.path.join(case_path, "combine_image.nii")
            writer = sitk.ImageFileWriter()
            writer.SetFileName(combine_image_path)
            writer.Execute(combine_image)


            
            

            
             
            
            
seg_path_for_check = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Phlebolithen\P046\combine_image.nii"
get_info(seg_path_for_check)

            
            


            
            
get_info(r"\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P106\resampled_image.nii")
            

