#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 01:54:33 2020

@author: youpele
"""

import pandas as pd
import os
from datetime import datetime
join = os.path.join




def after_full_evaluation(predict_test_result, test_cases, export_dir, delimeter = "/", delimeter2 = "/"):
    
    now = datetime.now()
    date = now.strftime("%d%m%Y")
    test_result = pd.read_excel(predict_test_result)
    listed1 = []
    listed2 = []
    for a in range(0,10,1):
        case_ID1 = int(test_result.iloc[a:a+1,2:3].to_numpy()[0][0].split(delimeter)[-1].split("_")[1])

        dice_label_1 =  test_result.iloc[a:a+1,3:4].to_numpy()[0][0]
        dice_label_2 = test_result.iloc[a:a+1,4:5].to_numpy()[0][0]
        
        for content in os.listdir(test_cases):
            if 'label_1' in content:
                file_path = join(test_cases,content )
                # Case ID
                case_ID2 =  int(file_path.split(delimeter2)[-1].split("_")[1])
                
                if case_ID1 == case_ID2:
                    # High Dice
                    high_dice_df = pd.read_excel(file_path,sheet_name = 'Detected', usecols = "C" )
                    # GT Volume
                    gt_volume = pd.read_excel(file_path,sheet_name = 'Detected', usecols = 'p' )
                    # Missed lesions
                    try:
                        missed = pd.read_excel(file_path,sheet_name = 'Missed', usecols = 'B' )
                    except:
                        missed = pd.DataFrame(columns = ['Volume GT'])
                        print("case",case_ID2, "'label_1' does not have any missed lesions!")
                    # False Positives    
                    false_positive = pd.read_excel(file_path,sheet_name = 'FalsePositives', usecols = 'B' )
                    if false_positive.shape[0]>0:
                        pass
                    else:
                        false_positive = pd.DataFrame( columns = ['Volume ML'] )
                        print("case", case_ID2, "'label_1' does not have any false positive!")
                        
                    df1 = pd.DataFrame({"Case ID": case_ID2, "Global Dice": dice_label_1,
                                        "High Dice":  high_dice_df ["Dice"], 
                                        'Number of Missed Lesions':missed.shape[0],
                                        'Average Volume of Missed Lesions': missed['Volume GT'].mean(),
                                        'Number of FP': false_positive.shape[0],
                                        'Average Volume of FP': false_positive['Volume ML'].mean(),
                                        'GT Volume': gt_volume['Volume GT']})
                    listed1.append(df1)
                    
                
            elif 'label_2' in content:
                file_path = join(test_cases,content )
                case_ID2 =  int(file_path.split(delimeter2)[-1].split("_")[1])
                
                if case_ID1 == case_ID2:
                    # High Dice
                    high_dice_df = pd.read_excel(file_path,sheet_name = 'Detected', usecols = "C" )
                    # GT Volume
                    gt_volume = pd.read_excel(file_path,sheet_name = 'Detected', usecols = 'p' )
                    # Missed lesions
                    try:
                        missed = pd.read_excel(file_path,sheet_name = 'Missed', usecols = 'B' )
                    except:
                        missed = pd.DataFrame(columns = ['Volume GT'])
                        print("case",case_ID2, "'label_2' does not have any missed lesions!")
                    # False Positives    
                    false_positive = pd.read_excel(file_path,sheet_name = 'FalsePositives', usecols = 'B' )
                    if false_positive.shape[0]>0:
                        pass
                    else:
                        false_positive = pd.DataFrame( columns = ['Volume ML'] )
                        print("case", case_ID2, "'label_2' does not have any false positive!")
                        
                    df2 = pd.DataFrame({"Case ID": case_ID2, "Global Dice": dice_label_2,
                                        "High Dice":  high_dice_df ["Dice"], 
                                        'Number of Missed Lesions':missed.shape[0],
                                        'Average Volume of Missed Lesions': missed['Volume GT'].mean(),
                                        'Number of FP': false_positive.shape[0],
                                        'Average Volume of FP': false_positive['Volume ML'].mean(),
                                        'GT Volume': gt_volume['Volume GT']})
                    listed2.append(df2)

        listed1_merged = pd.concat(listed1)        
        listed1_merged.index = range(0,len(listed1_merged), 1)
        listed2_merged = pd.concat(listed2)        
        listed2_merged.index = range(0,len(listed2_merged), 1)
        
        # Saving the generated info into an excel file
        with pd.ExcelWriter(join(export_dir,'after_full_evaluation_'+ date +'.xlsx')) as writer:
            listed1_merged.to_excel(writer, sheet_name = 'label_1')
            listed2_merged.to_excel(writer, sheet_name = 'label_2')
        
        

    



# Testing

# predict_test_result  = "/Users/youpele/Google Drive/FH Aachen/Thesis at Uniklinik Koeln/result_evaluation/nnUnet/Task011_Kits19/test_Task011_Kits19_Test_result_28-10-2020 copy.xlsx"
# test_cases = "/Users/youpele/Google Drive/FH Aachen/Thesis at Uniklinik Koeln/result_evaluation/nnUnet/Task011_Kits19/test_cases"
# export_dir = "/Users/youpele/Google Drive/FH Aachen/Thesis at Uniklinik Koeln/result_evaluation/nnUnet/Task011_Kits19"


# after_full_evaluation(predict_test_result, test_cases, export_dir, delimeter = "/")



























    







