#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 18:55:51 2020

@author: liliana & youpele
"""

import os
import numpy as np
import nibabel as nib
import pandas as pd
import datetime
import time
from skimage import measure
join = os.path.join



class FullEvaluation:
    
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
    
    
    def full_evaluation(predictions, ground_truth, pred_dir, gt_dir, fname):
        
        MLfile = predictions
        GTfile = ground_truth
        
        DDMMYYYY=datetime.date.today()
        todaysdate =str(DDMMYYYY.day)+str(DDMMYYYY.month)+str(DDMMYYYY.year)
        filename = fname + "_" + todaysdate + ".xlsx"
        writer=pd.ExcelWriter(join(pred_dir, filename),engine='xlsxwriter')
        
        dfresults=pd.DataFrame()
        ListofDetected=pd.DataFrame()
        ListofFP=pd.DataFrame()
        ListofMissed=pd.DataFrame()
        Categories=[]
        Volume=[]
        Dicevector=[]
        
        labeldetected=[]
        labeldetectedML=[]

        imgML = nib.load(MLfile)
        dataML=imgML.get_fdata()
        dataML_labels = measure.label(dataML, background=0)
       
        #LC from here
        imgGT = nib.load(GTfile)
        dataGT=imgGT.get_fdata()
        dataGT_labels = measure.label(dataGT, background=0)
 
        #Full Images Dice
        TPfull=np.multiply(dataML,dataGT)
        FPfull=np.multiply(dataML,np.logical_not(dataGT))
        FNfull=np.multiply(np.logical_not(dataML),dataGT)
        TNfull=np.multiply(np.logical_not(dataML),np.logical_not(dataGT))
        VolumeMLfull=np.sum(dataML)
            
        dice = 2 * np.sum(TPfull) / (np.sum(FNfull) + (2 * np.sum(TPfull)) + np.sum(FPfull))
 
       #Going through GT labels to decide whether a lesion was missed or detected
        for labelGT in range(1,np.max(dataGT_labels)+1):
            dataGT1=(dataGT_labels==labelGT)
            VolumeGT1=np.sum(dataGT1)
                        
            A=imgGT.header.get_zooms()
            TP=np.multiply(dataML,dataGT1)
            FP=np.multiply(dataML,np.logical_not(dataGT1))
            FN=np.multiply(np.logical_not(dataML),dataGT1)
            TN=np.multiply(np.logical_not(dataML),np.logical_not(dataGT1))
            VolumeGT=np.sum(dataGT)

            #If there are no True Positives, Then the lesion was missed, otherewise there was detection.
            if np.sum(TP)==0:
                #Missed
                Missed={'Volume GT':VolumeGT1*A[0]*A[1]*A[2]}
                ListofMissed=ListofMissed.append(Missed,ignore_index=True)
                results = {'ML file': MLfile,'Label ML': 0,'GT file': GTfile, 'Label GT': labelGT,
                           'TP':np.sum(TP),'FP':np.sum(FP),'FN':np.sum(FN),'TN':np.sum(TN),
                           'Volume GT': VolumeGT1*A[0]*A[1]*A[2], 'Volume ML': VolumeMLfull*A[0]*A[1]*A[2], 
                           'Detected': 0, 'Missed': 1,'False Positive':0,'TP Full':np.sum(TPfull),
                           'FP Full':np.sum(FPfull),'FN full':np.sum(FNfull),'TN Full':np.sum(TNfull),
                           'VolumeML Full':VolumeMLfull*A[0]*A[1]*A[2], "Full Dice": dice}
                dfresults = dfresults.append(results, ignore_index = True)
                Categories.append('Missed')
                Volume.append(VolumeGT)
                Dicevector.append(0)
                print('Lable MISSED ',labelGT)
            else:
                labeldetected.append(labelGT)
                print('label appended ',labelGT)
        
        #Going through ML labels to decide whether a lesion was FP or detected

        for label in range(1,np.max(dataML_labels)+1):
            dataML1=(dataML_labels==label)
            VolumeML1=np.sum(dataML1)
            FalsePositiveFlag=1

            A=imgGT.header.get_zooms()
            TP=np.multiply(dataML1,dataGT)
            FP=np.multiply(dataML1,np.logical_not(dataGT))
            FN=np.multiply(np.logical_not(dataML1),dataGT)
            TN=np.multiply(np.logical_not(dataML1),np.logical_not(dataGT))
            VolumeGT1=np.sum(dataGT)
            VolumeGT=np.sum(dataGT)

            #If there is no overlap with the complete ground truth than it is a false positive
            if np.sum(TP)==0:
                FalsePositive={'Volume ML':VolumeML1*A[0]*A[1]*A[2]}
                ListofFP=ListofFP.append(FalsePositive,ignore_index=True)
                results = {'ML file': MLfile,'Label ML':label,'GT file': GTfile,'Label GT': 0 ,'TP':np.sum(TP),'FP':np.sum(FP),'FN':np.sum(FN),'TN':np.sum(TN),'Volume GT': VolumeGT*A[0]*A[1]*A[2], 'Volume ML': VolumeML1*A[0]*A[1]*A[2], 'Detected': 0, 'Missed': 0,'False Positive':1,'TP Full':np.sum(TPfull),'FP Full':np.sum(FPfull),'FN full':np.sum(FNfull),'TN Full':np.sum(TNfull),'VolumeML Full':VolumeMLfull*A[0]*A[1]*A[2], 'Full Dice': 2 * np.sum(TPfull) / (np.sum(FNfull) + (2 * np.sum(TPfull)) + np.sum(FPfull))}
                dfresults = dfresults.append(results, ignore_index = True)
                Categories.append('FalsePositive')
                Volume.append(VolumeML1)
                Dicevector.append(0)
                print('Label FALSE POSITIVE', label)
    
            else: 
                labeldetectedML.append(label)
                print('Label ML appended',label)
            
        #Labels that are not either Missed or False positives    
        print('labeldetected is ',labeldetected)
        print('labeldetectedML is ', labeldetectedML)
        for labelGT2 in labeldetected:
            dataGT1=(dataGT_labels==labelGT2)
            VolumeGT1=np.sum(dataGT1)
            for labelML in labeldetectedML:
                dataML1=(dataML_labels==labelML)
                VolumeML1=np.sum(dataML1)
        #Here there was one detection, but we don't know with which lables
            #Going thru ML labels
            #Goign thru ML lables for false postives            
                TP=np.multiply(dataML1,dataGT1)
                FP=np.multiply(dataML1,np.logical_not(dataGT1))
                FN=np.multiply(np.logical_not(dataML1),dataGT1)
                TN=np.multiply(np.logical_not(dataML1),np.logical_not(dataGT1))
                VolumeGT1=np.sum(dataGT1)

                if np.sum(TP)==0:
                        #Not the right label
                    print('Not the right label ML', labelML, 'for label GT', labelGT2)
                else:
                    #Detected label
                    DetectedFlag=1

                    Dice=2*np.sum(TP)/(2*np.sum(TP)+np.sum(FN)+np.sum(FP))
                    Sens=np.sum(TP)/(np.sum(TP)+np.sum(FN))
                    Spec=np.sum(TN)/(np.sum(TN)+np.sum(FP))
                    Acc=(np.sum(TP)+np.sum(TN))/(np.sum(TP)+np.sum(TN)+np.sum(FP)+np.sum(FN))
                    Prec=np.sum(TP)/(np.sum(TP)+np.sum(FP))
                    F1_score=2*Prec*Sens/(Sens+Prec)
                    Detected={'Volume GT':VolumeGT1*A[0]*A[1]*A[2],'Volume ML':VolumeML1*A[0]*A[1]*A[2],'TP': np.sum(TP),'FP':np.sum(FP),'FN':np.sum(FN),'TN':np.sum(TN),'Dice': Dice,'Sens': Sens, 'Spec': Spec, 'Acc': Acc, 'Prec': Prec, 'F1-score': F1_score,'TP Full':np.sum(TPfull),'FP Full':np.sum(FPfull),'FN full':np.sum(FNfull),'TN Full':np.sum(TNfull),'VolumeML Full':VolumeMLfull*A[0]*A[1]*A[2]} 
                    ListofDetected=ListofDetected.append(Detected,ignore_index=True)    
                    results = {'ML file': MLfile,'Label ML':labelML,'GT file': GTfile,'Label GT': labelGT2 ,'TP':np.sum(TP),'FP':np.sum(FP),'FN':np.sum(FN),'TN':np.sum(TN),'Volume GT': VolumeGT*A[0]*A[1]*A[2], 'Volume ML': VolumeML1*A[0]*A[1]*A[2], 'Detected': 1, 'Missed': 0,'False Positive':0,'TP Full':np.sum(TPfull),'FP Full':np.sum(FPfull),'FN full':np.sum(FNfull),'TN Full':np.sum(TNfull),'VolumeML Full':VolumeMLfull*A[0]*A[1]*A[2]}
                    dfresults = dfresults.append(results, ignore_index = True)
                    Categories.append('Detected')
                    Volume.append(VolumeGT)
                    Dicevector.append(Dice)


        dfresults.to_excel(writer,'CNN Evaluation',)# columns=['ML file','Label ML','GT file','Label GT','TP','FP','FN','TN','Volume GT', 'Volume ML','Detected','Missed','False Positive','TP Full', 'FP Full', 'FN full', 'TN Full', 'VolumeML Full',"Full Dice" ])
        if not(ListofDetected.empty):
            ListofDetected.to_excel(writer,'Detected',)# columns=['Volume GT','Volume ML','TP','FP','FN','TN','Dice','Sens','Spec','Acc','Prec','F1-score','TP Full', 'FP Full', 'FN full', 'TN Full', 'VolumeML Full'])
        if not(ListofMissed.empty):
            ListofMissed.to_excel(writer,'Missed', )# columns=['Volume GT'])
        ListofFP.to_excel(writer,'FalsePositives',)#  columns=[ 'Volume ML'])
        writer.save()
        

    def run_FullEvaluation(predictions, ground_truth, pred_dir, gt_dir, fname):
        start = time.time()
        label_1 = FullEvaluation.binary_images (predictions, ground_truth, pred_dir, gt_dir, threshold = 1, subject = 'label_1' )
        label_2 = FullEvaluation.binary_images (predictions, ground_truth, pred_dir, gt_dir, threshold = 2, subject = 'label_2' )
        
        print("Evaluating: label = 1")
        full_evaluation_for_label_1 = FullEvaluation.full_evaluation(pred_dir = pred_dir, gt_dir = gt_dir, fname = fname + '_label_1',
                                                                     predictions  = label_1['pred_path'],
                                                                     ground_truth = label_1['gt_path'])
        print("Evaluation of label = 1 is successful, goto: ", pred_dir)
        print("Evaluating: label = 2")
        full_evaluation_for_label_2 = FullEvaluation.full_evaluation(pred_dir = pred_dir, gt_dir = gt_dir, fname = fname + '_label_2',
                                                                     predictions  = label_2['pred_path'], 
                                                                     ground_truth = label_2['gt_path'],)
        end = time.time()
        duration = end - start
        print("Evaluation of label = 2  is successful, goto: ", pred_dir)
        print('Time elapsed:',duration,'seconds.')
        
    
    def run_FullEvaluation_folder_based(pred_dir, gt_dir,pred_nametag, gt_nametag, patientID_position = 1):
        
        start = time.time()
        predictions_dir = pred_dir
        ground_truth_dir = gt_dir
        
        df_list = []
        for content1 in os.listdir(predictions_dir):
            if pred_nametag in content1:
                patientID1 = int(content1.split("_")[patientID_position])
                for content2 in os.listdir(ground_truth_dir):
                    if gt_nametag in content2:
                        patientID2 = int(content2.split("_")[patientID_position])
                        if patientID1 == patientID2:
                            fname = "case_" + str(patientID1)
                            predicted_file = join(predictions_dir, content1)
                            GT_file = join(ground_truth_dir, content2)
                            
                            # Full evaluation
                            full_evaluation = FullEvaluation.run_FullEvaluation(predictions = predicted_file, 
                                                                                ground_truth = GT_file , 
                                                                                pred_dir = pred_dir, 
                                                                                gt_dir = gt_dir, 
                                                                                fname = fname)
        
        end = time.time()
        duration = end - start
        print('TOTAL Time elapsed:',duration,'seconds.')
        
    
    def run_FullEvaluation_DeepMedic_based(pred_dir, gt_dir,pred_nametag, gtLabels_ConfigFile,
                                           patientID_position = -2, path_delimiter = "\\"):
        
        start = time.time()
        predictions_dir = pred_dir
        ground_truth_dir = gt_dir
        
        df_list = []
        
        read_GtLabels = [line.split('\n') for line in open(gtLabels_ConfigFile, "r").readlines()]
        gtLabels_path = {}
        for content1 in read_GtLabels:
            path = content1[0]
            patientID1 = path.split(path_delimiter)[patientID_position]
            gtLabels_path[patientID1] = path
            
            for content2 in os.listdir(predictions_dir):
                if patientID1 in content2:
                    fname = "case_" + str(patientID1)
                    if pred_nametag in content2:
                        predicted_file = join(predictions_dir, content2)
                        GT_file = gtLabels_path[patientID1]
                        
                        # Full evaluation
                        full_evaluation = FullEvaluation.run_FullEvaluation(predictions = predicted_file,
                                                                            ground_truth = GT_file , 
                                                                            pred_dir = pred_dir, 
                                                                            gt_dir = gt_dir, 
                                                                            fname = fname)
                        
        end = time.time()
        duration = end - start
        print('TOTAL Time elapsed:',duration,'seconds.')
        
        

# # Testing 

#FullEvaluation.run_FullEvaluation(predictions = "/Users/youpele/Documents/UKK/dice_calculation/predictions/pred_case_00035_Segm.nii.gz", 
#                                  ground_truth= '/Users/youpele/Documents/UKK/dice_calculation/GT/new_segmentation_35.nii', 
#                                  pred_dir = "/Users/youpele/Documents/UKK/dice_calculation/predictions", 
#                                  gt_dir = '/Users/youpele/Documents/UKK/dice_calculation/GT', 
#                                  fname = "case_35")
        
# FullEvaluation.run_FullEvaluation(predictions = 'C:\\Users\\caldeiral\\Downloads\\check\\check\\predictions\\pred_case_00035_Segm.nii.gz', 
#                                   ground_truth= 'C:\\Users\\caldeiral\\Downloads\\check\\check\\GT\\new_segmentation_35.nii', 
#                                   pred_dir = 'C:\\Users\\caldeiral\\Downloads\\check\\check\\predictions', 
#                                   gt_dir = 'C:\\Users\\caldeiral\\Downloads\\check\\check\\GT', 
#                                   fname = "case_35")
    
# FullEvaluation.run_FullEvaluation(predictions = "/Users/youpele/Documents/UKK/dice_calculation/check_LC/predictions/pred_case_00035_Segm.nii.gz", 
#                                   ground_truth= '/Users/youpele/Documents/UKK/dice_calculation/check_LC/GT/new_segmentation_35.nii', 
#                                   pred_dir = "/Users/youpele/Documents/UKK/dice_calculation/check_LC/predictions", 
#                                   gt_dir = '/Users/youpele/Documents/UKK/dice_calculation/check_LC/GT', 
#                                   fname = "case_35") 
    
    
    
