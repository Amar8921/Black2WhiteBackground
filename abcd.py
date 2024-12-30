import os
from PIL import Image
import pyodbc
import io
from rembg import remove

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

    return (0, 0, 0) in corners

def fetch_matching_barcodes(folder_names):
    """Fetch barcodes using the custom query and match with folder names."""
    connection_string = (
        "DRIVER={SQL Server};"
        "SERVER=FOODWORLD\\SQLEXPRESS;"
        "DATABASE=foodworld;"
        "UID=skienuser;"
        "PWD=skiendberp@123;"
    )
    matching_results = []

    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            query = """
                SELECT 
                    sku.BarCode,
                    CASE 
                        WHEN CHARINDEX('/', img.ImageFile) > 0 AND CHARINDEX('\\', img.ImageFile) > 0 THEN 
                            LEFT(img.ImageFile, 
                                 CASE 
                                     WHEN CHARINDEX('/', img.ImageFile) < CHARINDEX('\\', img.ImageFile) THEN CHARINDEX('/', img.ImageFile) - 1
                                     ELSE CHARINDEX('\\', img.ImageFile) - 1
                                 END)
                        WHEN CHARINDEX('/', img.ImageFile) > 0 THEN 
                            LEFT(img.ImageFile, CHARINDEX('/', img.ImageFile) - 1)
                        WHEN CHARINDEX('\\', img.ImageFile) > 0 THEN 
                            LEFT(img.ImageFile, CHARINDEX('\\', img.ImageFile) - 1)
                        ELSE 
                            img.ImageFile
                    END AS ExtractedNumber
                FROM 
                    catalog.ProductImageMaps img
                LEFT JOIN 
                    catalog.ProductSKUMaps sku 
                ON 
                    sku.ProductSKUMapIID = img.ProductSKUMapID
                WHERE 
                    ProductImageTypeID = 8
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Create a dictionary of extracted numbers to barcodes
            barcode_map = {str(row.ExtractedNumber): row.BarCode for row in results if row.BarCode is not None}
            
            # Match folder names with extracted numbers and get corresponding barcodes
            for folder_name in folder_names:
                if folder_name in barcode_map:
                    matching_results.append((folder_name, barcode_map[folder_name]))
                    print(f"Found match: Folder {folder_name} -> Barcode {barcode_map[folder_name]}")

    except Exception as e:
        print(f"Error fetching barcodes: {e}")

    return matching_results

def remove_background_and_save(image_path, output_path):
    """Remove the background from the image and save it to the specified path."""
    try:
        with open(image_path, 'rb') as input_file:
            image_data = remove(input_file.read())
            with Image.open(io.BytesIO(image_data)) as img:
                # Convert transparent pixels to white
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, (0, 0), img.convert('RGBA'))
                background.save(output_path, 'JPEG')
        print(f"Background removed and saved: {output_path}")
    except Exception as e:
        print(f"Error removing background from {image_path}: {e}")

def process_images(input_folder, output_folder, bg_removed_folder):
    """Process images and save matching barcodes."""
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(bg_removed_folder, exist_ok=True)

    # File to store names of folders containing images with black corners
    folder_txt_file_path = os.path.join(output_folder, "black_corner_folders.txt")
    barcode_txt_file_path = os.path.join(output_folder, "matching_barcodes.txt")
    processed_folders = set()
    folder_to_images = {}  # Dictionary to store folder -> image filename mapping

    # First pass: collect all images with black corners and their folder names
    with open(folder_txt_file_path, "w") as folder_txt_file:
        for root, dirs, files in os.walk(input_folder):
            if "ListingImage" in root:
                folder_name = os.path.basename(os.path.dirname(root))
                for filename in files:
                    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                        continue

                    file_path = os.path.join(root, filename)
                    try:
                        if has_black_color(file_path):
                            # Save original image
                            img = Image.open(file_path)
                            output_path = os.path.join(output_folder, filename)
                            img.save(output_path)
                            print(f"Saved image with black corners: {output_path}")

                            # Store the mapping of folder to image filename
                            folder_to_images[folder_name] = file_path

                            # Write the folder name if not already written
                            if folder_name not in processed_folders:
                                folder_txt_file.write(folder_name + "\n")
                                processed_folders.add(folder_name)
                                print(f"Found black corners in folder: {folder_name}")
                            break
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")

    print(f"Folder names saved in: {folder_txt_file_path}")

    # Second pass: get barcodes and process background removal
    matching_results = fetch_matching_barcodes(processed_folders)
    with open(barcode_txt_file_path, "w") as barcode_txt_file:
        for folder_name, barcode in matching_results:
            barcode_txt_file.write(f"{barcode}\n")
            print(f"Saved barcode for folder {folder_name}: {barcode}")

            # Get the corresponding image path and process it
            if folder_name in folder_to_images:
                original_image_path = folder_to_images[folder_name]
                # Save with barcode as filename
                file_extension = os.path.splitext(original_image_path)[1]
                bg_output_path = os.path.join(bg_removed_folder, f"{barcode}{file_extension}")
                remove_background_and_save(original_image_path, bg_output_path)

    print(f"Matching barcodes saved in: {barcode_txt_file_path}")
    print(f"Background-removed images saved in: {bg_removed_folder}")

def main():
    print("Detect black corner pixels, find matching barcodes, and remove backgrounds.")
    input_folder = input("Enter the path to the input folder: ").strip()
    output_folder = input("Enter the path to the output folder: ").strip()
    bg_removed_folder = input("Enter the path to save background-removed images: ").strip()

    if not os.path.isdir(input_folder):
        print(f"The input folder '{input_folder}' does not exist.")
        return

    process_images(input_folder, output_folder, bg_removed_folder)

if __name__ == "__main__":
    main()