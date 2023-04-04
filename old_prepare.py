import os
import glob
from PIL import Image
import face_recognition

size = (512, 512)

# get all the files in a folder, make sure all are image files
files = glob.glob('./training_data/raw/*')

def crop_center_face(image, face_locations):
    if len(face_locations) > 0:
        top, right, bottom, left = face_locations[0]
        face_center_x = (left + right) // 2
        face_center_y = (top + bottom) // 2

        half_crop_size = min(size) // 2
        new_left = max(0, face_center_x - half_crop_size)
        new_right = new_left + size[0]
        new_top = max(0, face_center_y - half_crop_size)
        new_bottom = new_top + size[1]

        if new_right > image.width:
            new_right = image.width
            new_left = new_right - size[0]

        if new_bottom > image.height:
            new_bottom = image.height
            new_top = new_bottom - size[1]

        return image.crop((new_left, new_top, new_right, new_bottom))

    return image.resize(size)

for fil in files:
    # get the basename, e.g. "dragon.jpg" -> ("dragon", ".jpg")
    basename = os.path.splitext(os.path.basename(fil))[0]

    with Image.open(fil) as img:
        # detect faces
        face_locations = face_recognition.face_locations(img)

        # crop and center the image around the first detected face
        centered_img = crop_center_face(img, face_locations)
        
        # save the centered image
        centered_img.save(f"./training_data/key/{basename}.png", format="PNG", resample=Image.Resampling.NEAREST)
