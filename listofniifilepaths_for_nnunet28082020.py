#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 15:35:36 2020

@author: michaely
"""

import os
join = os.path.join
import random
import shutil
import json



"""
USE THIS WHEN YOU DO NOT HAVE THE FILES IN THE RESPECTIVE FOLDERS,

AND YOU NEED ALSO THEIR PATHS TO MAKE THE dataset.json FILE
"""

# base = "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/task11_Kits19Data"

base = "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/Task11_Kits19"

# base = "/Volumes/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/task11_Kits19"
task_id = 11
task_name = "Kits19"
foldername = "Task%03.0d_%s" % (task_id, task_name)

out_base = join("/Volumes/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data", foldername)
imagestr = join(out_base, "imagesTr")
imagests = join(out_base, "imagesTs")
labelstr = join(out_base, "labelsTr")
os.makedirs(imagestr)
os.makedirs(imagests)
os.makedirs(labelstr)



# data_case_path = "/media/michaely/Youpele_HD/Uniklinik/kits19/Task11_Kits19Data"
# data_case_path = "/Volumes/Youpele_HD/Uniklinik/kits19/Task11_Kits19Data"
data_case_path = "/Volumes/Youpele_HD/Uniklinik/kits19_04092020/data"
cases_ = os.listdir(data_case_path)


cases = []
cases_paths = []
# removing the cases without segmentation
for c in cases_:
    ca = c.split("_")
    if len(ca) ==2:
        num = int(ca[1])
        if num <= 209:
            cases.append(c)

# Randomize the list 
cases = random.sample(cases, len(cases))


# Creating the cases paths 
for case in cases:
    case_path = os.path.join(data_case_path, case)
    cases_paths.append(case_path)








train_patient_names = []
test_patient_names = []

# all_cases = subfolders(base, join=False)

train_patients = cases_paths[:194]
test_patients = cases_paths[194:205]

test = []
for curr in test_patients:
    pa = curr.split("/")
    p = pa[-1]
    image_file = join(curr, "resampled_image.nii.gz")
    shutil.copy(image_file, join(imagests, "resampled_image.nii.gz"))
    os.rename(join(imagests, "resampled_image.nii.gz"), join(imagests, p + "_resampled_image.nii.gz"))
    # test_patient_names.append(p)
    test.append(join(imagests, p + "_resampled_image.nii.gz"))

    

training = []
for curr in train_patients:
    case_dict = {}
    # print(curr)
    pa = curr.split("/")
    p = pa[-1]
    # print(curr)
    label_file= join(curr, 'resampled_segmentation.nii.gz')
    image_file = join(curr, "resampled_image.nii.gz")

    shutil.copy(image_file, join(imagestr, "resampled_image.nii.gz"))
    os.rename(join(imagestr, "resampled_image.nii.gz"), join(imagestr, p + "_resampled_image.nii.gz"))
    case_dict["image"] = join(imagestr, p + "_resampled_image.nii.gz")
    
    shutil.copy(label_file, join(labelstr, "resampled_segmentation.nii.gz"))
    os.rename(join(labelstr, "resampled_segmentation.nii.gz"), join(labelstr, p + "_resampled_segmentation.nii.gz"))
    case_dict["label"] = join(labelstr, p + "_resampled_segmentation.nii.gz")
    training.append(case_dict)
    
    # train_patient_names.append(p)



# Creating a dict and filling it up

json_dict = {}
json_dict['name'] = "KiTS"
json_dict['description'] = "kidney and kidney tumor segmentation"
json_dict['tensorImageSize'] = "4D"
json_dict['reference'] = "KiTS data for nnunet"
json_dict['licence'] = ""
json_dict['release'] = "0.0"
json_dict['modality'] = {
        "0": "CT",
    }
json_dict['labels'] = {
        "0": "background",
        "1": "Kidney",
        "2": "Tumor"
    }

json_dict['numTraining'] = len(train_patient_names)
json_dict['numTest'] = len(test_patient_names)
json_dict['training'] = training
json_dict['test'] = test



# saving the json

with open(join(out_base,"dataset.json"), "w") as outfile:  
    json.dump(json_dict, outfile) 







"""
USE THIS WHEN YOU ALREADY HAVE THE FILES IN THE RESPECTIVE FOLDERS,

AND THE ONLY THING YOU NEED IS THE JUST THEIR PATHS TO MAKE THE dataset.json FILE
"""

imagesTr_path = "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/Task13_Phlebolith_Stone/imagesTr"
imagesTr = os.listdir(imagesTr_path)

labelsTr_path = "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/Task13_Phlebolith_Stone/labelsTr"
labelsTr = os.listdir(labelsTr_path)

imagesTs_path = "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/Task13_Phlebolith_Stone/imagesTs"
imagesTs = os.listdir(imagesTs_path)



#training image path
training = []
for image in imagesTr:
    caseNum_of_image = image.split("_")[1]
    
    for label in labelsTr:
        caseNum_of_label = label.split("_")[1]
        
        if caseNum_of_image == caseNum_of_label:
            case_dict = {"image":join(imagesTr_path, image) ,
                         "label":join(labelsTr_path, label) }
            training.append(case_dict)
            
            
# test image paths 
test = []
for image in imagesTs:
    test.append(join(imagesTs_path, image))



# Creating a dict and filling it up

json_dict = {}
json_dict['name'] = "Phlebolith & Kidney Stone"
json_dict['description'] = "Phlebolith & Kidney Stone segmentation"
json_dict['tensorImageSize'] = "4D"
json_dict['reference'] = "Phlebolith & Kidney Stone data for nnunet"
json_dict['licence'] = ""
json_dict['release'] = "0.0"
json_dict['modality'] = {
        "0": "CT",
    }
json_dict['labels'] = {
        "0": "background",
        "1": "Stone",
        "2": "Phlebolith"
    }

json_dict['numTraining'] = len(training)
json_dict['numTest'] = len(test)
json_dict['training'] = training
json_dict['test'] = test



# saving the json
out_base = "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/Task13_Phlebolith_Stone"
with open(join(out_base,"dataset.json"), "w") as outfile:  
    json.dump(json_dict, outfile) 



# nnUNet_convert_decathlon_task -i /media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/Task11_Kits19





