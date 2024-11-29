import gdown
import py7zr
import os
import shutil

# Google Drive file ID and URL
file_id = '15DHbYtzI45YDWphtO49rGiQxQlBjtNvT'
url = f'https://drive.google.com/uc?id={file_id}'

# Paths
output = 'data.7z'
extract_path = 'extracted_data'
destination_dir = 'tiki_product_data'

# Download the file
print("Starting download...")
result = gdown.download(url, output, quiet=False)

# Verify download success
if not result or not os.path.exists(output):
    raise FileNotFoundError("Download failed or file not found.")

print(f"Downloaded file to {output}")

# Extract the .7z file
print("Extracting the .7z file...")
with py7zr.SevenZipFile(output, mode='r') as z:
    z.extractall(path=extract_path)
print("Extraction complete.")

# Move extracted directory
source_dir = os.path.join(extract_path, "tiki_product_data")

if os.path.exists(source_dir):
    try:
        shutil.copytree(source_dir, destination_dir)
        print(f"Copied tiki_product_data to {destination_dir}")
        shutil.rmtree(source_dir)
        print("Cleaned up source directory.")
    except Exception as e:
        print(f"Error during copy: {e}")
else:
    print("tiki_product_data not found in the extracted_data folder.")

# Cleanup
if os.path.exists(extract_path):
    shutil.rmtree(extract_path)
    print("Deleted 'extracted_data' folder.")

if os.path.exists(output):
    os.remove(output)
    print("Deleted 'data.7z' file.")
