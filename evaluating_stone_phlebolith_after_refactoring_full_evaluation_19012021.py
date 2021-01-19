#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:47:06 2021

@author: youpele
"""

import os
import sys
sys.path.append('/Volumes/Youpele_HD/Uniklinik/Scripts/Prostate')
from full_evaluation import FullEvaluation as FE


'''
Task15_Phlebolith_Stone_windowed_60_360
'''

FE.run_FullEvaluation_folder_based(pred_dir = '/Volumes/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_trained_models/nnUNet/3d_fullres/Task015_Phlebolith_Stone_windowed_60_360/predicted_cases_fold_0', 
                                   gt_dir = '/Volumes/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_trained_models/nnUNet/3d_fullres/Task015_Phlebolith_Stone_windowed_60_360/nnunet_test_labels_nii', 
                                   pred_nametag = 'nii.gz', 
                                   gt_nametag = 'nii', 
                                   volume_threshold = 3)







