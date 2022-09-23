import zipfile
import os

def unzip(zip_file_dir, extract_file_dir):
    """Unzips files from the folder"""
    with zipfile.ZipFile(zip_file_dir, "r") as zip_ref:
        return zip_ref.extractall(extract_file_dir)

def unzip_all_folders(dir_path="data/DOC/EPNWA1", target_path= "data/DOC/EPNWA1"):
    for file in os.listdir(dir_path):
        if file.endswith(".zip"):
            extract_folder = f"{target_path}/{file.replace('.zip', '')}"
            os.mkdir(extract_folder)
            unzip(f"{dir_path}/{file}", extract_folder)            
    pass


unzip_all_folders("data/DOC/EPNWA1", "epo/samples"),