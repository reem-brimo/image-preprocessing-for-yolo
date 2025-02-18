
import os
import random
from PIL import Image
import random
import sys
import Utility;

output_path = "../Data/Output"

sub_csv_file =  os.path.join(output_path, 'DataFiles' ,'sub_tag_count.csv')
sub_csv_data = [['Name', 'Count', 'Num_Boards']]

main_csv_file = os.path.join(output_path, 'DataFiles','main_tag_count.csv')
main_csv_data = [['main_class_Name', 'Count']]

main_name_count, _ = Utility.get_old_counts(main_csv_file)
name_counts, name_board_counts = Utility.get_old_counts(sub_csv_file)

back_folder_path = '../Data/Background'

folder_path = '../Data/Foreground'

forground_folders = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f != '.DS_Store']

classes_path,len_classes = Utility.set_classes_names(forground_folders, output_path)
Utility.create_yaml(classes_path, output_path, len_classes)

print("enter the number of boards to Generate")
num = input()
num = int (num)
for k in range(0,num):
    #name of items in image
    image_items = []

    # initialize the list of previously placed image positions
    prev_positions = []

    background_images = [os.path.join(back_folder_path, f) for f in os.listdir(back_folder_path) if f.endswith(".jpg") or f.endswith(".png") ]

    #choose random back image
    background_image_path = random.choice(background_images)

    background_image = Image.open(background_image_path)

    if background_image.mode == "P":
        background_image = background_image.convert('RGB')

    #add trasperent element
    if background_image.mode == "RGB":
        a_channel = Image.new('L', background_image.size, 255)   # 'L' 8-bit pixels, black and white
        background_image.putalpha(a_channel)

   #get board coordinates
    x = 0
    y = 0
    w,h = background_image.size
 
    #create new background image to set alpha channel
    final = Image.new("RGBA", background_image.size)
    final.paste(background_image, (0,0), background_image)

    #create anotation file
    annotation = open(os.path.join(output_path,f"{k}" + ".txt"),"w+")


    items_num =random.randint(30, 40)
    imagesName = []
    images = []
    for i in range(0,items_num):
        #choose random item
        main_class_name = random.choice(forground_folders)
        imagesName = [os.path.join(main_class_name, f) for f in os.listdir(main_class_name) if f.endswith(".jpg") or f.endswith(".png") or f.endswith("jpeg")]
        #if it is empty it will skip an item
        if imagesName != []:
            images.append(random.choice(imagesName))
        
    #print(images)
    # select a random image file from the list
    for image_path in images:
        class_num, class_name = Utility.get_dir_name_from_img(image_path)

        sub_class_name = Utility.get_image_name(image_path)
        
        top_image = Utility.image_preprocessing(image_path)
        #top_image = Image.open(image_path)
    
        # get the dimensions of the top image
        top_image_width, top_image_height = top_image.size
        background_image_width, background_image_height  = background_image.size

        placed = False

        start_y = h // 10
        end_y = h - (h // 10)
        start_x = w // 20
        end_x = w - (w // 50)
        padding = 25

        for j in range(start_y, end_y):
            if placed:
                    break
            if(j + top_image_height + padding <  end_y):
                 for i in range(start_x, end_x):
                     if(i + top_image_width + padding < end_x):
                        x1 = i
                        y1 = j

                        overlap = False
                        for prev_position in prev_positions:
                           if x1 + top_image_width > prev_position[0] - padding and prev_position[0] + prev_position[2] + padding > x1 and \
                           y1 < prev_position[1] + prev_position[3] + padding and y1 + top_image_height > prev_position[1] - padding:
                                overlap = True
                                break
                   
                        if overlap != True:
                            position = (x1, y1, top_image_width, top_image_height)

                            x1_norm, y1_norm = x1 / background_image_width, y1 / background_image_height

                            # Calculate end pixels in normalized form
                            x2_norm, y2_norm = (x1 + top_image_width) / background_image_width, (y1 + top_image_height) / background_image_height

                            # Bounding box for the top image
                            center_x, center_y = (x1_norm + x2_norm) / 2, (y1_norm + y2_norm) / 2

                            width, height = top_image_width / background_image_width, top_image_height / background_image_height

                            annotation.write(str(class_num) + " %.6f %.6f %.6f %.6f\n" %(center_x,center_y,width,height))
                            placed = True
                            break
                     else: 
                        break 
            else: 
                break

        if overlap != True:
            # place the top image onto the background image using the mask
            final.paste(top_image, box=(x1, y1, x1+top_image_width, y1+top_image_height), mask=top_image)

            # add the position of the placed image to the list of previously placed image positions
            prev_positions.append(position)

            #add to statistic 
            if sub_class_name not in image_items :
                image_items.append(sub_class_name)


            name_counts[sub_class_name] += 1
            main_name_count[class_num] += 1

    for item in image_items:
        name_board_counts[item] += 1

    annotation.close()

    # save the resulting image
    final.save(os.path.join(output_path ,f"{k}" + ".png"),"PNG")

#build csv
for name, count in name_counts.items():
        file_count = name_board_counts[name]
        sub_csv_data.append([name, count, file_count])

for name, count in main_name_count.items():
        main_csv_data.append([name, count])

sub_sorted_csv = Utility.sort_csv(sub_csv_data)
main_sorted_csv = Utility.sort_int_csv(main_csv_data)

Utility.save_csv(sub_csv_file, sub_sorted_csv)
Utility.save_csv(main_csv_file, main_sorted_csv)

