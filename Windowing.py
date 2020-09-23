#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 12:22:53 2020

@author: Vicente Rodríguez, modified by youpele
"""



import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import os


class Windowing():
    def windowing(image_path, window_center, window_width, export_dir, export_name):
        
        medical_image = nib.load(image_path)
        image = medical_image.get_fdata()
        
        # Transform the pixel values to the Hounsfield units
        def transform_to_hu(medical_image, image):
            intercept = medical_image.dataobj.inter #RescaleIntercept
            slope = medical_image.dataobj.slope #RescaleSlope
            hu_image = image * slope + intercept
            return hu_image
        
        # Window the image
        def window_image(image, window_center, window_width):
            img_min = window_center - window_width // 2
            img_max = window_center + window_width // 2
            window_image = image.copy()
            window_image[window_image < img_min] = img_min
            window_image[window_image > img_max] = img_max
            
            return window_image
        
        print("Processing:", image_path)
        hu_image = transform_to_hu(medical_image= medical_image, image = image)
        window_the_image = window_image(image = hu_image, 
                                        window_center = window_center, 
                                        window_width  = window_width)
        func = nib.load(image_path)
        ni_img = nib.Nifti1Image(window_the_image, func.affine)
        nib.save(ni_img, os.path.join(export_dir, export_name))
        
        print("Windowing successful.\nThe windowed image can be found here: ", str(os.path.join(export_dir, export_name)))
        
    def display_views(image_path):
    
        image_axis = 2
        medical_image = nib.load(image_path)
        image = medical_image.get_fdata()
        
        axial_image = image[:, :, 144] # Axis 2
        coronal_image = image[:, 144, :] # Axis 1
        sagital_image = image[110, :, :] # Axis 0
        
        plt.figure(figsize=(20, 10))
        plt.style.use('grayscale')
    
        plt.subplot(142)
        plt.imshow(np.rot90(axial_image))
        plt.title('Axial Plane')
        plt.axis('off')
    
        plt.subplot(143)
        plt.imshow(np.rot90(coronal_image))
        plt.title('Coronal Plane')
        plt.axis('off')
        
        plt.subplot(141)
        plt.imshow(np.rot90(sagital_image))
        plt.title('Sagital Plane')
        plt.axis('off')

        


# Testing

# Windowing.windowing(image_path="/Volumes/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/Task11_Kits19/imagesTr/case_00200_resampled_image.nii.gz",
#                     window_center = 90, 
#                     window_width= 1600, 
#                     export_dir = "/Users/youpele/Desktop", 
#                     export_name = "windowed_image_1.nii.gz")


# Windowing.display_views("/Volumes/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/Task11_Kits19/imagesTr/case_00200_resampled_image.nii.gz")

# Windowing.display_views("/Users/youpele/Desktop/windowed_image_1.nii.gz")

# get_info("/Users/youpele/Desktop/windowed_image_1.nii.gz")