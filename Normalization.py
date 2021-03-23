# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 15:22:50 2020

@author: michaely
"""



import os
import numpy as np
import nibabel as nib
# from shutil import copyfile
import matplotlib.pyplot as plt
from scipy import stats
join = os.path.join


def normalization (image_path, export_dir, export_name, create_mask = True, threshold = -900):
    # NOTE: if the script does not work, remove the entire docstring below.
    '''
    Creates a normalized image from a given image, and optionally a ROI mask for the image.

    Parameters
    ----------
    image_path : str
        Path to the image.
    export_dir : str
        Path to folder in which the created normalized image and ROI mask will be saved.
    export_name : str
        Name of the output image.
    create_mask: Boolean, Default is True
        Set to False, if you do not want a ROI mask.
    threshold: int, Default is -900
        Image intensity threshold used in creating the normalised image as well as the ROI mask.

    Returns
    -------
    None.

    '''
    
    print("Processing:", image_path)
    img = nib.load(image_path)
    I=img.get_fdata()
    #Define  mask
    mask=(I>threshold) 
    plt.imshow(mask[:,:,100])
    plt.show()
    plt.imshow(I[:,:,100])
    plt.show()
    
    # normalizing the image
    tmeanI=stats.tmean(I, (threshold,np.max(I)))
    tstdI=stats.tstd(np.ndarray.flatten(I), (threshold,np.max(I)))
    img_new=(I-tmeanI)/tstdI
    # img_new=(I-101)/76.9
    plt.imshow(img_new[:,:,100])
    plt.show()
    new_img = nib.Nifti1Image(img_new, img.affine, img.header)
    nib.save(new_img, join(export_dir, export_name + ".nii"))
    print("Normalized image created.")
    
    # creating image mask
    if create_mask == True:
        subject_mask = export_name + "_mask"
        img_mask = nib.Nifti1Image(mask, img.affine, img.header)
        nib.save(img_mask, join(export_dir, subject_mask + ".nii"))
        print("Image mask created.")
    
    
    
    
    
    
    
    
    
# normalization(image_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P001\windowed_image.nii", 
#               export_dir = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P001", 
#               export_name = "wind_norm", threshold = -900)    
    
# a =  r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P001\resampled_image.nii.gz"
# b = os.path.basename(a)
# c = os.path.splitext(b)[0]
