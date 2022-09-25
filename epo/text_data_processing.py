import xml.etree.ElementTree as ET
import os
import json
from tqdm import tqdm


def open_xml_file(path="epo/samples/full-text/EP06818318NWB1/EP06818318NWB1.xml"):
    data = ET.parse(path).getroot()
    return data


def create_average_file():
    """Is able to generate fictional patent like data-structures"""
    pass


def create_max_file():
    """Renders the largest xml tree"""
    pass


def print_tree_with_tags(xml_data, max_level=8):
    for child_1 in xml_data:
        print(f'{child_1.tag}')
        for child_2 in child_1:
            print(f'\t#Child level 2: {child_2.tag}')
            for child_3 in child_2:
                print(f'\t\t#Child level 3: {child_3.tag}')
                for child_4 in child_3:
                    print(f'\t\t\t#Child level 4: {child_4.tag}')
                    for child_5 in child_4:
                        print(f'\t\t\t\t#Child level 5: {child_5.tag}')
                        for child_6 in child_5:
                            print(f'\t\t\t\t\t#Child level 6: {child_6.tag}')
                            for child_7 in child_6:
                                print(
                                    f'\t\t\t\t\t\t#Child level 7: {child_7.tag}')
                                for child_8 in child_7:
                                    print(
                                        f'\t\t\t\t\t\t\t#Child level 8: {child_8.tag}')
                                    for child_9 in child_8:
                                        print(
                                            f'\t\t\t\t\t\t\t\t#Child level 9: {child_9.tag}')
                                        for child_10 in child_9:
                                            print(
                                                f'\t\t\t\t\t\t\t\t\t#Child level 10: {child_10.tag}')


def retrieve_section_details(xml_data, patent_id):
    """Functions that returns the top level section names and their attributes. Returns in the form of array of dict. All in memory function"""
    details_dict = []
    for el in xml_data:
        attrib_dict = {attrib:value for attrib, value in el.attrib.items()}
        details_dict += [{"patent_no": patent_id, "id": xml_data.attrib['id'], "tag": el.tag, **attrib_dict}]
    return details_dict


def retrieve_all_section_details_folder(input_dir_path):
    combined_list = []
    for i, file in enumerate(os.listdir(input_dir_path)):
        if file.endswith(".xml") and not file.startswith('TOC.xml') and not file.startswith(".DS"):
            data = open_xml_file(f"{input_dir_path}/{file}")
            combined_list += retrieve_section_details(data, patent_id=input_dir_path.split('/')[-1])
    return combined_list

def create_section_summary(path="data/DOC-UNPACKED", export_path="section_summary.json"):
    data = []
    for batch in tqdm(os.listdir(path)):
        batch_level_data = []

        for patent in os.listdir(f"{path}/{batch}"):
            batch_level_data += retrieve_all_section_details_folder(
                f"{path}/{batch}/{patent}")

        data += batch_level_data

    with open(export_path, "w") as f:
        json.dump(data, f)
