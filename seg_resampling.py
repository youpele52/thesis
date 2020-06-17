# -*- coding: utf-8 -*-
"""
Created on Fri May 22 15:36:23 2020
Modified 12:47 16.06.2020 

@author: michaely
"""

import SimpleITK as sitk
import os



def segmentation_resampling(seg_path, image_path, out_seg_path, is_label=True):
    '''
    Resamples segmentation.

    Parameters
    ----------
    seg_path : String.
        Path to the segmentation.
    out_seg_path : String
        Folder where the resampled segmentation would be saved.
    image_path : String.
        Image path.
    is_label : Boolean, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    None.

    '''
    
    
    seg = sitk.ReadImage(seg_path)

    original_spacing = sitk.ReadImage(image_path).GetSpacing()
    original_size = sitk.ReadImage(image_path).GetSize()
    original_origin = sitk.ReadImage(image_path).GetOrigin()

    out_size = original_size 
    
    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(original_spacing)
    resample.SetSize(out_size)     
    resample.SetOutputDirection(seg.GetDirection())
    resample.SetOutputOrigin(original_origin)
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(0) 

    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkBSpline)

    seg_image = resample.Execute(seg)
    
    output_seg = out_seg_path + "/new_segmentation.nii"
    
    sitk.WriteImage(seg_image, output_seg)


# LEGACY CODE

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
    resample.SetDefaultPixelValue(0) #(itk_image.GetPixelIDValue(0))

    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkBSpline)

    image = resample.Execute(itk_image)
    
    output_image = out_image_path +"/new_" +segmentation_or_image + ".nii"
    
    sitk.WriteImage(image, output_image)




# how to call 

# experiment = segmentation_resampling(seg_path=r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine\P001\Segmentation.seg.nii", 
#                                      out_seg_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere\Steine\P001", 
#                                      image_path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\DICOM_Niere\DICOM\P001\kidney.nii")



