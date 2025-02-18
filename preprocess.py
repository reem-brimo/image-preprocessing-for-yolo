from tkinter import filedialog
import cv2
from PIL import Image
import random
import os
import Utilty



print("Select forground images folder")
folder_path = filedialog.askdirectory()
forground_folders = [os.path.join(folder_path, f) for f in os.listdir(folder_path)  if f != '.DS_Store']

imagesName = []
for path in forground_folders:
        #choose random item
        imagesName.append([os.path.join(path, f) for f in os.listdir(path) if f.endswith(".jpg") or f.endswith(".JPG") or f.endswith(".png") or f.endswith("jpeg")])
for image_path in imagesName:

    for path in image_path:

        #resize
        img = cv2.imread(str(path))

        height, width, _ = img.shape

            # Determine the new size to maintain the aspect ratio
        # if width > height:
        #         new_width = 60
        #         new_height = int(height * 60 / width)
        # else:
        #         new_height = 60
        #         new_width = int(width * 60 / height)

        #     # Resize the image to the new size
        # img = cv2.resize(img, (new_width, new_height))
    
        res = Utilty.remove_color("green",img)
        res = Utilty.remove_color("blue",res)

            #rotate and paste
        img = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)

            # form cv2 to PIL
        im_pil = Image.fromarray(img)

        top_image = im_pil.convert('RGBA')

            # Rotate the image by 45 degrees
        #top_image = img.rotate(random.randint(0,360), expand=1)


            ## Generate a random number between 0 and 3 to determine the direction of rotation
            #direction = random.randint(0, 2)

            ## Rotate the image by 90 degrees in the specified direction
            #if direction == 0:
            #    # Rotate clockwise
            #    top_image = img.transpose(method=Image.rot)
            #elif direction == 1:
            #    # Rotate counterclockwise
            #    top_image = img.transpose(method=Image.ROTATE_90)
            #elif direction == 2:
            #    # Rotate 180 degrees
            #    top_image = img.transpose(method=Image.ROTATE_180)
  


            #make transparent after rotation
        datas = top_image.getdata()

        newImage = []
        for item in datas:
              if item[:3] == (255, 255, 255):
                    newImage.append((255, 255, 255, 0))
              else:
                    newImage.append(item)

        top_image.putdata(newImage)
        path1, _ = os.path.splitext(path)
        print (path1)
        top_image.save(path1 + "edited.png")