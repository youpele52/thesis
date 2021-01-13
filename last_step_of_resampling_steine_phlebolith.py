# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 15:25:01 2020

@author: caldeiral and michaely
"""

import SimpleITK as sitk
import os

# used for resampling 4D images made up of two 3D images

def last_step_resampling (out_image_path, input_image, reference_image):
    
    itk_image_input = sitk.ReadImage(input_image)
    itk_image_reference = sitk.ReadImage(reference_image)
    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(itk_image_reference.GetSpacing())
    resample.SetSize(itk_image_reference.GetSize())
    resample.SetOutputDirection(itk_image_reference.GetDirection())
    resample.SetOutputOrigin(itk_image_reference.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(0)
    
    resample.SetInterpolator(sitk.sitkNearestNeighbor)
    
    image = resample.Execute(itk_image_input)
    
    output_image = os.path.join(out_image_path ,"resampledsize_combine_image.nii")
    
    sitk.WriteImage(image, output_image)


    