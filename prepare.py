import os
import glob
import cv2
import numpy as np
from PIL import Image
from mtcnn import MTCNN

detector = MTCNN()
size = (512, 512)

# get all the files in a folder, make sure all are image files
files = glob.glob('./input/raw*.jpg') + glob.glob('./input/raw/*.png') + glob.glob('./input/raw/*.jpeg')


for fil in files:
    basename = os.path.splitext(os.path.basename(fil))[0]

    with Image.open(fil) as img:
        # Convert the PIL image to OpenCV format
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Detect faces using MTCNN
        faces = detector.detect_faces(img_cv)
        
        if faces:
            # Use the first detected face (assuming there's only one face in the image)
            x, y, width, height = faces[0]['box']
            
            # Calculate the center of the face
            center_x = x + width // 2
            center_y = y + height // 2
            
            # Calculate the cropping coordinates
            half_size = 256
            left = max(0, center_x - half_size)
            top = max(0, center_y - half_size)
            right = min(img_cv.shape[1], center_x + half_size)
            bottom = min(img_cv.shape[0], center_y + half_size)
            
            # Crop the image to the face
            cropped_img_cv = img_cv[top:bottom, left:right]
            
            # Resize the cropped image to 512x512
            resized_img_cv = cv2.resize(cropped_img_cv, size)
            
            # Convert the resized OpenCV image back to PIL format
            resized_img = Image.fromarray(cv2.cvtColor(resized_img_cv, cv2.COLOR_BGR2RGB))
            
            # Save the resized image, modify the output directory as needed
            resized_img.save(f"./input/key/{basename}.png", format="PNG")
        else:
            print(f"No face detected in {fil}")
