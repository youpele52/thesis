# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 20:46:41 2020

@author: Orginally written by Liliana, modified by Youpele
"""

import numpy as np
import SimpleITK as sitk


def resample(image_path, out_image_path, segmentation_or_image,
                 out_spacing=[0.75, 0.75, 1], is_label=False):
    
    itk_image = sitk.ReadImage(image_path)
    
    # Resample images to 2mm spacing with SimpleITK
    original_spacing = itk_image.GetSpacing()
    original_size = itk_image.GetSize()

    out_size = [
        int(np.round(original_size[0] * (original_spacing[0] / out_spacing[0]))),
        int(np.round(original_size[1] * (original_spacing[1] / out_spacing[1]))),
        int(np.round(original_size[2] * (original_spacing[2] / out_spacing[2])))]

    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(out_spacing)
    resample.SetSize(out_size)
    resample.SetOutputDirection(itk_image.GetDirection())
    resample.SetOutputOrigin(itk_image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(0)

    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkBSpline)

    image = resample.Execute(itk_image)
    
    output_image = out_image_path +"/resampled_" +segmentation_or_image + ".nii"
    
    sitk.WriteImage(image, output_image)






# Testing

# import sys
# sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts")
# from get_info import get_info


# before = get_info(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P001\kidney.nii")

# resample(image_path =r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P001\kidney.nii" , 
#          out_image_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P001", 
#          segmentation_or_image = 'image',
#           is_label=False)


# after = get_info(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P001\resampled_image.nii")
