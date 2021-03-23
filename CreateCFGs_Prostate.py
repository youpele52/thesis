#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 13:45:24 2021

@author: michaely
"""


# from datetime import datetime
import os
join = os.path.join





def create_prostate_cfgs(main_dir, export_dir, search_term  ):
    # NOTE: if the script does not work, remove the entire docstring below.
    '''
    Creates GtLabels, Channels_t2grase, RoiMasks, Channels_t2tse, Channels_adc and NamesOfPredictions CFG files.
    The created CFG files will contain list of paths. 
    Example: GtLabels.cfg will contain a list of paths for all the GT files.
    
    Parameters
    ----------
    main_dir : String
        Path to the main folder which contains all the patients' folder. Each patient's folder
        should contain Gtlabels_T2TSE, T2GraSe, ROI_T2TSE etc files. 
    export_dir : String
        Path to the folder in which the created CFG files will be saved.
    search_term : String
        In cases where there are mutiple Gtlabels_T2TSEs, search_term is used to 
        specify the exact one needed. 
        Example: search_term = '03032021', if date is used to distinguish the different Gtlabels_T2TSEs.

    Returns
    -------
    None.

    '''

    # todays_date = datetime.now().strftime('%d%m20%y')
    dir_name = main_dir.split('/')[-1]
    
    GtLabels = []
    Channels_t2grase = [] 
    RoiMasks = []
    Channels_t2tse = []
    NamesOfPredictions = []
    Channels_adc = []
    
    
    for patient in os.listdir(main_dir):
        if patient[0] == 'P':
            # print(patient)
            NamesOfPredictions.append('pred_' + patient + '.nii.gz')
            patient_dir = join(main_dir, patient)
            
            for content in os.listdir(patient_dir):
                if search_term in content:
                    if 'Gtlabels_T2TSE' in content:
                        GtLabels.append( join(patient_dir, content)  )   
                    elif 'T2GraSe' in content:
                        Channels_t2grase.append( join(patient_dir, content)  )
                    elif 'ROI_T2TSE' in content:
                        RoiMasks.append( join(patient_dir, content)  )
                    elif 'T2TSE' in content:
                        Channels_t2tse.append( join(patient_dir, content)  )
                    elif content[0] == 'A':
                        Channels_adc.append(  join(patient_dir, content) )
                        
                    
    with open( join(export_dir, dir_name + 'GtLabels.cfg' ), 'w' ) as f:
        f.writelines("%s\n" % line for line in GtLabels)       
    
    with open( join(export_dir, dir_name + 'Channels_t2grase.cfg' ), 'w' ) as f:
        f.writelines("%s\n" % line for line in Channels_t2grase)    
                    
    with open( join(export_dir, dir_name + 'RoiMasks.cfg' ), 'w' ) as f:
        f.writelines("%s\n" % line for line in RoiMasks)                     
    
    with open( join(export_dir, dir_name + 'Channels_t2tse.cfg' ), 'w' ) as f:
        f.writelines("%s\n" % line for line in Channels_t2tse)                     
    
    with open( join(export_dir, dir_name + 'NamesOfPredictions.cfg' ), 'w' ) as f:
        f.writelines("%s\n" % line for line in NamesOfPredictions)                     
                    
    with open( join(export_dir, dir_name + 'Channels_adc.cfg' ), 'w' ) as f:
        f.writelines("%s\n" % line for line in Channels_adc)                     
    
    



# Testing

# main_dir = '/home/lenzmi/deepmedic/prostate_risk/data/withoutPIRADS/res_to_T2/test'
# export_dir = '/home/lenzmi/deepmedic/prostate_risk/configFiles/deepMedic/noP_T2TSE+ADC_T2_03032021/test'
# search_term = '03032021'

# create_prostate_cfgs(main_dir, export_dir, search_term )


# # training 
# create_prostate_cfgs(main_dir = '/home/lenzmi/deepmedic/prostate_risk/data/withoutPIRADS/res_to_T2/train', 
#                       export_dir = '/home/lenzmi/deepmedic/prostate_risk/configFiles/deepMedic/noP_T2TSE+ADC_T2_03032021/train', 
#                       search_term  = '03032021')

# # validation
# create_prostate_cfgs(main_dir = '/home/lenzmi/deepmedic/prostate_risk/data/withoutPIRADS/res_to_T2/train/validation', 
#                       export_dir = '/home/lenzmi/deepmedic/prostate_risk/configFiles/deepMedic/noP_T2TSE+ADC_T2_03032021/train/validation', 
#                       search_term  = '03032021')


