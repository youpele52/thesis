# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 15:34:59 2020

@author: michaely
"""

import os
import sys
sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts\stones_phlebolith")
from last_step_of_resampling_steine_phlebolith import last_step_resampling



imagedir_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM"
imagedir_list = os.listdir(imagedir_path)

# Phlebolithen_dir_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Phlebolithen"
# Phlebolithen_dir_list = os.listdir(Phlebolithen_dir_path)
# Steine_dir_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine"
# Steine_dir_list = os.listdir(Steine_dir_path)
# Steine_Phlebolith_dir_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine+Phlebolithen"
# Steine_Phlebolith_dir_list = os.listdir(Steine_Phlebolith_dir_path)






# Phlebolithen
dataset_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Phlebolithen"

# Steine
dataset_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine"

# Steine+Phlebolithen
dataset_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine+Phlebolithen"




dataset_list = os.listdir(dataset_path)
for case in imagedir_list:
    for case2 in dataset_list:
        if case ==case2:
            print("Processing case: ", case)
            case_image_path = os.path.join(imagedir_path, case)
            case_image_list = os.listdir(case_image_path)
            
            case_seg_path = os.path.join(dataset_path, case)
            out_image_path = case_seg_path
            case_seg_list = os.listdir(case_seg_path)
            
            # print(case_image_path,"\n",case_seg_path, "\n\n")
            
            for content in case_image_list:
                if "resampled_image" in content:
                    image_path = os.path.join(case_image_path, content)
                    reference_image = image_path
                    for content2 in case_seg_list:
                        if "combine_image.nii" in content2:
                            seg_path = os.path.join(case_seg_path, content2)
                            input_image = seg_path
                            
                            last_step_resampling(out_image_path = out_image_path , 
                                                 input_image = input_image, 
                                                 reference_image = reference_image)
                        
                        
                            # print(out_image_path, "\n", input_image, "\n", reference_image, "\n\n\n")
                    
                        
