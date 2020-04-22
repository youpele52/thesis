# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 18:18:30 2020

@author: Youpele
"""



import gzip
import shutil
import os


def gunzip(file_path,output_path):
    with gzip.open(file_path,"rb") as f_in, open(output_path,"wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
     
        

gunzip(r"D:\Uniklinik\kits19\data\case_00002\imaging.nii.gz",
       r"D:\Uniklinik\kits19\data\case_00002\imaging.nii")



cases = os.listdir("D:/Uniklinik/kits19/data")
case_list = []
data_case_path = "D:/Uniklinik/kits19/data"

for case in cases:
    if case[0] == 'c':
        case =  data_case_path + '/' + case
        case_list.append(case)
        
        
        
        
# This zips the gz files         
for cases_ in case_list:
    case_temp =  os.listdir(cases_)

    for content in case_temp:
        if content =='imaging.nii.gz':
            content_path = cases_ + '/' + content
            content_path_new = content_path.strip('.gz')
            print('Image exist here\nThe path is ',content_path +
                  '\nAnd the adjusted path is ', content_path_new + '\n\n\n')
            gunzip(content_path, content_path_new)
            
            
            
            #print('Image exist here\n\nThe path is ', cases_ + '/' + content +'\n\n\n\n')
        if content == 'segmentation.nii.gz':
            content_path = cases_ + '/' + content
            content_path_new = content_path.strip('.gz') 
            print('Segmentation exist here\nThe path is ',content_path +
                  '\nAnd the adjusted path is ', content_path_new + '\n\n\n')
            gunzip(content_path, content_path_new)
        



# This interpolates
for cases_ in case_list:
    case_temp =  os.listdir(cases_)

    for content in case_temp:

        if content =='imaging.nii':
            content_path = cases_ + '/' + content
            case_folder = cases_ + '/'
            print('Image exist here\nThe path is ', cases_ + '/' + content)
            print('The image can be found in', case_folder + ' folder.\n\n\n')
                        
            resampled_sitk_img = resample_img(image_path = content_path, 
                                              out_image_path=case_folder,
                                              segmentation_or_image = "image",
                                              out_spacing=[3.0, 1.0, 1.0], is_label=False)
                     
            

        
        
        if content == 'segmentation.nii':
            content_path = cases_ + '/' + content
            case_folder = cases_ + '/'
            print('Segmentation exist here\nThe path is ', cases_ + '/' + content)
            print('The segmentation can be found in', case_folder + ' folder.\n\n\n')
            resampled_sitk_img = resample_img(image_path = content_path, 
                                  out_image_path=case_folder,
                                  segmentation_or_image = "segmentation",
                                  out_spacing=[3.0, 1.0, 1.0], is_label=True)




        if content =='imaging.nii':
            content_path = cases_ + '/' + content
            case_folder = cases_ + '/'
            print('Image exist here\nThe path is ', cases_ + '/' + content)
            print('The image can be found in', case_folder + ' folder.\n\n\n')
                        
            resampled_sitk_img = resample_img(image_path = content_path, 
                                              out_image_path=case_folder,
                                              segmentation_or_image = "image",
                                              out_spacing=[3.0, 1.0, 1.0], is_label=False)
                     
            
            
            
         
            

resampled_sitk_img = resample_img(image_path = image_path, 
                                  out_image_path=out_image_path,
                                  segmentation_or_image = "segmentation",
                                  out_spacing=[3.0, 1.0, 1.0], is_label=True)


            
            
            
            
            
            
            
            
            
            
aaa = r"D:\Uniklinik\kits19\data\case_00002\imaging.nii.gz"
aaa_mod = aaa.strip('.gz')            
case_mod = case.replace('2','')          
            