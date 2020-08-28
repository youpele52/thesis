# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 12:01:22 2020

@author: michaely
"""


from datetime import datetime
import os

class Create_CFGs:     
    def create_cfgs_plus_roi(project_name="kits19"):
        now = datetime.now()
        todays_date = now.strftime("%d%m%Y")
        
        # Training files
        
        traing_dir = r"C:\Users\michaely\Documents\deepmedic-master\deepmedic-master\examples\configFiles\deepMedic\train"
        train_name = project_name + "Train"
        
        with open(os.path.join(traing_dir, train_name + "Channels_flair_" + todays_date + 'Edition.cfg'), 'w') as f:
            training_images = train_set['image']
            f.writelines("%s\n" % line for line in training_images)     
            
        with open(os.path.join(traing_dir, train_name + "GtLabels_" + todays_date + 'Edition.cfg'), 'w') as f:
            training_gTLabels = train_set['segmentation']
            f.writelines("%s\n" % line for line in training_gTLabels)
            
        with open(os.path.join(traing_dir, train_name + "RoiMasks_" + todays_date + 'Edition.cfg'), 'w') as f:
            training_roi_Mask = train_set['roi_Mask']
            f.writelines("%s\n" % line for line in training_roi_Mask)
    
        # Validation files
        val_dir = r"C:\Users\michaely\Documents\deepmedic-master\deepmedic-master\examples\configFiles\deepMedic\train\validation"
        val_name = project_name + "Validation"      
        
        with open(os.path.join(val_dir, val_name + "Channels_flair_" + todays_date + 'Edition.cfg'), 'w') as f:
            val_images = val_set['image']
            f.writelines("%s\n" % line for line in val_images) 
            
        with open(os.path.join(val_dir, val_name + "GtLabels_" + todays_date + 'Edition.cfg'), 'w') as f:
            val_gTLabels = val_set['segmentation']
            f.writelines("%s\n" % line for line in val_gTLabels) 
            
        with open(os.path.join(val_dir, val_name + "RoiMasks_" + todays_date + 'Edition.cfg'), 'w') as f:
            val_roi_Mask = val_set['roi_Mask']
            f.writelines("%s\n" % line for line in val_roi_Mask) 
        
        with open(os.path.join(val_dir, val_name + "NamesOfPredictions" + todays_date + 'Edition.cfg'), 'w') as f:
            val_NamesOfPredictions = val_pred_set
            f.writelines("%s\n" % line for line in val_NamesOfPredictions) 
            
        # Test files
        test_dir = r"C:\Users\michaely\Documents\deepmedic-master\deepmedic-master\examples\configFiles\deepMedic\test"
        test_name = project_name + "Test"     
        
        with open(os.path.join(test_dir, test_name + "Channels_flair_" + todays_date + 'Edition.cfg'), 'w') as f:
            test_images = test_set['image']
            f.writelines("%s\n" % line for line in test_images) 
        
        with open(os.path.join(test_dir, test_name + "GtLabels_" + todays_date + 'Edition.cfg'), 'w') as f:
            test_gTLabels = test_set['segmentation']
            f.writelines("%s\n" % line for line in test_gTLabels) 
        
        with open(os.path.join(test_dir, test_name + "RoiMasks_" + todays_date + 'Edition.cfg'), 'w') as f:
            test_roi_Mask= test_set['roi_Mask']
            f.writelines("%s\n" % line for line in test_roi_Mask) 
        
        with open(os.path.join(test_dir, test_name + "NamesOfPredictions" + todays_date + 'Edition.cfg'), 'w') as f:
            test_NamesOfPredictions =test_pred_set
            f.writelines("%s\n" % line for line in test_NamesOfPredictions) 
            
    def create_cfgs_no_roi(project_name="kits19"):
        now = datetime.now()
        todays_date = now.strftime("%d%m%Y")
        
        # Training files
        
        traing_dir = r"C:\Users\michaely\Documents\deepmedic-master\deepmedic-master\examples\configFiles\deepMedic\train"
        train_name = project_name + "Train"
        
        with open(os.path.join(traing_dir, train_name + "Channels_flair_" + todays_date + 'Edition.cfg'), 'w') as f:
            training_images = train_set['image']
            f.writelines("%s\n" % line for line in training_images)     
            
        with open(os.path.join(traing_dir, train_name + "GtLabels_" + todays_date + 'Edition.cfg'), 'w') as f:
            training_gTLabels = train_set['segmentation']
            f.writelines("%s\n" % line for line in training_gTLabels)
            
        # with open(os.path.join(traing_dir, train_name + "RoiMasks_" + todays_date + 'Edition.cfg'), 'w') as f:
        #     training_roi_Mask = train_set['roi_Mask']
        #     f.writelines("%s\n" % line for line in training_roi_Mask)
    
        # Validation files
        val_dir = r"C:\Users\michaely\Documents\deepmedic-master\deepmedic-master\examples\configFiles\deepMedic\train\validation"
        val_name = project_name + "Validation"      
        
        with open(os.path.join(val_dir, val_name + "Channels_flair_" + todays_date + 'Edition.cfg'), 'w') as f:
            val_images = val_set['image']
            f.writelines("%s\n" % line for line in val_images) 
            
        with open(os.path.join(val_dir, val_name + "GtLabels_" + todays_date + 'Edition.cfg'), 'w') as f:
            val_gTLabels = val_set['segmentation']
            f.writelines("%s\n" % line for line in val_gTLabels) 
            
        # with open(os.path.join(val_dir, val_name + "RoiMasks_" + todays_date + 'Edition.cfg'), 'w') as f:
        #     val_roi_Mask = val_set['roi_Mask']
        #     f.writelines("%s\n" % line for line in val_roi_Mask) 
        
        with open(os.path.join(val_dir, val_name + "NamesOfPredictions" + todays_date + 'Edition.cfg'), 'w') as f:
            val_NamesOfPredictions = val_pred_set
            f.writelines("%s\n" % line for line in val_NamesOfPredictions) 
            
        # Test files
        test_dir = r"C:\Users\michaely\Documents\deepmedic-master\deepmedic-master\examples\configFiles\deepMedic\test"
        test_name = project_name + "Test"     
        
        with open(os.path.join(test_dir, test_name + "Channels_flair_" + todays_date + 'Edition.cfg'), 'w') as f:
            test_images = test_set['image']
            f.writelines("%s\n" % line for line in test_images) 
        
        with open(os.path.join(test_dir, test_name + "GtLabels_" + todays_date + 'Edition.cfg'), 'w') as f:
            test_gTLabels = test_set['segmentation']
            f.writelines("%s\n" % line for line in test_gTLabels) 
        
        # with open(os.path.join(test_dir, test_name + "RoiMasks_" + todays_date + 'Edition.cfg'), 'w') as f:
        #     test_roi_Mask= test_set['roi_Mask']
        #     f.writelines("%s\n" % line for line in test_roi_Mask) 
        
        with open(os.path.join(test_dir, test_name + "NamesOfPredictions" + todays_date + 'Edition.cfg'), 'w') as f:
            test_NamesOfPredictions =test_pred_set
            f.writelines("%s\n" % line for line in test_NamesOfPredictions) 
            
        
        
        
    
    
    
    
    
Create_CFGs.create_cfgs_plus_roi()
    
    
    