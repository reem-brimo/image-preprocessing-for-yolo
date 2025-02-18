import os
import xml.etree.ElementTree as ET
from collections import defaultdict
import Utility;

def count_name_tags(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    name_tags = root.findall('.//name')
    name_counts = defaultdict(int)

    for tag in name_tags:
        name_counts[tag.text] += 1
    
    return name_counts

def process_xml_files(folder_path, output_file):
    csv_data = [['Name', 'Count', 'Num_Boards']]  
    name_counts = defaultdict(int)
    name_board_counts = defaultdict(int)
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            counts = count_name_tags(file_path)
            for name, count in counts.items():
                name_counts[name] += count
                name_board_counts[name] += 1

    
    for name, count in name_counts.items():
        file_count = name_board_counts[name]
        csv_data.append([name, count, file_count])
    
    
    sorted_csv_data = Utility.sort_csv(csv_data)

    Utility.save_csv(output_file, sorted_csv_data) 
    
    print(f"Sub class Processing complete. Results stored in '{output_file}'.")

def count_main_classes(sub_count_path, output_path):
    
    main_csv_data = [['main_class_Name', 'Count']]
    main_counts = defaultdict(int)
    csv_file = Utility.get_csv(sub_count_path)

    for row in csv_file:
        if len(row) == 3:  # Check if row has expected number of columns
            name = row[0]
            c_num = Utility.get_subclass_num(name)
            main_class = Utility.get_main_class(int(c_num))
            main_counts[main_class] += int(row[1])
    
    for main_class, count in main_counts.items():
        main_csv_data.append([main_class, count])

    Utility.save_csv(output_path, main_csv_data)
    
    print(f"Main class count Processing complete. Results stored in '{output_path}'.")



# Example usage
#print("Select images folder")
folder_path = '../xml_lables'

sub_output_file = 'sub_tag_count.csv'
main_output_file = 'main_tags_count.csv'

process_xml_files(folder_path, sub_output_file)

count_main_classes(sub_output_file, main_output_file)