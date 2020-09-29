# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:52:46 2020

@author: Youpele & Kautenja 
"""


import os
import numpy as np
import nibabel as nib
import pandas as pd
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
        """
        Creates binary images

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
        threshold : int
            Integer used for masking.
        subject : str
            Name given to the created binary file.

        Returns
        -------
        dict
            A dictionary containing the file paths to the creaetd binary images.

        """
        
        subject_mask = subject + "_mask" + ".nii"    
        # pred
        pred_outputfile = join(pred_dir, subject_mask)
        print("Evaluating:", predictions)
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
    
    def evaluation_metrics (predictions, ground_truth,
                            negative: int=0.0,
                            positive: int=1.0,
                            normalize: bool=True):
        """
        
        Parameters
        ----------
        predictions : Str
            Path to the prediction DL file.
        ground_truth : TYPE
            Path to the ground truth file.
        negative : int, optional
            DESCRIPTION. The default is 0.0.
        positive : int, optional
            DESCRIPTION. The default is 1.0.
        normalize : bool, optional
            DESCRIPTION. The default is True.
    
        Returns
        -------
        dict
            A dictionary of the evaluation metrics such as:
                Dice coefficient, Accuracy, Sensitivity, Specificity, TP, TN, FP, and FN.
    
        """
        
        predictions =  nib.load(predictions).get_fdata().copy()
        ground_truth =  nib.load(ground_truth).get_fdata().copy()
        
        # compute the raw accuracy
        acc = np.mean(predictions == ground_truth)
        # accumulate the true/false negative/positives
        tp = np.sum(np.logical_and(predictions == positive, ground_truth == positive))
        tn = np.sum(np.logical_and(predictions == negative, ground_truth == negative))
        fp = np.sum(np.logical_and(predictions == positive, ground_truth == negative))
        fn = np.sum(np.logical_and(predictions == negative, ground_truth == positive))
        
        # Dice coefficient 
        dice = 2 * tp / (fn + (2 * tp) + fp)
        # Accuracy
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        # Sensitivity
        sensitivity = tp / (tp + fn)
        # Specificity
        specificity = tn / (tn + fp)
        
        # normalize the true/false negative/positives to a percentages if
        # normalization is enabled
        if normalize:
            # calculate the total number of positive guesses
            total_positive = np.sum(predictions == positive)
            if total_positive == 0:
                # avoid divide by zero
                tp = 0
                fp = 0
            else:
                # normalize by the total number of positive guesses
                tp = tp / total_positive
                fp = fp / total_positive
    
            # calculate the total number of negative guesses
            total_negative = np.sum(predictions == negative)
            if total_negative == 0:
                # avoid divide by zero
                tn = 0
                fn = 0
            else:
                # normalize by the total number of negative guesses
                tn = tn / total_negative
                fn = fn / total_negative
    
        # return a dictionary of the raw accuracy and true/false positive/negative
        # values
    
        return { 'Dice': dice,
            'Accuracy': accuracy,
            'Sensitivity' : sensitivity,
            'Specificity' : specificity, 
            'acc': acc,
            'tp': tp,
            'tn': tn,
            'fp': fp,
            'fn': fn,
            }


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
    





# case_35_df2= evaluating_segmentation_result(predictions =  r"C:\Users\Youpele\Documents\dice_calculation\predictions\pred_case_00035_Segm.nii",
#                                     ground_truth =  r"C:\Users\Youpele\Documents\dice_calculation\GT\new_segmentation_35.nii", 
#                                     pred_dir = r"C:\Users\Youpele\Documents\dice_calculation\predictions", 
#                                     gt_dir = r"C:\Users\Youpele\Documents\dice_calculation\GT")

    