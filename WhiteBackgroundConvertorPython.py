from rembg import remove
from PIL import Image
import os
import io


def remove_background(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)

            try:
                with open(input_path, 'rb') as input_file:
                    image_data = remove(input_file.read())
                    with Image.open(io.BytesIO(image_data)) as img:
                        # Convert transparent pixels to white
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, (0, 0), img.convert('RGBA'))
                        background.save(output_path, 'JPEG')

                print(f"Processed: {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

if __name__ == '__main__':
    # Ask the user for input and output folder paths
    input_folder = input("Enter the input folder path (default: './input'): ").strip() or './input'
    output_folder = input("Enter the output folder path (default: './output'): ").strip() or './output'

    # Check if input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
    else:
        remove_background(input_folder, output_folder)
