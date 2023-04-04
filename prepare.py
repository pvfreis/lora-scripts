import os
import glob
import cv2
import numpy as np
from PIL import Image
from mtcnn import MTCNN

detector = MTCNN()

# get all the files in a folder, make sure all are image files
files = glob.glob('./input/*')

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
            
            # Crop the image to the face
            cropped_img_cv = img_cv[y:y+height, x:x+width]
            
            # Convert the cropped OpenCV image back to PIL format
            cropped_img = Image.fromarray(cv2.cvtColor(cropped_img_cv, cv2.COLOR_BGR2RGB))
            
            # Save the cropped image without resizing, modify the output directory as needed
            cropped_img.save(f"./input/key/{basename}.png", format="PNG")
        else:
            print(f"No face detected in {fil}")
