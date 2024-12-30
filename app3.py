import numpy as np
from PIL import Image
from rembg import remove
import os

def change_background_to_white(input_path, output_path):
    """
    Remove the background of an image and replace it with white
    
    Parameters:
    input_path (str): Path to input image
    output_path (str): Path where the processed image will be saved
    """
    # Open the image
    input_image = Image.open(input_path)
    
    # Remove the background
    output = remove(input_image)
    
    # Create a white background image of the same size
    white_background = Image.new('RGBA', output.size, (255, 255, 255, 255))
    
    # Composite the image onto the white background
    white_background.paste(output, (0, 0), output)
    
    # Convert to RGB (removing alpha channel) and save
    final_image = white_background.convert('RGB')
    final_image.save(output_path)

# Example usage
if __name__ == "__main__":
    input_image_path = "input/blu.jpg"  # Replace with your input image path
    output_image_path = "output.jpg"  # Replace with desired output path
    
    change_background_to_white(input_image_path, output_image_path)