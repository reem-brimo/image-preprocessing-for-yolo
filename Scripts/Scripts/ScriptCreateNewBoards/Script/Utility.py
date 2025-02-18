import os
import cv2
from PIL import Image
import numpy as np
import random
from collections import defaultdict
import csv
import yaml


def set_classes_names(folders, output_path):
    indexes = []
    values = []

    class_path = os.path.join(output_path,"DataFiles", "classes.txt")
    for folder in folders:
        index, name = get_main_class_name_index(folder)
        indexes.append(index)
        values.append(name)

    indexes = np.array(indexes)
    values = np.array(values)

    data = np.column_stack((indexes, values))

    np.savetxt(class_path, data, fmt='%s')
    
    return class_path, len(folders)

def create_yaml(class_path, output_path, len_classes):
    yaml_path = os.path.join(output_path, "DataFiles","yolo_config.yaml")
    data = {
        "path":"./",
        "train": "./train/images",
        "val": "./val/images",
        "nc": len_classes,
        "names": [],
    }

    saved_classes = np.loadtxt(class_path, dtype=str)

    loaded_names = saved_classes[:, 1].tolist()

    data["names"] = loaded_names
    data["names"] =  [str(name) for name in data["names"]]

    yaml_content = yaml.dump(data, sort_keys=False)

    # Write the YAML content to a file
    with open(yaml_path, "w") as file:
        file.write(yaml_content)

def get_image_name(path):
    _, background_image_name = os.path.split(path)
    background_image_name, _ = os.path.splitext(background_image_name)
    
    split_text = background_image_name.split("_")
    background_image_name = "_".join(split_text[:-1])
    
    return background_image_name

def get_main_class_name_index(path):
    _, dir_name = os.path.split(path)
    index, name = dir_name.split("_")
    index = int(index[1:]) - 1
    name = name.upper()
     
    return index, name

def get_dir_name_from_img(path):
    dir_name, _ = os.path.split(path)
    index, name = get_main_class_name_index(dir_name)

    return index, name

def remove_color(color, img):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    color_val = 0
    sv = 100
    if color == "green":
     color_val = 60
     sv = 60
    else:
     color_val = 120


    lower_color = np.array([color_val - 30, sv, sv]) 
    upper_color = np.array([color_val + 30, 255, 255])

    #place 255
    mask =  cv2.inRange(hsv_image, lower_color, upper_color)

    mask = cv2.bitwise_not(mask)

    # Replace the green pixels with white pixels
    res = cv2.bitwise_and(img,img, mask= mask)

    # get (i, j) positions of all RGB pixels that are black (i.e. [0, 0, 0])
    black_pixels = np.where(
        (res[:, :, 0] == 0) & 
        (res[:, :, 1] == 0) & 
        (res[:, :, 2] == 0)
    )

    # set those pixels to white
    res[black_pixels] = [255, 255, 255]
    return res

def image_preprocessing(image_path):
    
    #resize
    img = cv2.imread(image_path)

    height, width, _ = img.shape

    # Determine the new size to maintain the aspect ratio
    if width > height:
        new_width = 60
        new_height = int(height * 60 / width)
    else:
        new_height = 60
        new_width = int(width * 60 / height)

    # Resize the image to the new size
    img = cv2.resize(img, (new_width, new_height))
    
    #remove any G or B colors
    res = remove_color("green",img)
    res = remove_color("blue",res)

    #rotate and paste
    img = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)

    # form cv2 to PIL
    im_pil = Image.fromarray(img)

    img = im_pil.convert('RGBA')

    # Rotate the image by 45 degrees
    #top_image = img.rotate(random.randint(0,360), expand=1)


    # Generate a random number between 0 and 3 to determine the direction of rotation
    direction = random.randint(0, 2)

    # Rotate the image by 90 degrees in the specified direction
    if direction == 0:
        # Rotate clockwise
        top_image = img.rotate(random.randint(0,360), expand=1)
    elif direction == 1:
        # Rotate counterclockwise
        top_image = img.transpose(method=Image.ROTATE_90)
    elif direction == 2:
        # Rotate 180 degrees
        top_image = img.transpose(method=Image.ROTATE_180)
  


    #make transparent after rotation
    datas = top_image.getdata()

    newImage = []
    for item in datas:
      if item[:3] == (255, 255, 255):
            newImage.append((255, 255, 255, 0))
      else:
            newImage.append(item)

    top_image.putdata(newImage)

    return top_image

def get_board_coordinates(image):

    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the bounding box of the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    return cv2.boundingRect(largest_contour)

def get_subclass_num(name):
    name = name.split("_")
    c_name = name[0]
    c_name = c_name[1:]
    return c_name

def get_csv(file_path):

    if os.path.isfile(file_path):  # Check if the file exists
            file = open(file_path, 'r', newline='')
            csv_reader = csv.reader(file)
            next(csv_reader)
            return csv_reader
    else:
            print(f"no file '{file_path}' creating a new one.")
            return csv.reader([])  # Return an empty reader
      
def get_old_counts(file_path):
    name_counts = defaultdict(int)
    name_file_counts = defaultdict(int)

    csv_file = get_csv(file_path)

    for row in csv_file:
        if len(row) == 3 or len(row) == 2:  # Check if row has expected number of columns
            name = row[0]
            count = int(row[1])
            name_counts[name] = count
            #it is sub class count
            if len(row) == 3 :
                file_count = int(row[2])
                name_file_counts[name] = file_count

    return name_counts, name_file_counts

def sort_csv(csv_data):
     # Sort the main_csv_data based on the first column
    sorted_csv_data = sorted(csv_data[1:], key=lambda x: x[0])
    csv_data = [csv_data[0]] + sorted_csv_data

    return csv_data


def sort_int_csv(csv_data):
     # Sort the main_csv_data based on the first column
    sorted_csv_data = sorted(csv_data[1:], key=lambda x: int(x[0]))
    csv_data = [csv_data[0]] + sorted_csv_data

    return csv_data

def save_csv(file_path, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)