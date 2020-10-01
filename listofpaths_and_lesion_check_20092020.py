# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 01:00:46 2020

@author: michaely
"""


import random
import pandas as pd
import os
import sys
from datetime import datetime
sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts\stones_phlebolith")
from seg_full_info import SegInfo
from CreateCFGs import Create_CFGs




main_image_folder_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM"
image_list = os.listdir(main_image_folder_path)

image_dict = {}
for patient in image_list:
    if patient[0] == "P":
        patient_path = os.path.join(main_image_folder_path, patient)
        patient_list = os.listdir(patient_path)
        for content in patient_list:
            if "resampled" in content:
                image_path = os.path.join(patient_path, content)
                image_dict[patient] = image_path
                
                
                
                

Phlebolithen_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Phlebolithen"
Phlebolithen_list = os.listdir(Phlebolithen_path)
segmentation_dict = {}
for patient in Phlebolithen_list:
    patient_path = os.path.join(Phlebolithen_path, patient)
    patient_list = os.listdir(patient_path)
    for content in patient_list:
        if "new_segmentation.nii" in content:
            segmentation_path = os.path.join(patient_path, content)
            segmentation_dict[patient] = segmentation_path
            

Steine_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine"
Steine_list = os.listdir(Steine_path)
# Steine_dict = {}
for patient in Steine_list:
    patient_path = os.path.join(Steine_path, patient)
    patient_list = os.listdir(patient_path)
    for content in patient_list:
        if "new_segmentation.nii" in content:
            segmentation_path = os.path.join(patient_path, content)
            segmentation_dict[patient] = segmentation_path
            

Steine_Phlebolithen_path=r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine+Phlebolithen"
Steine_Phlebolithen_list = os.listdir(Steine_Phlebolithen_path)
# Steine_Phlebolithen_dict = {}
for patient in Steine_Phlebolithen_list:
    patient_path = os.path.join(Steine_Phlebolithen_path, patient)
    patient_list = os.listdir(patient_path)
    for content in patient_list:
        if "new_segmentation.nii" in content:
            segmentation_path = os.path.join(patient_path, content)
            segmentation_dict[patient] = segmentation_path
            
            

# Shuffle 

l = list(segmentation_dict.items())
random.shuffle(l)
segmentation_dict = dict(l)


"""
Dividing them into image and segmentation
"""

image_segmentation_dict = {}
image_list2 = []
phlebstone_list = []


for segID in segmentation_dict:
    for imageID in image_dict:
        if segID == imageID:
            image_list2.append(image_dict[segID])
            phlebstone_list.append(segmentation_dict[segID])
            image_segmentation_dict["image"] =  image_list2
            image_segmentation_dict["segmentation"] = phlebstone_list



"""
Splitting the datasets into train, val and test
"""
 

train = 78
val = 15
test = 10
total = train + val + test


train_set = {'image' : image_segmentation_dict["image"][0:train:1],
            'segmentation': image_segmentation_dict["segmentation"][0:train:1],}  

val_set = {'image' : image_segmentation_dict["image"][train:train+val:1],
            'segmentation': image_segmentation_dict["segmentation"][train:train+val:1],} 

test_set = {'image' : image_segmentation_dict["image"][train+val:total:1],
            'segmentation': image_segmentation_dict["segmentation"][train+val:total:1],} 



# Check for lesion

lesionBox = []
for seg in train_set["segmentation"]:
    lesionBox.append(SegInfo.image_seg_full_info(seg))
    
    
# merge    
image_info_df_merged =  pd.concat(lesionBox)
image_info_df_merged.index = range(0,len(image_info_df_merged),1) 

# column = image_info_df_merged.iloc[0:1,3:4]
# print(column)

stone = []
phlebolith = []
for num in range(0,len(image_info_df_merged),1):
    if num<=344:
        column = image_info_df_merged.iloc[num:num+1,3:4].to_numpy()
        content = column[0][0]
        if "Stone" in content:
            stone.append(content)
        elif "Phlebolite" in content:
            phlebolith.append(content)
                     
print("Total number of Stone is:", str(len(stone)) + "\n" + "Total number of Phlebolite is:", str(len(phlebolith)))
            
        
"""
NOW LET US GET THE REAL SEGMENTATION FILE IE COMBINE RESAMPLE
"""

image_segmentation_dict["segmentation"]

     

Phlebolithen_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Phlebolithen"
Phlebolithen_list = os.listdir(Phlebolithen_path)
segmentation_dict = {}
for patient in Phlebolithen_list:
    patient_path = os.path.join(Phlebolithen_path, patient)
    patient_list = os.listdir(patient_path)
    for content in patient_list:
        if "resampledsize_combine_image.nii" in content:
            segmentation_path = os.path.join(patient_path, content)
            segmentation_dict[patient] = segmentation_path
            
Steine_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine"
Steine_list = os.listdir(Steine_path)
# Steine_dict = {}
for patient in Steine_list:
    patient_path = os.path.join(Steine_path, patient)
    patient_list = os.listdir(patient_path)
    for content in patient_list:
        if "resampledsize_combine_image.nii" in content:
            segmentation_path = os.path.join(patient_path, content)
            segmentation_dict[patient] = segmentation_path
            
Steine_Phlebolithen_path=r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine+Phlebolithen"
Steine_Phlebolithen_list = os.listdir(Steine_Phlebolithen_path)
for patient in Steine_Phlebolithen_list:
    patient_path = os.path.join(Steine_Phlebolithen_path, patient)
    patient_list = os.listdir(patient_path)
    for content in patient_list:
        if "resampledsize_combine_image.nii" in content:
            segmentation_path = os.path.join(patient_path, content)
            segmentation_dict[patient] = segmentation_path
            

resampled_combine_seg = []
for segID2 in image_segmentation_dict["segmentation"]:
#    print(segID2.split("\\")[-2])
    for segID1 in segmentation_dict:
        if segID2.split("\\")[-2] == segID1:
            resampled_combine_seg.append(segmentation_dict[segID1])
            
            
"""
Splitting again with the image and new segmentation
"""


train = 78
val = 15
test = 10
total = train + val + test


train_set = {'image' : image_segmentation_dict["image"][0:train:1],
            'segmentation': resampled_combine_seg[0:train:1],}  

val_set = {'image' : image_segmentation_dict["image"][train:train+val:1],
            'segmentation':resampled_combine_seg[train:train+val:1],} 

test_set = {'image' : image_segmentation_dict["image"][train+val:total:1],
            'segmentation':resampled_combine_seg[train+val:total:1],} 


# Get pred_case       
val_pred_set = []
val_pred = image_segmentation_dict["image"][train:train+val:1]
for i in val_pred:
    val_pred_set.append('pred_' + i.split("\\")[9] + '.nii')
 
test_pred_set = []
test_pred =  image_segmentation_dict["image"][train+val:total:1]
for i in test_pred:
    test_pred_set.append('pred_' + i.split("\\")[9] + '.nii')


"""
Creating CFGs
"""
Create_CFGs.create_cfgs_no_roi( train_set, val_set, val_pred_set, test_set, test_pred_set,project_name = "Stone_Phleb")

