#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:08:28 2021

@author: michaely
"""

from datetime import datetime
import os
import sys
sys.path.append("/home/michaely/Documents/Script")
from resampling_prostate_main import resample
from get_info import get_info
join = os.path.join


todays_date = datetime.now().strftime('%d%m20%y')
main_dir = '/home/lenzmi/deepmedic/prostate_risk/data/withoutPIRADS/res_to_T2/test'

for patient in os.listdir(main_dir):
    patient_dir = join(main_dir, patient)
    
    for content in os.listdir(patient_dir):
        if 'ROI' in content:
            patient_ROI = join(patient_dir, content)
            out_patient_ROI = patient_ROI.split('.nii')[0]  +'_' + todays_date + ".nii.gz"
            # print(patient_ROI,  out_patient_ROI )
            resample(image_path = patient_ROI, 
                     out_image_path = out_patient_ROI, 
                     out_spacing=[1, 1, 1],
                     is_label=True)
            
        elif 'Gtlabels' in content:
            patient_GT = join(patient_dir, content)
            out_patient_GT =  patient_GT.split('.nii')[0]  +'_' + todays_date + ".nii.gz"
            # print(patient_GT,out_patient_GT )
            resample(image_path = patient_GT , 
                     out_image_path = out_patient_GT, 
                     out_spacing=[1, 1, 1],
                     is_label=True)
        else:
            patient_Image = join(patient_dir, content)
            out_patient_Image = patient_Image.split('.nii')[0]  +'_' + todays_date + ".nii.gz"
            resample(image_path  = patient_Image, 
                     out_image_path = out_patient_Image, 
                     out_spacing=[1, 1, 1],
                     is_label=False)
            
            
        
        
        
        
        
        
        
        
        
        

# TESTING 

# get_info(image_path='/home/lenzmi/deepmedic/prostate_risk/data/withoutPIRADS/res_to_T2/test/Prostate_6_new/ADC_resampled_norm.nii.gz')       

# resample(image_path = '/home/lenzmi/deepmedic/prostate_risk/data/withoutPIRADS/res_to_T2/test/Prostate_6_new/ADC_resampled_norm.nii.gz', 
#           out_image_path = '/home/lenzmi/deepmedic/prostate_risk/data/withoutPIRADS/res_to_T2/test/Prostate_6_new/ADC_resampled_norm_NEWWWWWWWWWWW.nii.gz', 
#           out_spacing=[1, 1, 1], 
#           is_label=False)  
    
    
# get_info( '/home/lenzmi/deepmedic/prostate_risk/data/withoutPIRADS/res_to_T2/test/Prostate_6_new/ADC_resampled_norm_NEWWWWWWWWWWW.nii.gz')



    
    
    