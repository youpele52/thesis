# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 02:10:26 2020

@author: michaely
"""

# imports
import pandas as pd
from skimage.measure import label
from skimage.measure import regionprops
import SimpleITK as sitk
import os
import sys
from datetime import datetime
sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts")
from get_info import get_info


class PatientsImageInfo:
    def __init__(self,path):
        self.path = path
        
        
    @staticmethod
    def get_patients_image_info(path, keyword1='new', keyword2 = '.nii'):
        '''
        Extracts the information about a particular type of file of all the patients.

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
            DataFrame containing information about a particular type of file of all the patients.

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
                                
                                print("Patient", patient, "of", case, "is being processed.")
                                
                                image_path = os.path.join(patient_path,filtered_1)
                                image_info = get_info(image_path)
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
                                
                                
                                # sitk_image = sitk.ReadImage(image_path)
                                # data =  sitk.GetArrayFromImage(sitk_image)
                                
                                for prop in props_1:
                                    df = pd.DataFrame({"Case":case, "Patient":patient,
                                                  "File_name":filtered_1,
                                                  "Stone or Phlebolite":"Stone",
                                                  "Origin_X":image_info['Origin'][0], 
                                                  "Origin_Y":image_info['Origin'][1],
                                                  "Origin_Z":image_info['Origin'][2],
                                                  "Size_X":image_info['Size'][0],
                                                  "Size_Y":image_info['Size'][1],
                                                  "Size_Z":image_info['Size'][2],
                                                  "Spacing_X":image_info['Spacing'][0],
                                                  "Spacing_Y":image_info['Spacing'][1],
                                                  "Spacing_Z":image_info['Spacing'][2],
                                                  "Label":prop.label,
                                                  "Centroid": [prop.centroid],
                                                  "Voxel Area":prop.area,
                                                  "Voxel Volume": image_info['Spacing'][0] *\
                                                                      image_info['Spacing'][1]*\
                                                                          image_info['Spacing'][2],
                                                "Lesion Volume":image_info['Spacing'][0] *\
                                                          image_info['Spacing'][1]*\
                                                          image_info['Spacing'][2] * prop.area}, index = [0])
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
                                                  "Origin_X":image_info['Origin'][0], 
                                                  "Origin_Y":image_info['Origin'][1],
                                                  "Origin_Z":image_info['Origin'][2],
                                                  "Size_X":image_info['Size'][0],
                                                  "Size_Y":image_info['Size'][1],
                                                  "Size_Z":image_info['Size'][2],
                                                  "Spacing_X":image_info['Spacing'][0],
                                                  "Spacing_Y":image_info['Spacing'][1],
                                                  "Spacing_Z":image_info['Spacing'][2],
                                                  "Label":prop.label,
                                                  "Centroid": [prop.centroid],
                                                  "Voxel Area":prop.area,
                                                  "Voxel Volume": image_info['Spacing'][0] *\
                                                                      image_info['Spacing'][1]*\
                                                                          image_info['Spacing'][2],
                                                "Lesion Volume":image_info['Spacing'][0] *\
                                                          image_info['Spacing'][1]*\
                                                          image_info['Spacing'][2] * prop.area}, index = [0])
                                    
                                    listed_2.append(df)
                                    
                                    
                                listed_merged_2 =  pd.concat(listed_2)
                                listed_merged_2.index = range(0,len(listed_merged_2),1)
                                
                                result_list_for_patient = pd.concat([listed_merged_1,listed_merged_2])
                                
                                image_info_df_list.append(result_list_for_patient)

        image_info_df_merged =  pd.concat(image_info_df_list)
        image_info_df_merged.index = range(0,len(image_info_df_merged),1) 
        
        return image_info_df_merged
    
    def export_info (path,  keyword1='new', keyword2 = '.nii'):
        """
        Export an excel file containing all the information about each patient.

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
        None.

        """
        
        df = PatientsImageInfo.get_patients_image_info(path = path,keyword1=keyword1, keyword2=keyword2 )
        now = datetime.now()
        date = now.strftime("%m-%d-%Y")
        filename = "3DSlicer_Niere_info_" + date + ".xlsx"
        
        with pd.ExcelWriter( os.path.join(path,filename) ) as writer:
            
            df.to_excel(writer, sheet_name = "Kidney_stone_phlebolith_info")
        
        
        
        
                                
                                
                                
                                
            
        
        
        
        
        
        
path =  r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere"       
pdsheet = PatientsImageInfo.get_patients_image_info(r"C:\Users\michaely\Documents\hiwi\DeepMedic Stuff\Convert to nifti 20052020\3DSlicer_Niere")   

dfdf= PatientsImageInfo.export_info(path = path)





     