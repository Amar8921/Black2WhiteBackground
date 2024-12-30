import argparse
import os
from PIL import Image

def has_black_color(image_path):
    """Check if black color exists in the corner pixels of the image."""
    # Open the image
    img = Image.open(image_path)
    # Ensure the image is in RGB mode
    img = img.convert("RGB")

    # Get dimensions
    width, height = img.size

    # Get pixel colors from the corners
    corners = [
        img.getpixel((0, 0)),           # Top-left
        img.getpixel((width - 1, 0)),  # Top-right
        img.getpixel((0, height - 1)), # Bottom-left
        img.getpixel((width - 1, height - 1)) # Bottom-right
    ]

    # Check if any corner contains black (RGB: (0, 0, 0))
    return (0, 0, 0) in corners

def process_images(input_folder, output_folder):
    """Process all images in the input folder and save those with black corners to the output folder."""
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        # Get full file path
        file_path = os.path.join(input_folder, filename)

        # Skip if not an image file
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        try:
            # Check if the image has black corners
            if has_black_color(file_path):
                # Save the image to the output folder
                img = Image.open(file_path)
                output_path = os.path.join(output_folder, filename)
                img.save(output_path)
                print(f"Saved: {output_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Detect black corner pixels in images from a folder and save matching images to another folder.")
    parser.add_argument("input_folder", help="Path to the folder containing images")
    parser.add_argument("output_folder", help="Path to the folder to save images with black corners")

    # Parse arguments
    args = parser.parse_args()

    # Process the images
    process_images(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()
