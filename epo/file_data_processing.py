import zipfile
import os
from PIL import Image
from tqdm import tqdm

# Unzipping functions

def unzip(zip_file_dir, extract_file_dir):
    """Unzips files from the folder into a folder (does not create new folder)"""
    with zipfile.ZipFile(zip_file_dir, "r") as zip_ref:
        return zip_ref.extractall(extract_file_dir)

def unzip_all_folders(input_dir_path="data/DOC/EPNWA1", output_dir_path= "data/DOC/EPNWA1", limit=99999):
    """Unzips all zip folders in a given folder and removes limit if need be"""
    for i, file in enumerate(os.listdir(input_dir_path)):
        if file.endswith(".zip"):
            extract_folder = f"{output_dir_path}/{file.replace('.zip', '')}"
            os.mkdir(extract_folder)
            unzip(f"{input_dir_path}/{file}", extract_folder)
        if i == limit: break

def unzip_all_subfolders(input_dir_path="data/DOC", output_dir_path="data/DOC-UNPACKED"):
    """Unzips the entire DOC file package into a new folder"""
    for folder in tqdm(os.listdir(input_dir_path)):
        os.mkdir(f"{output_dir_path}/{folder}")
        unzip_all_folders(input_dir_path=f"{input_dir_path}/{folder}", output_dir_path= f"{output_dir_path}/{folder}", limit=99999)


# Image Conversions

def convert_tiff_to_png(tiff_import_path='image.tif', png_export_path="image.png"):
    """Converts image using the PILLOW library from tif to png"""
    image = Image.open(tiff_import_path)
    return image.save(png_export_path, format="png")

def convert_subfolder_images(input_dir_path="epo/samples/full-text", output_dir_path="static/img/patent_images"):
    """Converts all the images in a directory which contains a folders that in turn contain tif images"""
    for folder in os.listdir(input_dir_path):
        for file in os.listdir(f'{input_dir_path}/{folder}'):
            if file.endswith('.tif'):
                if file.startswith('imgf'):
                    convert_tiff_to_png(f'{input_dir_path}/{folder}/{file}', f'{output_dir_path}/{file.replace(".tif", "")}{folder}.png')