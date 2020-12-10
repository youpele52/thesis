# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 19:39:25 2020

@author: michaely
"""

import os
import nibabel as nib
from scipy import ndimage


def fill_holes(image_path, export_dir, export_name):
    '''
    Fill the holes in a binary image.

    Parameters
    ----------
    image_path : str
        Path to the image.
    export_dir : str
        Folder path in which the output image will be saved.
    export_name : str
        Name of the output image.

    Returns
    -------
    None.

    '''
    medical_image = nib.load(image_path)
    image = medical_image.get_fdata()
    image_filled = ndimage.binary_fill_holes(image).astype(int)
    func = nib.load(image_path)
    ni_img = nib.Nifti1Image(image_filled, func.affine)
    nib.save(ni_img, os.path.join(export_dir, export_name))





# How to use 
# fill_holes(image_path =  r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P001\normalised_image_mask.nii", 
#            export_dir = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P001", 
#            export_name = "mask_fillup2")


