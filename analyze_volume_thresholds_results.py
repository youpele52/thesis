#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:23:40 2021

@author: youpele
"""


import pandas as pd
import os
from datetime import datetime
join = os.path.join

now = datetime.now()
date = now.strftime("%d%m%Y")


def analyze_volume_thresholds_results(results_dir, volume_threshold_2,test_session_name, delimeter = "/",
                                      volume_threshold_1= 0, case_ID_position = 1):

    df_list = []
    for content in os.listdir(results_dir):
        if content[0]!= '.'and 'combine' in content:
            filepath = join(results_dir, content)
            caseID = "P" + str(content.split('_')[case_ID_position])
            print("Processing: ", caseID)
            
            df_dict = pd.read_excel(filepath, sheet_name=None)
            df_result = pd.DataFrame()
            
            for key in df_dict.keys():
                if 'Missed' in key:
                    if str(volume_threshold_1) in key:
                        df = pd.read_excel(filepath, sheet_name = key,usecols="C")
                        df_result["Case ID"] = [caseID]
                        df_result['File Path'] = [filepath]
                        num_of_missed_lesions_1 = len(df.index)
                        df_result["Number of missed lesions (vol_thresh=" + str(volume_threshold_1) +')'] = [num_of_missed_lesions_1]
                        df_result[ 'Average Volume of Missed Lesions (vol_thresh=' + str(volume_threshold_1) +')'] = [float(df.mean())]
                    elif str(volume_threshold_2) in key:
                        df = pd.read_excel(filepath, sheet_name = key,usecols="C")
                        df_result["Case ID"] = [caseID]
                        df_result['File Path'] = [filepath]
                        num_of_missed_lesions_2 = len(df.index)
                        df_result["Number of missed lesions (vol_thresh=" + str(volume_threshold_2) +')'] = [num_of_missed_lesions_2]
                        df_result[ 'Average Volume of Missed Lesions (vol_thresh=' + str(volume_threshold_2) +')' ] = [float(df.mean())]
                        
                elif 'FalsePositives' in key:
                    if str(volume_threshold_1) in key:
                        df = pd.read_excel(filepath, sheet_name = key,usecols="C")
                        df_result["Case ID"] = [caseID]
                        df_result['File Path'] = [filepath]
                        num_of_false_positive_1 = len(df.index)
                        df_result["Number of False Positive (vol_thresh=" + str(volume_threshold_1) +')'] = [num_of_false_positive_1]
                        df_result[ 'Average Volume of False Postives (vol_thresh=' + str(volume_threshold_1) +')'] = [float(df.mean())]
                    elif str(volume_threshold_2) in key:
                        df = pd.read_excel(filepath, sheet_name = key,usecols="C")
                        df_result["Case ID"] = [caseID]
                        df_result['File Path'] = [filepath]
                        num_of_false_positive_2 = len(df.index)
                        df_result["Number of  False Positive (vol_thresh=" + str(volume_threshold_2) +')'] = [num_of_false_positive_2]
                        df_result[ 'Average Volume of False Postives (vol_thresh=' + str(volume_threshold_2) +')' ] = [float(df.mean())]
            
            df_list.append(df_result)
                
    df_merged = pd.concat(df_list) 
    df_merged.index = range(0,len(df_merged), 1)
    
    with pd.ExcelWriter(join(results_dir,test_session_name + '_threshold_analysis_'+ date +'.xlsx')) as writer:
        df_merged.to_excel(writer, sheet_name = 'Threshold Analysis')
                





Example
analyze_volume_thresholds_results(results_dir =  '/Volumes/Youpele_HD/Uniklinik/Scripts/Prostate/ml',
                                  volume_threshold_2 = 1,
                                  test_session_name = 'stone_phlebolith')
    
 






