import os
import cv2
from PIL import Image
import numpy as np
import random
from collections import defaultdict
import csv
import yaml
import pandas as pd

df = pd.read_csv('../../data.csv', encoding='iso-8859-1')
df['number'] = df['sub_class'].str.extract('(\d+)').astype(int)

def get_main_class(number):
    filtered_df = df[df['number'] == number]
    if not filtered_df.empty:  # Check if the DataFrame is not empty
        return filtered_df['main_class'].values[0]
    else:
        return None

def get_csv(file_path):

    if os.path.isfile(file_path):  # Check if the file exists
            file = open(file_path, 'r', newline='')
            csv_reader = csv.reader(file)
            next(csv_reader)
            return csv_reader
    else:
            print(f"no file '{file_path}' creating a new one.")
            return csv.reader([])  # Return an empty reader

def get_subclass_num(name):
    name = name.split("_")
    c_name = name[0]
    c_name = c_name[1:]
    return c_name

def sort_csv(csv_data):
     # Sort the csv_data based on the first column
    sorted_csv_data = sorted(csv_data[1:], key=lambda x: x[0])

    csv_data = [csv_data[0]] + sorted_csv_data

    return csv_data

def save_csv(file_path, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)