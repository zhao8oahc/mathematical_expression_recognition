#-*- encoding: utf-8 -*-

import os
#import cv2
import pandas as pd
import numpy as np
import random
import string
import matplotlib.pyplot as plt

from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
#from captcha.image import ImageCaptcha
#from PIL import Image


csv_path = 'data/train.csv'
df_label = pd.read_csv(csv_path, index_col=0)

characters = string.digits + '+-*=()'

#im = array(Image.open('').convert('L'),'f')

#def data(self, dir='Data/train_dir/train', ):
#	def __init__():
#
#
#	def 
