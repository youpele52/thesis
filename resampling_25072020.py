# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 21:10:00 2020

@author: michaely
"""
import os
import sys
sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts")
from resample_spacing import resample
from get_info import get_info



# Resampling images

dicom_rootdir = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM"
dicom_list= os.listdir(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM")


# images_info_dict = {}

for po in dicom_list:
    if "P" in po:
        image_dir = os.path.join(dicom_rootdir, po)
        image_path = dicom_rootdir +  '\\' + po + '\kidney.nii'
        print("Processing", po)
        print(image_path)
        
        resample(image_path = image_path, out_image_path=image_dir, segmentation_or_image = "image", is_label=False)
        
    elif "x" in po:
        x_dir = os.path.join(dicom_rootdir, po)
        x_list = os.listdir(x_dir)
        for i in x_list:
            image_dir = os.path.join(x_dir, i)
            image_path = x_dir  +  '\\' + i + '\kidney.nii'
            print("Processing", i)
            print(image_path)  
            
            resample(image_path = image_path, out_image_path=image_dir, segmentation_or_image = "image", is_label=False)
        
        
        
# Resampling segmentation


niere_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere"  
niere_list = os.listdir(niere_path)      
    

for file in niere_list:
    folder_path = os.path.join(niere_path, file)
    if os.path.isdir(folder_path):
        cases_dir = os.listdir(folder_path)
        for patient in cases_dir:
            patient_path = os.path.join(folder_path, patient)
            patient_dir = os.listdir(patient_path)
            for file in patient_dir:
                if "new_seg" in file:
                    segmentation_path = os.path.join(patient_path, file)
                    
                    print("Processing:\n", segmentation_path)
                    resample(image_path=segmentation_path, out_image_path=patient_path, segmentation_or_image="segmentation", is_label=True)
                    print("\nResampled segmentation saved in:", patient_path,"\n")
                    
                    
                    
                    

get_info(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Phlebolithen\P096\new_segmentation.nii")

get_info(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Phlebolithen\P096\resampled_segmentation.nii")
                    
