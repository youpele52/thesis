# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 13:41:25 2020

@author: michaely
"""



# import os
# import sys
# sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts")
# from seg_size_change import segmentation_size_change
import SimpleITK as sitk



def segmentation_size_change(image_path, out_image_path, seg_I_mean_real_image_path,
                             segmentation_or_image = "segmentation", is_label=True):
    
    itk_image = sitk.ReadImage(image_path)
    
    
    original_spacing = sitk.ReadImage(seg_I_mean_real_image_path).GetSpacing()
    
    original_size = sitk.ReadImage(seg_I_mean_real_image_path).GetSize()
    
    original_origin = sitk.ReadImage(seg_I_mean_real_image_path).GetOrigin()


    out_size = original_size # list(out_size)

    resample = sitk.ResampleImageFilter()
    
    # work 1
    resample.SetOutputSpacing(original_spacing )
    
    
    # work 2
    resample.SetSize(out_size) # leave unchanged 
    
    resample.SetOutputDirection(itk_image.GetDirection())

    # work 3
    # resample.SetOutputOrigin(itk_image.GetOrigin())
    
    resample.SetOutputOrigin(original_origin)


    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(0) #(itk_image.GetPixelIDValue(0))

    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkBSpline)

    image = resample.Execute(itk_image)
    
    output_image = out_image_path +"/new_" +segmentation_or_image + ".nii"
    
    sitk.WriteImage(image, output_image)



# Tring it out

experiment = segmentation_size_change(image_path=r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine\P001\Segmentation.seg.nii",
                                      seg_I_mean_real_image_path= r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P001\kidney.nii",
                                      
                                     out_image_path= r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine\P001")


