# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 18:58:45 2020

@author: Youpele
"""


import random
import pandas as pd
import os
import sys
import csv
from datetime import datetime
sys.path.append("D:/Uniklinik/Scripts")
# sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts\stones_phlebolith")
from seg_full_info import SegInfo
import shutil
# from CreateCFGs import Create_CFGs
join = os.path.join

"""
Getting the paths
"""


# Getting the paths for the images
images_dir = r"D:\Uniklinik\Phlebolith_Stone_Data\Images"
image_dict = {}

for content1 in os.listdir(images_dir):
    if content1[0] == "P":
        patientID = content1.split("_")[1]
        image_path = join(images_dir, content1)
        image_dict[patientID] = image_path
        
        
# Getting the paths for the segmentations
segmentation_dict = {}
Phlebolithen_path = r"D:\Uniklinik\Phlebolith_Stone_Data\Segmentations\Phlebolith"
for gt_file in os.listdir(Phlebolithen_path):
    if gt_file[0] == "P":
        patientID1 = gt_file.split("_")[1]
        segmentation_path = join(Phlebolithen_path, gt_file)
        segmentation_dict[patientID1] = segmentation_path



Stone_path = r"D:\Uniklinik\Phlebolith_Stone_Data\Segmentations\Stone"
# segmentation_dict = {}
for gt_file in os.listdir(Stone_path):
    if gt_file[0] == "P":
        patientID1 = gt_file.split("_")[1]
        segmentation_path = join(Stone_path, gt_file)
        segmentation_dict[patientID1] = segmentation_path
        


Stone_Phlebolith_path = r"D:\Uniklinik\Phlebolith_Stone_Data\Segmentations\Stone-Phlebolith"
# segmentation_dict = {}
for gt_file in os.listdir(Stone_Phlebolith_path):
    if gt_file[0] == "P":
        patientID1 = gt_file.split("_")[1]
        segmentation_path = join(Stone_Phlebolith_path, gt_file)
        segmentation_dict[patientID1] = segmentation_path
                

"""
Shuffling 
"""      

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
Splitting the datasets into train , test
"""
 

train = 94
val = 0
test = 10
total = train + val + test



train_set = {'image' : image_segmentation_dict["image"][0:train:1],
            'segmentation': image_segmentation_dict["segmentation"][0:train:1],}  

val_set = {'image' : image_segmentation_dict["image"][train:train+val:1],
            'segmentation': image_segmentation_dict["segmentation"][train:train+val:1],} 

test_set = {'image' : image_segmentation_dict["image"][train+val:total:1],
            'segmentation': image_segmentation_dict["segmentation"][train+val:total:1],} 






"""
Copying from remote desktop files, extracting the patientIDs
"""
# import csv

# for test
Stone_PhlebTest_images = open(r"C:\Users\Youpele\Desktop\Stone_PhlebTestChannels_flair_20092020Edition.cfg", "r")
yourResult = [line.split('\n') for line in Stone_PhlebTest_images.readlines()]

imageTs = []
for path in yourResult:
    imageTs.append(path[0])

imageTs_dict = {}
for content3 in imageTs:
    patientID3 = content3.split("\\")[-2][1:]
    imageTs_dict[patientID3] = content3
    
# for train
Stone_PhlebTrain_images = open(r"C:\Users\Youpele\Desktop\Stone_PhlebTrainChannels_flair_20092020Edition.cfg", "r")
yourResultTrain = [line.split('\n') for line in Stone_PhlebTrain_images.readlines()]

Stone_PhlebVal_images = open(r"C:\Users\Youpele\Desktop\Stone_PhlebValidationChannels_flair_20092020Edition.cfg", "r")
yourResultVal = [line.split('\n') for line in Stone_PhlebVal_images.readlines()]


imageTr = []
for path in yourResultTrain:
    imageTr.append(path[0])
    
for path in yourResultVal:
    imageTr.append(path[0])
 
    
    
imageTr_dict = {}
for content4 in imageTr:
    patientID4 = content4.split("\\")[-2][1:]
    imageTr_dict[patientID4] = content4


"""
Comparing the remote desktop data split and the one here in this computer, 
and splitting the data according to the datasplit in RD  
"""

RemoteDesktop_ImageSplit = imageTr_dict
HardDD_Images = image_dict

# Train images
for patientID_RD in RemoteDesktop_ImageSplit:
    for patientID_HDD in HardDD_Images:
        if patientID_RD == patientID_HDD:
            shutil.copy2(HardDD_Images[patientID_RD], r"D:\Uniklinik\nnUNet_data\nnUNet_raw_data_base\nnUNet_raw_data\Task13_Phlebolith_Stone\imagesTr")
            
            

            
# Train labels        
HardDD_Label = segmentation_dict
for patientID_RD in RemoteDesktop_ImageSplit:
    for patientID_HDD in HardDD_Label:
        if patientID_RD == patientID_HDD:
            print("Copying:", patientID_RD)
            shutil.copy2(HardDD_Label[patientID_RD],r"D:\Uniklinik\nnUNet_data\nnUNet_raw_data_base\nnUNet_raw_data\Task13_Phlebolith_Stone\labelsTr")
            

# Test image
RemoteDesktop_TestSplit = imageTs_dict
HardDD_Images = image_dict
for patientID_RD in RemoteDesktop_TestSplit:
    for patientID_HDD in HardDD_Images:
        if  patientID_RD == patientID_HDD:
            print("Copying:", patientID_RD)
            shutil.copy2(HardDD_Images[patientID_RD], r"D:\Uniklinik\nnUNet_data\nnUNet_raw_data_base\nnUNet_raw_data\Task13_Phlebolith_Stone\imagesTs")
            


# Test label
RemoteDesktop_TestSplit = imageTs_dict
HardDD_Label = segmentation_dict

for patientID_RD in RemoteDesktop_TestSplit:
    for patientID_HDD in HardDD_Label:
        if patientID_RD == patientID_HDD:
            print("Copying:", patientID_RD)
            shutil.copy2(HardDD_Label[patientID_RD],r"D:\Uniklinik\Phlebolith_Stone_Data\nnunet test labels")



    