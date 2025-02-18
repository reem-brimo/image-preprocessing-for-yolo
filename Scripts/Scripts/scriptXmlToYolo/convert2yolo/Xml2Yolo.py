import xml.etree.ElementTree as ET
import glob
import os
import Utility;


classes = []
input_dir = "../xml_lables"

output_dir = "./yolo_labels/"

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

files = glob.glob(os.path.join(input_dir, '*.xml'))
print(files)
for fil in files:
    
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]

    result = []
    tree = ET.parse(fil)
    root = tree.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)
    for obj in root.findall('object'):
        label = obj.find("name").text
        
        c_num = Utility.get_subclass_num(label)

        main_class_num = Utility.get_main_class(int(c_num))

        pil_bbox = [float(x.text) for x in obj.find("bndbox")]
        yolo_bbox = Utility.xml_to_yolo_bbox(pil_bbox, width, height)
        bbox_string = " ".join([str(x) for x in yolo_bbox])
        result.append(f"{main_class_num} {bbox_string}")

    if result:
        with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(result))