import pandas as pd

df = pd.read_csv('../../data.csv', encoding='iso-8859-1')
df['number'] = df['sub_class'].str.extract('(\d+)').astype(int)

def get_main_class(number):
    filtered_df = df[df['number'] == number]
    if not filtered_df.empty:
        return filtered_df['main_class'].values[0]
    else:
        return None

def get_subclass_num(name):
    name = name.split("_")
    c_name = name[0]
    c_name = c_name[1:]
    return c_name

def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]


def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]
