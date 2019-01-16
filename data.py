#-*- encoding: utf-8 -*-

from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
import osimport cv2
from captcha.image import ImageCaptcha
import matplotlib.pyplot as plt
import numpy as np
import random
from PIL import Image


csv_path = 'Data/train.csv'

im = array(Image.open('').convert('L'),'f')