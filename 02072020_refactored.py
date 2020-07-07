# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:03:56 2020

@author: michaely
"""

# imports
import pandas as pd
from skimage.measure import label
from skimage.measure import regionprops
import SimpleITK as sitk
import os
import sys
sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts")
from get_info import get_info


class PatientsImageInfo:
    def __init__(self,path):
        self.path = path

    @staticmethod
    def getBasicInfo(path, keyword1='new', keyword2 = '.nii'):
        '''
        Extracts the basic information about a particular type of file of all the patients.

        Parameters
        ----------
        path : String
            Path to the folder containing all cases folder. The case folder each contains patients image files.
        keyword1 : String, optional
            Filter to look for certain file(s) containing the inputted string. The default is 'new'.
        keyword2 : String, optional
            Filter to look for certain file(s) containing the inputted string. The default is '.nii'.

        Returns
        -------
        image_info_df_merged : DataFrame
            DataFrame containing basic information about a particular type of file of all the patients.

        '''
        cases = os.listdir(path)
        image_info_df_list = []
        for case in cases:
            case_path = os.path.join(path, case)
            if os.path.isdir(case_path):
                patients = os.listdir(case_path)
                
                for patient in patients:
                    patient_path = os.path.join(case_path, patient)
                    patient_dir_content = os.listdir(patient_path)
                    
                    for content in patient_dir_content:
                        if keyword1 in content:
                            filtered_0 = content
                            if keyword2 in filtered_0:
                                filtered_1 = filtered_0
                                
                                image_path = os.path.join(patient_path,filtered_1)
                                image_info = get_info(image_path)
                                sitk_image = sitk.ReadImage(image_path)
                                data =  sitk.GetArrayFromImage(sitk_image)
                                print("Patient", patient, "of", case, "is being processed.")
                                image_info_df = pd.DataFrame({"Case":case, "Patient":patient,
                                                  "File_name":filtered_1,
                                                  "Origin_X":image_info['Origin'][0], 
                                                  "Origin_Y":image_info['Origin'][1],
                                                  "Origin_Z":image_info['Origin'][2],
                                                  "Size_X":image_info['Size'][0],
                                                  "Size_Y":image_info['Size'][1],
                                                  "Size_Z":image_info['Size'][2],
                                                  "Spacing_X":image_info['Spacing'][0],
                                                  "Spacing_Y":image_info['Spacing'][1],
                                                  "Spacing_Z":image_info['Spacing'][2],
                                                  "Image Dimension (sitk)": sitk_image.GetDimension(),
                                                  "Image np Array Shape": [data.shape],}, index = [0]) 
                                image_info_df_list.append(image_info_df)
        image_info_df_merged =  pd.concat(image_info_df_list)
        image_info_df_merged.index = range(0,len(image_info_df_merged),1) 
        
        return image_info_df_merged
    
    
    
    @staticmethod
    def getLabelInfo(path,  keyword1='new', keyword2 = '.nii'):
        '''
        
        Extracts the label information about a particular type of file of all the patients.
        
        Parameters
        ----------
        path : String
            Path to the folder containing all cases folder. The case folder each contains patients image files.
        keyword1 : String, optional
            Filter to look for certain file(s) containing the inputted string. The default is 'new'.
        keyword2 : String, optional
            Filter to look for certain file(s) containing the inputted string.. The default is '.nii'.

        Returns
        -------
        image_info_df_merged : DataFrame
            DataFrame containing label information about a particular type of file of all the patients.

        '''
        cases = os.listdir(path)
        image_info_df_list = []
        for case in cases:
            case_path = os.path.join(path, case)
            if os.path.isdir(case_path):
                patients = os.listdir(case_path)
                
                for patient in patients:
                    patient_path = os.path.join(case_path, patient)
                    patient_dir_content = os.listdir(patient_path)
                    
                    for content in patient_dir_content:
                        if keyword1 in content:
                            filtered_0 = content
                            if keyword2 in filtered_0:
                                filtered_1 = filtered_0
                                
                                image_path = os.path.join(patient_path,filtered_1)
                                
                                print("Patient", patient, "of", case, "is being processed.")
                                
                                reader = sitk.ImageFileReader()
                                reader.SetFileName(image_path)
                                image = reader.Execute();
                                data = sitk.GetArrayFromImage(image)
                                data.shape
                                Stone_label = data[:,:,:,0]
                                Phlebolite_label = data[:,:,:,1]
                                
                                # Getting info about the Stones            
                                final_ROIs_1 = Stone_label
                                label_final_ROIs_1 = label(final_ROIs_1)
                                props_1 = regionprops(label_final_ROIs_1)
                                
                                listed_1 = [pd.DataFrame()]

                                for prop in props_1:
                                    df = pd.DataFrame({"Case":case, "Patient":patient,
                                                  "File_name":filtered_1,
                                                  "Stone or Phlebolite":"Stone",
                                                       "Label":prop.label,
                                                        "Centroid": [prop.centroid],
                                                        "Voxel Area":prop.area}, index = [0])
                                    listed_1.append(df)
                                    
                                listed_merged_1 =  pd.concat(listed_1)
                                listed_merged_1.index = range(0,len(listed_merged_1),1)

                                # Getting info about the Phlebolites
                                
                                final_ROIs_2 = Phlebolite_label
                                label_final_ROIs_2 = label(final_ROIs_2)
                                props_2 = regionprops(label_final_ROIs_2)
                                
                                listed_2 = [pd.DataFrame()]
                                for prop in props_2:
                                    df = pd.DataFrame({"Case":case, "Patient":patient,
                                                  "File_name":filtered_1,
                                                  "Stone or Phlebolite":"Phlebolite",
                                                       "Label":prop.label,
                                                            "Centroid": [prop.centroid],
                                                            "Voxel Area":prop.area}, index = [0])
                                    listed_2.append(df)
                                    
                                    
                                listed_merged_2 =  pd.concat(listed_2)
                                listed_merged_2.index = range(0,len(listed_merged_2),1)
                                
                                result_list_for_patient = pd.concat([listed_merged_1,listed_merged_2])
                                
                                image_info_df_list.append(result_list_for_patient)

        image_info_df_merged =  pd.concat(image_info_df_list)
        image_info_df_merged.index = range(0,len(image_info_df_merged),1) 
        
        return image_info_df_merged
    
    @staticmethod
    def getExcel (path):
        '''
        Export an excel file containing all the information about each patient.

        Parameters
        ----------
        path : String
            Path to the folder containing all cases folder. The case folder each contains patients image files.

        Returns
        -------
        None.

        '''
        
        basic_info = PatientsImageInfo.getBasicInfo(path)
        label_info = PatientsImageInfo.getLabelInfo(path)
        
        with pd.ExcelWriter( os.path.join(path,"3DSlicer_Niere_info.xlsx") ) as writer:
            basic_info.to_excel(writer, sheet_name = "basic_info")
            label_info.to_excel(writer, sheet_name = "label_info")
            
        

        
    
                                
        
        
                                
                                
                                
                                
                
# # how to call

# pdsheet = PatientsImageInfo.getBasicInfo(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere")

# path = r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere"

# with pd.ExcelWriter( os.path.join(path,"3DSlicer_Niere.xlsx") ) as writer:
#     pdsheet.to_excel(writer, sheet_name = "3DSlicer_Niere")



# asasas =PatientsImageInfo.getDimensions(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere")



# label_info = PatientsImageInfo.getLabelInfo(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere")




# with pd.ExcelWriter( os.path.join(path,"label_info.xlsx") ) as writer:
#     label_info.to_excel(writer, sheet_name = "label_info")




# export = PatientsImageInfo.getExcel(path)



