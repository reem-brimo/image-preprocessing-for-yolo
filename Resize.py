import os
import cv2

from tkinter import filedialog

print("Select Foreground images folder")
folder_path = filedialog.askdirectory() # show file explorer and return folder path
imagesName = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if  f.endswith(".jpg") or f.endswith(".png") ]
print(len(imagesName))
i=0
output_path = "../Desktop"
for image_path in imagesName:
    try:
        i+=1
        # load the image to be placed on top of the background
        top_image = cv2.imread(image_path)
        if top_image is not None:
            name = os.path.basename(image_path)
            top_image = cv2.resize(top_image, (640, 640))
            cv2.imwrite(f"{name}",top_image)  
    except:
        print(image_path)