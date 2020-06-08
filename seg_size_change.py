# -*- coding: utf-8 -*-
"""
Created on Fri May 22 15:36:23 2020

@author: caldeira & michaely
"""

#import numpy as np
import SimpleITK as sitk



def segmentation_size_change(image_path, out_image_path,out_size, 
                             segmentation_or_image = "segmentation", is_label=True):
    
    itk_image = sitk.ReadImage(image_path)
    
    # Resample images to 2mm spacing with SimpleITK
    original_spacing = itk_image.GetSpacing()
    #original_size = itk_image.GetSize()

    out_size = list(out_size)

    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(original_spacing)
    resample.SetSize(out_size)
    resample.SetOutputDirection(itk_image.GetDirection())
    resample.SetOutputOrigin(itk_image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(itk_image.GetPixelIDValue())

    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkBSpline)

    image = resample.Execute(itk_image)
    
    output_image = out_image_path +"/new_" +segmentation_or_image + ".nii"
    
    sitk.WriteImage(image, output_image)




