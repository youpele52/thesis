# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 16:54:56 2020

@author: Youpele 
"""


import os
import pandas as pd
import nibabel as nib
import sys
sys.path.append("/Users/youpele/Documents/Uniklink Koeln/dice_calculation/thesis")
from evaluation_metrics import evaluation_metrics
join = os.path.join



def evaluating_segmentation_result(predictions, ground_truth, pred_dir, gt_dir):
    """

    Parameters
    ----------
    predictions : str
        Path to the prediction DL file.
    ground_truth : str
        Path to the ground truth file.
    pred_dir : str
        Path to the folder in which the prediction file is in.
    gt_dir : str
        Path to the folder in which the GT file is in.

    Returns
    -------
    DataFrame
        A DataFrame containing evaluation metrics such as:
            Dice coefficient, Accuracy, Sensitivity, Specificity, TP, TN, FP, and FN.

    """
    
    def binary_images (predictions, ground_truth, pred_dir, gt_dir, threshold, subject):
        
        subject_mask = subject + "_mask" + ".nii"    
        # pred
        pred_outputfile = join(pred_dir, subject_mask)
        img1 =  nib.load(predictions)
        I1 =img1.get_fdata()
        mask1=(I1==threshold)
        img_mask1 = nib.Nifti1Image(mask1, img1.affine, img1.header)
        nib.save(img_mask1,pred_outputfile)
        # gt
        gt_outputfile = join(gt_dir, subject_mask)
        img2 =  nib.load(ground_truth)
        I2 =img2.get_fdata()
        mask2=(I2==threshold)
        img_mask2 = nib.Nifti1Image(mask2, img2.affine, img2.header)
        nib.save(img_mask2,gt_outputfile)
        
        return {"pred_path":pred_outputfile,
                "gt_path": gt_outputfile}

    label_1 = binary_images (predictions, ground_truth, pred_dir, gt_dir, threshold = 1, subject = 'label_1' )
    label_2 = binary_images (predictions, ground_truth, pred_dir, gt_dir, threshold = 2, subject = 'label_2' )
    
    label_1_result = evaluation_metrics(predictions = label_1['pred_path'], ground_truth = label_1['gt_path'])
    label_2_result = evaluation_metrics(predictions = label_2['pred_path'], ground_truth = label_2['gt_path'])
    
    df = pd.DataFrame({"Pred file": predictions,
                       "GT file": ground_truth,
                       "Dice (label_1)": label_1_result["Dice"],
                       "Dice (label_2)": label_2_result["Dice"], 
                       "Accuracy (label_1)": label_1_result["Accuracy"],
                       "Accuracy (label_2)": label_2_result["Accuracy"],
                       "Sensitivity (label_1)": label_1_result["Sensitivity"],
                       "Sensitivity (label_2)": label_2_result["Sensitivity"],
                       "Specificity (label_1)": label_1_result["Specificity"],
                       "Specificity (label_2)": label_2_result["Specificity"],
                       "TP (label_1)": label_1_result["tp"],
                       "TP (label_2)": label_2_result["tp"], 
                       "TN (label_1)": label_1_result["tn"],
                       "TN (label_2)": label_2_result["tn"], 
                       "FP (label_1)": label_1_result["fp"],
                       "FP (label_2)": label_2_result["fp"], 
                       "FN (label_1)": label_1_result["fn"],
                       "FN (label_2)": label_2_result["fn"], 
                       }, index = [0])
    
    return  df
    








# case_35_df= evaluating_segmentation_result(predictions =  r"C:\Users\Youpele\Documents\dice_calculation\predictions\pred_case_00035_Segm.nii",
#                                    ground_truth =  r"C:\Users\Youpele\Documents\dice_calculation\GT\new_segmentation_35.nii", 
#                                    pred_dir = r"C:\Users\Youpele\Documents\dice_calculation\predictions", 
#                                    gt_dir = r"C:\Users\Youpele\Documents\dice_calculation\GT")

    