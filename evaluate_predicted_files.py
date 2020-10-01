#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:35:03 2020

@author: michaely
"""

import pandas as pd
import os
import sys
# sys.path.append("/media/michaely/Youpele_HD/Uniklinik/Scripts")
sys.path.append("D:/Uniklinik/Scripts/evaluating_segmentation_result_OneForAll.py")
from evaluating_segmentation_result_OneForAll import evaluating_segmentation_result 
from datetime import datetime
join = os.path.join





class EvaluatePredictedFiles:
    def evaluate_predicted_files_1(predictions_dir, ground_truth_dir,pred_nametag, gt_nametag):
        df_list = []
        for content1 in os.listdir(predictions_dir):
            if pred_nametag in content1:
                patientID1 = int(content1.split("_")[1])
                for content2 in os.listdir(ground_truth_dir):
                    if gt_nametag in content2:
                        patientID2 = int(content2.split("_")[1])
                        if patientID1 == patientID2:
                            predicted_file = join(predictions_dir, content1)
                            GT_file = join(ground_truth_dir, content2)
                            # print(str(patientID1) + "\n" + predicted_file + "\n" + GT_file + "\n\n" )
                            result = evaluating_segmentation_result(predictions = predicted_file, 
                                                                    ground_truth = GT_file, 
                                                                    pred_dir = predictions_dir, 
                                                                    gt_dir = ground_truth_dir)
                            df_list.append(result)
        df_merged = pd.concat(df_list)
        df_merged.index = range(0,len(df_merged),1)
        
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        filename = "Test_result_" + date + ".xlsx"
        
        with pd.ExcelWriter(join(predictions_dir,filename) ) as writer:            
            df_merged.to_excel(writer, sheet_name = "Test Result")  
            
        return df_merged
        
                            
                            
        "Used when all the predicted files are in one folder, same as the GTs"
    def evaluate_predicted_files_X():
        "Used when the predicted files and GT are in multiple subfolders"




# Testing        
# ab = EvaluatePredictedFiles.evaluate_predicted_files_1(predictions_dir = r"D:\Uniklinik\nnUNet_data\nnUNet_trained_models\nnUNet\3d_fullres\Task012_Kits19_windowed\nnUNetTrainerV2__nnUNetPlansv2.1\fold_0\validation_raw", 
#                                                   ground_truth_dir = r"D:\Uniklinik\nnUNet_data\nnUNet_raw_data_base\nnUNet_raw_data\Task12_Kits19_windowed\labelsTr",
#                                                   pred_nametag = "case",
#                                                   gt_nametag = "case")


# ab = EvaluatePredictedFiles.evaluate_predicted_files_1(predictions_dir = r"D:\Uniklinik\nnUNet_data\nnUNet_trained_models\nnUNet\3d_fullres\Task012_Kits19_windowed\predicted_cases_fold_0", 
#                                                   ground_truth_dir = r"D:\Uniklinik\nnUNet_data\nnUNet_raw_data_base\nnUNet_raw_data\Task12_Kits19_windowed\imagesTs",
#                                                   pred_nametag = "case",
#                                                   gt_nametag = "case")





# ab = EvaluatePredictedFiles.evaluate_predicted_files_1(predictions_dir = "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_trained_models/nnUNet/3d_fullres/Task012_Kits19_windowed/predicted_cases_fold_0", 
#                                                   ground_truth_dir = "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/nnUNet_raw_data/Task012_Kits19_windowed/imagesTs",
#                                                   pred_nametag = "case",
#                                                   gt_nametag = "case")




# ab = evaluating_segmentation_result(predictions =  "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_trained_models/nnUNet/3d_fullres/Task012_Kits19_windowed/predicted_cases_fold_0/case_00163_windowed_image.nii.gz", 
#                                     ground_truth = "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/nnUNet_raw_data/Task012_Kits19_windowed/imagesTs/case_00163_windowed_image.nii.gz" , 
#                                     pred_dir = "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_trained_models/nnUNet/3d_fullres/Task012_Kits19_windowed/predicted_cases_fold_0", 
#                                     gt_dir =  "/media/michaely/Youpele_HD/Uniklinik/nnUNet_data/nnUNet_raw_data_base/nnUNet_raw_data/nnUNet_raw_data/Task012_Kits19_windowed/imagesTs")
