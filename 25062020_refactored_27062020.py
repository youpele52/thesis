# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 14:41:23 2020

@author: Youpele
"""


import pandas as pd
import os
import sys
sys.path.append(r"D:\Uniklinik\Scripts")
from get_info import get_info






class pickT2TSEFile():
    """
    Path: Path to the folder containing all the patient prostate files.
    """
    def __init__(self,prostate_path):
        self.prostate_path = prostate_path
        # self.prostate_list = os.listdir(self.prostate_path)
        
    @staticmethod
    def get_T2LO_prefix(prostate_path):
        
        '''
        Extract the first three numbers of the files having LO and T2 in their names.

        Parameters
        ----------
        prostate_path : String
            Path the folder containing all the patient files.

        Returns
        -------
        lo_prefix_dict : Dictionary
            Dictionary containing the first three numbers of the files having LO and T2 in their names.

        '''
        prostate_list = os.listdir(prostate_path)
        lo_prefix_dict = {}
        
        for patient in prostate_list:
            patient_path = os.path.join(prostate_path,patient)
            if os.path.isdir(patient_path):
                patient_images_path = os.path.join(patient_path,"1")
                patient_images_list = os.listdir(patient_images_path)
                for patient_image in patient_images_list:
                    if "LO" in patient_image:
                        lo_im = patient_image
                        if "T2" in lo_im:
                            lo_prefix = patient_image[0:3]
                            lo_prefix_dict[patient] = lo_prefix
                            
        return lo_prefix_dict
    
    @staticmethod
    def get_T2TSE_info(prostate_path):
        
        '''
        Extract the necessary information about T2TSE files of all the patients.

        Parameters
        ----------
        prostate_path : String
            Path the folder containing all the patient files.

        Returns
        -------
        image_info_df_merged : DataFrame
            DataFrame containing necessary information about T2TSE files of all the patients.

        '''
        prostate_list = os.listdir(prostate_path)
        image_info_df_list = []
        
        for patient in prostate_list:
            patient_path = os.path.join(prostate_path,patient)
            if os.path.isdir(patient_path):
                patient_images_path = os.path.join(patient_path,"1")
                patient_images_list = os.listdir(patient_images_path)
                for patient_image in patient_images_list:
                    prefix = pickT2TSEFile.get_T2LO_prefix(prostate_path)
                    if prefix[patient] in patient_image:
                        filtered_0 = patient_image
                        if "T2TSE" in filtered_0:
                            filtered_1 = filtered_0
                            
                            image_path =  os.path.join(patient_images_path,filtered_1)
                            image_info = get_info(image_path)
                            print("Processing: ", image_path)
                            image_info_df = pd.DataFrame({"Patient":patient,
                                                  "File_name":filtered_1,
                                                  "Origin_X":image_info['Origin'][0], 
                                                  "Origin_Y":image_info['Origin'][1],
                                                  "Origin_Z":image_info['Origin'][2],
                                                  "Size_X":image_info['Size'][0],
                                                  "Size_Y":image_info['Size'][1],
                                                  "Size_Z":image_info['Size'][2],
                                                  "Spacing_X":image_info['Spacing'][0],
                                                  "Spacing_Y":image_info['Spacing'][1],
                                                  "Spacing_Z":image_info['Spacing'][2],}, index = [0]) 
                            image_info_df_list.append(image_info_df)
                            
        
        image_info_df_merged =  pd.concat(image_info_df_list)  
        image_info_df_merged.index = range(0,len(image_info_df_merged),1) 
        
        return image_info_df_merged
    
    @staticmethod
    def get_GraSe_info(prostate_path):
        '''
        

        Parameters
        ----------
        prostate_path : String
            Path the folder containing all the patient files.

        Returns
        -------
        image_info_df_merged : DataFrame.
            DataFrame containing necessary information about GraSe files of all the patients.
        '''
        prostate_list = os.listdir(prostate_path)
        image_info_df_list = []
        
        for patient in prostate_list:
            patient_path = os.path.join(prostate_path,patient)
            if os.path.isdir(patient_path):
                patient_images_path = os.path.join(patient_path,"1")
                patient_images_list = os.listdir(patient_images_path)
                for patient_image in patient_images_list:
                    if "GraSe" in patient_image:
                         image_path =  os.path.join(patient_images_path,patient_image)
                         image_info = get_info(image_path)
                         
                         print("Processing: ", image_path)
                         image_info_df = pd.DataFrame({"Patient":patient,
                                                  "File_name":patient_image,
                                                  "Origin_X":image_info['Origin'][0], 
                                                  "Origin_Y":image_info['Origin'][1],
                                                  "Origin_Z":image_info['Origin'][2],
                                                  "Size_X":image_info['Size'][0],
                                                  "Size_Y":image_info['Size'][1],
                                                  "Size_Z":image_info['Size'][2],
                                                  "Spacing_X":image_info['Spacing'][0],
                                                  "Spacing_Y":image_info['Spacing'][1],
                                                  "Spacing_Z":image_info['Spacing'][2],}, index = [0]) 
                         image_info_df_list.append(image_info_df)
                         
        image_info_df_merged =  pd.concat(image_info_df_list)  
        image_info_df_merged.index = range(0,len(image_info_df_merged),1) 
        
        return image_info_df_merged
    
    @staticmethod
    def get_all(prostate_path):
        
        '''
        Export an excel file containing all the necessary information about the GraSe and T2TSE files of all patient.        
        
        Parameters
        ----------
        prostate_path : String
            Path the folder containing all the patient files.


        Returns
        -------
        None.

        '''
        T2TSE_info = pickT2TSEFile.get_T2TSE_info(prostate_path)
        GraSe_info = pickT2TSEFile.get_GraSe_info(prostate_path)
        
        with pd.ExcelWriter( os.path.join(prostate_path,"T2TSE_GraSe.xlsx") ) as writer:
            T2TSE_info.to_excel(writer, sheet_name = "T2TSE_info")
            GraSe_info.to_excel(writer, sheet_name = "GraSe_info")
            
        
        
        


                            
                            
                            
                

#Calling

# gg = pickT2TSEFile.get_T2LO_prefix(prostate_path= r"D:\Uniklinik\Prostate")

# getsome = pickT2TSEFile.get_T2TSE_info(prostate_path= r"D:\Uniklinik\Prostate")


# get_grase = pickT2TSEFile.get_GraSe_info(prostate_path= r"D:\Uniklinik\Prostate")


# getall = pickT2TSEFile.get_all(prostate_path= r"D:\Uniklinik\Prostate")

        
        
        
        
        