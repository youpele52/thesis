# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:52:34 2020

@author: michaely
"""

import os
#import pandas as pd
import random
import sys
sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts")

data_case_path = r"C:\Users\michaely\Documents\hiwi\kits19\mean0std1"
cases_ = os.listdir(data_case_path)


cases = []
case_list = []
case_pred_list = []
image_list = []
segmentation_list = []
roiMask_list = []




# removing the cases without segmentation
for c in cases_:
    ca = c.split("_")
    if len(ca) ==2:
        num = int(ca[1])
        if num <= 209:
            cases.append(c)

# Randomize the list 
cases = random.sample(cases, len(cases))


# Adding data to case list and removing the case 37
for case in cases:
    if case[0] == 'c' and 'case_00037' not in case:
        case =  data_case_path + '\\' + case
        case_list.append(case)



        
# Get pred_case        
for case in cases:
    if case[0] == 'c' and 'case_00037' not in case:
        case = 'pred_' + case + '.nii'
        case_pred_list.append(case)
        
    
    
        
# Getting the new image and new segmentation file paths
for cases_ in case_list:
    case_temp =  os.listdir(cases_)

    for content in case_temp:

        if 'new_image' in content:
            content_path = cases_ + '\\' + content
            content_path = content_path.replace('\\','/')
            image_list.append(content_path)
            
        elif 'new_segmentation.nii' in content:
            content_path = cases_ + '\\' + content
            content_path = content_path.replace('\\','/')
            segmentation_list.append(content_path)
            
        elif 'mask.nii' in content:
            content_path = cases_ + '\\' + content
            content_path = content_path.replace('\\','/')
            roiMask_list.append(content_path)
            
            
            
            

# Splitting the datasets into train, val and test
train = 174
val = 20
test = 10
total = train + val + test

train_set = {'image' : image_list[0:train:1],
            'segmentation': segmentation_list[0:train:1],
            "roi_Mask":roiMask_list[0:train:1]}  


val_set = {'image' : image_list[train:train+val:1],
            'segmentation': segmentation_list[train:train+val:1],
            "roi_Mask": roiMask_list[train:train+val:1]} 


test_set = {'image' : image_list[train+val:total:1],
            'segmentation': segmentation_list[train+val:total:1],
            "roi_Mask": roiMask_list[train+val:total:1]} 

            
            
# Prediction val and test list
val_pred_set = case_pred_list[train:train+val:1]
test_pred_set = case_pred_list[train+val:total:1]



'''
TO CREATE CFGS FILES GO TO CREATE CFGs 
1. RUN ALL THE LINES IN THIS SCRIPT 
2. GO TO CreateCFGs AND RUN THE SCRIPT

'''





