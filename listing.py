import os
from PIL import Image

def has_black_color(image_path):
    """Check if black color exists in the corner pixels of the image."""
    img = Image.open(image_path)
    img = img.convert("RGB")  # Ensure the image is in RGB mode

    width, height = img.size
    corners = [
        img.getpixel((0, 0)),           # Top-left
        img.getpixel((width - 1, 0)),  # Top-right
        img.getpixel((0, height - 1)), # Bottom-left
        img.getpixel((width - 1, height - 1)) # Bottom-right
    ]

    return (0, 0, 0) in corners  # Check if any corner contains black (RGB: (0, 0, 0))

def process_images(input_folder, output_folder):
    """Process images and save those with black corners directly to the output folder."""
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

    # File to store names of saved images
    txt_file_path = os.path.join(output_folder, "black_corner_images.txt")
    with open(txt_file_path, "w") as txt_file:
        for root, dirs, files in os.walk(input_folder):
            if "ListingImage" in root:  # Process only the 'ListingImage' subfolder
                for filename in files:
                    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):  # Skip non-image files
                        continue

                    file_path = os.path.join(root, filename)
                    try:
                        if has_black_color(file_path):  # Check if the image has black corners
                            # Save the image directly into the output folder
                            img = Image.open(file_path)
                            output_path = os.path.join(output_folder, filename)
                            img.save(output_path)

                            # Write the image name without extension to the text file
                            name_without_extension = os.path.splitext(filename)[0]
                            txt_file.write(name_without_extension + "\n")

                            print(f"Saved: {output_path}")
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")

    print(f"Image names saved in: {txt_file_path}")

def main():
    print("Detect black corner pixels in images and save matching images to a single folder.")
    input_folder = input("Enter the path to the input folder: ").strip()
    output_folder = input("Enter the path to the output folder: ").strip()

    if not os.path.isdir(input_folder):
        print(f"The input folder '{input_folder}' does not exist.")
        return

    process_images(input_folder, output_folder)

if __name__ == "__main__":
    main()
