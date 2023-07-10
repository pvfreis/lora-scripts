import json
import requests
import io
import base64
import time
import os
from PIL import Image, PngImagePlugin
import subprocess

url = "http://127.0.0.1:7861"


def read_prompts_from_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


json_file_path = os.path.join(os.getcwd(), "prompts.json")

prompts = read_prompts_from_json(json_file_path)

# Create a timestamped folder
timestamp = time.strftime("%d-%m-%Y-%H-%M")
folder_name = os.path.join("out", timestamp)
folder_path = os.path.join(os.getcwd(), folder_name)
os.makedirs(folder_path, exist_ok=True)

# Print the current working directory
print(f"Current working directory: {os.getcwd()}")
print(f"Saving images in folder: {folder_path}")    # Print the folder path
start_time = None

for index, prompt in enumerate(prompts):
    payload = {
        "prompt": prompt,
        "negative_prompt": "photo, photography, photograph, DSLR, ((((ugly)))), (((duplicate))), ((morbid)), ((mutilated)), [out of frame], extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((ugly)), blurry, ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, (((disfigured))), out of frame, ugly, extra limbs, (bad anatomy), gross proportions, (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), mutated hands, (fused fingers), (too many fingers), (((long neck)))",
        "steps": 36,
        "sampler_index": 'DPM++ 2M Karras',
        "seed": -1,
    }

    highres_payload = {
        "enable_hr": True,
        "hr_upscaler": "Latent",
        "hr_scale": 1,
        "hr_second_pass_steps": 16,
        "denoising_strength": 0.6,
    }
    payload.update(highres_payload)

    while True:
        try:
            response = requests.post(
                url=f'{url}/sdapi/v1/txt2img', json=payload)
            response.raise_for_status()
            if start_time is None:
                start_time = time.time()
            break
        except requests.exceptions.RequestException as e:
            print(f"Service not available yet: Trying again in 10 seconds.")
            time.sleep(10)  # Wait for 5 seconds before retrying

    r = response.json()

    for i, img_data in enumerate(r['images']):
        image = Image.open(io.BytesIO(
            base64.b64decode(img_data.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + img_data
        }
        response2 = requests.post(
            url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))

        # Save the images with different filenames in the timestamped folder
        image_filename = os.path.join(folder_path, f"{prompt}_{index}_{i}.png")
        image.save(image_filename, pnginfo=pnginfo)


# Set source and dest path for info.json
json_source_path = "/home/ubuntu/sky_workdir/lora-scripts/input/lrao/80_lrao/info.json"
json_dest_path = os.path.join(folder_path, "info.json")
# Execute the cp command
subprocess.run(["cp", json_source_path, json_dest_path], check=True)

print(f"info.json copied to: {json_dest_path}")


end_time = time.time()  # End time
elapsed_time = end_time - start_time  # Calculate elapsed time
# Print the elapsed time
print(f"Time taken for inference of all images: {elapsed_time:.2f} seconds")
