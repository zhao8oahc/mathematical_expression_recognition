#-*- encoding: utf-8 -*-

import os
#import cv2
import pandas as pd
import numpy as np
import random
import string

from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from captcha.image import ImageCaptcha
from PIL import Image


csv_path = 'data/train/train.csv'
df_label = pd.read_csv(csv_path, index_col=0)

characters = string.digits + '+-*=()'

#class dataset(object):

	#def __init__(self,)




#history = model.fit_generator(
#	gen_data(), 
#	steps_per_epoch = 100000/50, 
#	epochs=400,
#	validation_data = valid_data.get_batch(),
#	validation_steps = int(0.3*100000/50),
#	callbacks=[ReduceLROnPlateau('loss', cooldown=1),
#	ModelCheckpoint('../model/model_gru_best.h5', save_best_only=True)])