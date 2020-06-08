# -*- coding: utf-8 -*-
"""
Created on Fri May 22 15:36:23 2020

@author: michaely
"""


import os
import sys
sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts")
from seg_size_change import segmentation_size_change
import SimpleITK as sitk




# Getting the image size 
dicom_rootdir = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM"
dicom_list= os.listdir(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM")

images_sizes_dict = {}

for po in dicom_list:
    if 'x' in po:
        x = dicom_rootdir +  '\\' + po
        x_dir = x
        x_list = os.listdir(x)

        for i in x_list:
            image_path = x_dir  +  '\\' + i + '\kidney.nii'
            itk_image = sitk.ReadImage(image_path)
            image_size = itk_image.GetSize()
            images_sizes_dict[i+'_x'] = image_size
    else:
        image_path = dicom_rootdir +  '\\' + po + '\kidney.nii'
        itk_image = sitk.ReadImage(image_path)
        image_size = itk_image.GetSize()
        images_sizes_dict[po] = image_size
    



# Comparing the 

def change_size(alist,path):
    for key, value in images_sizes_dict.items():
        for keyz in alist:
            if key ==keyz:
                out_image_path = path + '\\' + keyz
                image_path = out_image_path + '\Segmentation.seg.nii'
                
                segmentation_size_change(image_path = image_path, 
                                         out_image_path = out_image_path, out_size = value)


'''
--------------
CHANGING SEGMENTATION SIZE TO MATCH RESPECTIVE IMAGE SIZE
Folder: 3DSlicer_Niere
--------------
'''


Niere_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere"
Niere_list = os.listdir(Niere_path)

alpha_path = Niere_path +  '\\' +  Niere_list[0]
alpha_list = os.listdir(alpha_path)

beta_path = Niere_path +  '\\' +  Niere_list[1]
beta_list = os.listdir(beta_path)

gamma_path = Niere_path +  '\\' +  Niere_list[2]
gamma_list = os.listdir(gamma_path)



change_size(alist = alpha_list ,path = alpha_path)

change_size(alist = beta_list ,path = beta_path)

change_size(alist = gamma_list ,path = gamma_path)




'''
--------------
CHANGING SEGMENTATION SIZE TO MATCH RESPECTIVE IMAGE SIZE
Folder: Folder: 3DSlicer_OhneBefund
--------------
'''


kappa_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_OhneBefund\Ohne Befund"
kappa_list = os.listdir(kappa_path)

change_size(alist = kappa_list ,path = kappa_path)




seggi = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_OhneBefund\Ohne Befund\P026\Segmentation.seg.nii"
itk_image1 = sitk.ReadImage(seggi)
segg_size = itk_image1.GetSize()
segg_space = itk_image1.GetSpacing()
segg_origin = itk_image1.GetOrigin()


# Read the data back from file
