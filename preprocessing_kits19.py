# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:05:17 2020

@author: michaely
"""

import sys
sys.path.append(r"C:\Users\michaely\Documents\hiwi\Scripts")
from preprocessing_window import preprocessing_window



preprocessing_window(root_path =  r"C:\Users\michaely\Documents\hiwi\kits19\data", 
                     root_output_path = r"C:\Users\michaely\Documents\hiwi\kits19\mean0std1", 
                     threshold= -900)

