import os
from PIL import Image
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