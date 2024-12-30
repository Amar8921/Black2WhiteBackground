import argparse
from PIL import Image

def get_corner_colors(image_path):
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

    # Return the most common color among the corners
    return max(set(corners), key=corners.count)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Detect the background color of an image based on corner pixels.")
    parser.add_argument("image_path", help="Path to the image file")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Get the background color from the image
    background_color = get_corner_colors(args.image_path)
    
    # Print the result
    print("Background color:", background_color)

if __name__ == "__main__":
    main()
