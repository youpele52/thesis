# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:21:57 2020

@author: michaely
"""

import numpy as np
import SimpleITK as sitk

def get_info (image_path):
    '''
    

    Parameters
    ----------
    image_path : String
        Path to the image.

    Returns
    -------
    image_info : Dictionary.
        Dictionary containing important information about the image.

    '''
    
    image_info = {}
    image_info['Origin'] = sitk.ReadImage(image_path).GetOrigin()
    image_info['Size']=sitk.ReadImage(image_path).GetSize()
    image_info['Spacing'] = sitk.ReadImage(image_path).GetSpacing()

    return image_info
    
