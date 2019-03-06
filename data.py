#-*- encoding: utf-8 -*-

import os
#import cv2
import pandas as pd
import numpy as np
import random
import string

from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
#from captcha.image import ImageCaptcha
#from PIL import Image


csv_path = 'train/train.csv'
df_label = pd.read_csv(csv_path, index_col=0)

characters = string.digits + '+-*=()'

def gen_captcha(batch_size = 50):
    X = np.zeros([batch_size,height,width,1])
    img = np.zeros((height,width),dtype=np.uint8)
    Y = np.zeros([batch_size,n_len,n_class])
    image = generator

    while True:
        for i in range(batch_size):
            captcha_str = ''.join(random.sample(characters,n_len))
            img = image.generate_image(captcha_str).convert('L')
            img.save('D:\Full_Stack\mathematical_expression_recognition\data',captcha_str + '.jpg')
            img = np.array(img.getdata())
            X[i] = np.reshape(img,[height,width,1])/255.0
            for j,ch in enumerate(captcha_str):
                Y[i,j,characters.find(ch)] = 1
        Y = np.reshape(Y,(batch_size,n_len*n_class))
        yield X,Y