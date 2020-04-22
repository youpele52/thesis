# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:36:29 2020

@author: Orginally written by Liliana, modified by Youpele
"""



import numpy as np
import SimpleITK as sitk



def resample_img(image_path, out_image_path, segmentation_or_image,
                 out_spacing=[2.0, 2.0, 2.0], is_label=False):
    
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
    resample.SetDefaultPixelValue(itk_image.GetPixelIDValue())

    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkBSpline)

    image = resample.Execute(itk_image)
    
    output_image = out_image_path +"/new_" +segmentation_or_image + ".nii"
    
    sitk.WriteImage(image, output_image)







# IMAGE

image_path = r"D:\Uniklinik\kits19\data\case_00001\imaging.nii"
out_image_path = r"D:\Uniklinik\kits19\data\case_00001"

resampled_sitk_img = resample_img(image_path = image_path, 
                                  out_image_path=out_image_path,
                                  segmentation_or_image = "image",
                                  out_spacing=[2.0, 2.0, 2.0], is_label=False)



# Segmentation
image_path = r"D:\Uniklinik\kits19\data\case_00001\segmentation.nii"
out_image_path = r"D:\Uniklinik\kits19\data\case_00001"

resampled_sitk_img = resample_img(image_path = image_path, 
                                  out_image_path=out_image_path,
                                  segmentation_or_image = "segmentation",
                                  out_spacing=[2.0, 2.0, 2.0], is_label=True)

