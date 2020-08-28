# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 11:00:40 2020

@author: michaely
"""

import os
import pandas as pd
import random
import json

data_case_path = r"C:\Users\michaely\Documents\hiwi\kits19\data"
cases_ = os.listdir(data_case_path)


cases = []
case_list = []
case_pred_list = []
image_list = []
segmentation_list = []

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



# Splitting the datasets into train, val and test
trainNum = 174
valNum = 20
testNum = 10
totalNum = train + val + test

trainset = case_list[0:trainNum:1]
valset = case_list[trainNum:trainNum+valNum:1]
testset = case_list[trainNum+valNum:totalNum:1]


# Putting the paths for images and labels into training and test folders
training = []
for cases_ in trainset:
    case_dict = {}
    case_temp =  os.listdir(cases_)
    
    for content in case_temp:
        if content == "new_image.nii":
            content_path = cases_ + '\\' + content
            content_path = content_path.replace('\\','/')
            case_dict["image"] = content_path
        elif content == 'new_segmentation.nii':
            content_path = cases_ + '\\' + content
            content_path = content_path.replace('\\','/')
            case_dict["label"] = content_path
    training.append(case_dict)
            
    
test = []    
for cases_ in testset:
    # case_dict = {}
    case_temp =  os.listdir(cases_)
    
    for content in case_temp:
        if content == "new_image.nii":
            content_path = cases_ + '\\' + content
            content_path = content_path.replace('\\','/')
            # case_dict["image"] = content_path
        
    test.append(content_path)
             
        
    
    




''''

Creating the json file required by nnunet
''''



dataset = {"name": "kits19",
           "description": "copy it from the kits",
           "reference": "MIT",
           "licence": "MIT",
           "relase": "some date",
           "tensorImageSize": "3D",
           "modality": {"0": "CT"},
           "labels":{"0": "background", 
                     "1": "Anterior/kidney", 
                     "2": "Posterior/tumor"},
           "numTraining": 260,
           "numTest": 130,
           "training": training,
           "test":test,
           }




with open(r"C:\Users\michaely\Documents\hiwi\kits19\data\dataset.json", "w") as outfile:  
    json.dump(dataset, outfile) 



readjson = pd.read_json(r"C:\Users\michaely\Documents\hiwi\kits19\data\dataset.json", orient='index' )








