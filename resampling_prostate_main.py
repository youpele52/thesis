# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 20:46:41 2020

@author: Orginally written by Liliana, modified by Youpele
"""

import numpy as np
import SimpleITK as sitk


def resample(image_path, out_image_path,
                 out_spacing=[0.75, 0.75, 1], is_label=False):
    # NOTE: if the script does not work, remove the entire docstring below.
    '''
    Resamples a given image.

    Parameters
    ----------
    image_path : str
        Path to the image.
    out_image_path: str
        Path to folder in which the resampled image will be saved.
    out_spacing: list, Default is [0.75, 0.75, 1]
        List containing three numbers that will be used to resample the image in x, y and z axis.
    is_label: Boolean, Default is False.
        If the image is a label, sitk.sitkNearestNeighbor is used to interpolate the image, else sitk.sitkBSpline is used.
    
    Returns
    -------
    None.

    '''
    
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
    
    # output_image = out_image_path +"/resampled_" +segmentation_or_image + ".nii"
    
    sitk.WriteImage(image, out_image_path)

