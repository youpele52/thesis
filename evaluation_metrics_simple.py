# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 17:39:13 2020

@authors:  Kautenja & Youpele
"""

import os
import numpy as np
import nibabel as nib
join = os.path.join


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
    


# case_35_label_2 = evaluation_metrics(ground_truth = r"C:\Users\Youpele\Documents\dice_calculation\GT\label_2_mask.nii", 
#                                      predictions = r"C:\Users\Youpele\Documents\dice_calculation\predictions\label_2_mask.nii")
