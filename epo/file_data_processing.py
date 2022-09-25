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