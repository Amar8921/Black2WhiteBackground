from rembg import remove
from PIL import Image
import os
import io
import numpy as np

def is_background_black(image):
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Get the corners of the image
    corners = [
        img_array[0, 0],
        img_array[0, -1],
        img_array[-1, 0],
        img_array[-1, -1]
    ]
    
    # Check if corners are black (RGB values close to 0)
    threshold = 30  # Allowing some variation in black
    return all(np.all(corner < threshold) for corner in corners)

def process_image(image_path):
    try:
        # Open and process image
        with open(image_path, 'rb') as input_file:
            # First check if the image has a black background
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                if is_background_black(img):
                    # Remove background and convert to white
                    image_data = remove(input_file.read())
                    with Image.open(io.BytesIO(image_data)) as processed_img:
                        # Convert transparent pixels to white
                        background = Image.new('RGB', processed_img.size, (255, 255, 255))
                        background.paste(processed_img, (0, 0), processed_img.convert('RGBA'))
                        # Save back to the same location
                        background.save(image_path, 'JPEG', quality=95)
                        print(f"Processed (black background removed): {image_path}")
                else:
                    print(f"Skipped (no black background): {image_path}")
                    
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def process_products_folder(main_folder):
    # Walk through all subdirectories
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, file)
                process_image(image_path)

if __name__ == '__main__':
    # Ask user for the main products folder path
    products_folder = input("Enter the main products folder path: ").strip()

    # Check if folder exists
    if not os.path.exists(products_folder):
        print(f"Error: Folder '{products_folder}' does not exist.")
    else:
        print("Processing images... This may take a while.")
        process_products_folder(products_folder)
        print("Processing complete!")