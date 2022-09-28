import xml.etree.ElementTree as ET
import os
import json
from tqdm import tqdm


def open_xml_file(path):
    """Opens an xml file and creates an in-memory copy in python"""
    data = ET.parse(path).getroot()
    return data


def print_tree_with_tags(
    xml_data: ET.Element,
    level: int = 0,
    max_level: int = 10,
):
    """Visualizes xml data of the tags in the terminal"""
    if level >= max_level:
        return
    tabs = "\t" * level
    print(f"{tabs} Child level {level}: {xml_data.tag}")
    for child in xml_data:
        print_tree_with_tags(child, level + 1, max_level)


def retrieve_section_details(xml_data, patent_id):
    """Functions that returns the top level section names and their attributes. Returns in the form of array of dict. All in memory function"""
    details_dict = []
    for el in xml_data:
        attrib_dict = {attrib: value for attrib, value in el.attrib.items()}
        details_dict += [
            {
                "patent_no": patent_id,
                "id": xml_data.attrib["id"],
                "tag": el.tag,
                **attrib_dict,
            }
        ]
    return details_dict


def retrieve_claim_text(xml_data):
    """Parses xml data to combine claims-text into a string to create dataset"""

    elements = []
    for claim_section in xml_data.findall("claims"):
        if claim_section.get("lang") != "en":
            continue
        # FIGURE OUT X CODE
        for claim in claim_section.findall("claim"):
            for claim_text in claim.findall("claim-text"):
                elements += [claim_text.text]

    return elements


def retrieve_title(xml_data):
    """Retrieves patent title from xml data"""
    ticker = False
    for element in xml_data.find("./SDOBI/B500/B540"):
        if ticker:
            return element.text
        if element.text == "en":
            ticker = True


def retrieve_classification_codes(xml_data):
    """Retrieves patent classification codes from xml data"""
    classification_list = []
    try:
        for classification in xml_data.find(
            "./SDOBI/B500/B520EP/classifications-cpc"
        ).findall("classification-cpc"):
            text_string = (
                classification.find("text")
                .text.replace("\t", " ")
                .replace("  ", " ")
                .replace("  ", " ")
                .replace("  ", " ")
                .replace("  ", " ")
            )
            if text_string[4] != " ":
                text_string = text_string[:4] + " " + text_string[4:]
            text_string = " ".join(text_string.split(" ")[:2])

            classification_list += [text_string]
    except:
        pass

    return classification_list


def retrieve_description(xml_data):
    """Retrieves description text from xml data. Separating each heading with two new lines '\n'\n and each paragraph with one new line '\n"""

    patent_description_string = ""
    if not xml_data.find("description"):
        return patent_description_string
    for element in xml_data.find("description"):
        if element.tag == "heading" and patent_description_string:
            patent_description_string += "\n\n"
        elif element.tag == "p" and patent_description_string:
            patent_description_string += "\n"

        if element.text:
            patent_description_string += element.text

    return patent_description_string


def build_all_claims_dataset(
    path,
    output_path="epo/data/ml_datasets/claims_dataset_with_titles_with_classes.json",
):
    """Build compelete full claim-text dataset"""
    dataset = []
    for batch in tqdm(os.listdir(path)):
        for patent_filing in os.listdir(f"{path}/{batch}"):
            if f"{patent_filing}.xml" in os.listdir(f"{path}/{batch}/{patent_filing}"):
                xml_data = open_xml_file(
                    f"{path}/{batch}/{patent_filing}/{patent_filing}.xml"
                )
                claim_array = retrieve_claim_text(xml_data)
                title = retrieve_title(xml_data)
                classification_list = retrieve_classification_codes(xml_data)
                patent_description_string = retrieve_description(xml_data)

                for claim in claim_array:
                    dataset += [
                        {
                            "patent_no": patent_filing,
                            "claim-text": claim,
                            "title": title,
                            "description_string": patent_description_string,
                            "classifications": classification_list,
                            "main_classification_symbol": classification_list[0][0]
                            if classification_list
                            else None,
                        }
                    ]

    with open(output_path, "w") as f:
        json.dump(dataset, f)


build_all_claims_dataset(
    "data/DOC-UNPACKED",
    output_path="epo/data/ml_datasets/claims_dataset_with_titles_with_classes_and_string_descriptions.json",
)


def retrieve_all_section_details_folder(input_dir_path):
    """Retrieves the section details in a given a patent folder by detecting which files to open"""
    combined_list = []
    for i, file in enumerate(os.listdir(input_dir_path)):
        if (
            file.endswith(".xml")
            and not file.startswith("TOC.xml")
            and not file.startswith(".DS")
        ):
            data = open_xml_file(f"{input_dir_path}/{file}")
            combined_list += retrieve_section_details(
                data, patent_id=input_dir_path.split("/")[-1]
            )
    return combined_list


def create_section_summary(
    path="data/DOC-UNPACKED", export_path="section_summary.json"
):
    """Retrieves the section details in a given batch of folders"""
    data = []
    for batch in tqdm(os.listdir(path)):
        batch_level_data = []

        for patent in os.listdir(f"{path}/{batch}"):
            batch_level_data += retrieve_all_section_details_folder(
                f"{path}/{batch}/{patent}"
            )

        data += batch_level_data

    with open(export_path, "w") as f:
        json.dump(data, f)
