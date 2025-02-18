import SizeUtility;
from ultralytics import YOLO
import os
import torch

output_path = "./Output"
images_path = "./images"

images = [os.path.join(images_path, f) for f in os.listdir(images_path) if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg")]

for image in images:
    
    pixel_rate = float(input("Please enter a pixel rate value: "))

    #create result file
    image_name = SizeUtility.get_image_name(image)
    result_txt = open(os.path.join(output_path,f"{image_name}" + ".txt"),"w+")

    #use yolo to predict the item
    model = YOLO('./yoloModel/yolov8n.pt')

    results = model.predict(source=image)
    for result in results:
        # Get the class label and bounding box coordinates
        predicted_class = result.boxes.cls
        bounding_box = result.boxes.xyxy
        
        main_class = int(predicted_class.item())

        flattened_bounding_box =torch.flatten(bounding_box)
        
        # Calculate the width and height of the bounding box
        width = flattened_bounding_box[2].item() - flattened_bounding_box[0].item()
        height = flattened_bounding_box[3].item() - flattened_bounding_box[1].item()

        width_cloab = width * pixel_rate
        height_cloab = height * pixel_rate

        # Convert the dimensions to real-world measurements using the pixel rate
        yolo_space = width_cloab * height_cloab

        sub_class_name_and_size = SizeUtility.get_subclasses_from_main(main_class)
        sub_class_name_and_size = sub_class_name_and_size.reset_index(drop=True)

        print("sub classes and their sizes:\n")
        print(sub_class_name_and_size.to_string(index=False, header=True))
        
        #compare it to the spaces calculated from the file i have using eqludian distance
        distances = sub_class_name_and_size.apply(lambda row: abs(row['width'] * row['height'] - yolo_space), axis=1)

        # Get the index of the row with the smallest distance
        closest_index = distances.idxmin()

        # Get the closest object
        closest_object = sub_class_name_and_size.loc[closest_index]

        result_txt.write("Predicted main class " + str(main_class) + ", Claculated width and height %.6f %.6f \n" %(width_cloab, height_cloab))
        result_txt.write("Closest subclass: " +  closest_object['sub_class'] + ", Closest subclass width and height %.6f %.6f \n\n" %( closest_object['width'], closest_object['height']))
        
        result_txt.close()

