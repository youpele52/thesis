# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 01:12:38 2020

@author: Youpele
"""



import os
import numpy as np
import nibabel as nib
import pandas as pd
from datetime import datetime

join = os.path.join




class EvaluatePredictedFiles: 
    
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
                                normalize: bool=False):
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
    
    
    def evaluate_predicted_files_1(predictions_dir, ground_truth_dir,pred_nametag, gt_nametag, patientID_position = 1):
        """
        Creates an excel file as well as returns a DataFrame containing evaluation metrics such as:
        Dice coefficient, Accuracy, Sensitivity, Specificity, TP, TN, FP, and FN.
            
        Note:
            All the predicted files should be inside the given predictions_dir, and GT files in ground_truth_dir as well.
            
        Parameters
        ----------
        predictions_dir : str
            Path to the prediction directory. The excel file shall be saved here.
        ground_truth_dir : str
            Path to the GT directory.
        pred_nametag : str
            A filter to search for the predicted files in their directory.
        gt_nametag : str
            A filter to search for the GT files in their directory.
        patientID_position: int
            Position of the patient ID eg (case_00001) in path names in the gtLabels_ConfigFile.
            
        Returns
        -------
        df_merged : DataFrame containing evaluation metrics such as:
            Dice coefficient, Accuracy, Sensitivity, Specificity, TP, TN, FP, and FN..
        """
        df_list = []
        for content1 in os.listdir(predictions_dir):
            if pred_nametag in content1:
                patientID1 = int(content1.split("_")[patientID_position])
                for content2 in os.listdir(ground_truth_dir):
                    if gt_nametag in content2:
                        patientID2 = int(content2.split("_")[patientID_position])
                        if patientID1 == patientID2:
                            predicted_file = join(predictions_dir, content1)
                            GT_file = join(ground_truth_dir, content2)
                            # print(str(patientID1) + "\n" + predicted_file + "\n" + GT_file + "\n\n" )
                            result = EvaluatePredictedFiles.evaluating_segmentation_result(predictions = predicted_file, 
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
                            
        
        
    def evaluate_predicted_files_X(predictions_dir, ground_truth_dir,pred_nametag, gtLabels_ConfigFile,  
                                   patientID_position = -2, path_delimiter = "\\"):
        """
        Optimized for DeepMedic
        
        Creates an excel file as well as returns a DataFrame containing evaluation metrics such as: 
        Dice coefficient, Accuracy, Sensitivity, Specificity, TP, TN, FP, and FN.
        
        Parameters
        ----------
        predictions_dir : str
            Path to the prediction directory. The excel file shall be saved here.
        ground_truth_dir : str
            Path to the GT directory or any other directory of choice. 
            Only used for saving binary images.
        pred_nametag : str
            A filter to search for the predicted files in their directory.
            Required if there are other files in the directory.
        gtLabels_ConfigFile : str
            Path to the TEST gtLabels Config file .
        patientID_position: int
            Position of the patient ID eg (case_00001) in path names in the gtLabels_ConfigFile.
        path_delimiter: str
            Depends on how your paths are named in the gtLabels_ConfigFile. "/" for mac/linux based systems and "\\" for windows.
            
        Returns
        -------
        df_merged : DataFrame containing evaluation metrics such as:
            Dice coefficient, Accuracy, Sensitivity, Specificity, TP, TN, FP, and FN...
        """
        df_list = []
        
        read_GtLabels = [line.split('\n') for line in open(gtLabels_ConfigFile, "r").readlines()]
        gtLabels_path = {}
        for content1 in read_GtLabels:
            path = content1[0]
            patientID1 = path.split(path_delimiter)[patientID_position]
            gtLabels_path[patientID1] = path
            
            for content2 in os.listdir(predictions_dir):
                if patientID1 in content2:
                    if pred_nametag in content2:
                        predicted_file = join(predictions_dir, content2)
                        GT_file = gtLabels_path[patientID1]
                        
                        result = EvaluatePredictedFiles.evaluating_segmentation_result(predictions = predicted_file, 
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