import os
import cv2
from PIL import Image
import numpy as np
import random
from collections import defaultdict
import csv
import yaml
import pandas as pd

df = pd.read_csv('../data.csv', encoding='iso-8859-1')
df['number'] = df['sub_class'].str.extract('(\d+)').astype(int)

def get_main_class(number):
    filtered_df = df[df['number'] == number]
    if not filtered_df.empty:  # Check if the DataFrame is not empty
        return filtered_df['main_class'].values[0]
    else:
        return None

def get_subclasses_from_main(number):
    filtered_df = df[df['main_class'] == number]
    if not filtered_df.empty:  
        return filtered_df.iloc[:, [1, 2, 3]]
    else:
        return None

def get_image_name(path):
    _, name = os.path.split(path)
    name, _ = os.path.splitext(name)

    return name
