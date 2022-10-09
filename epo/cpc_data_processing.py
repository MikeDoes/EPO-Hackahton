### Library that deals with the processing of CPC data from https://www.cooperativepatentclassification.org/cpcSchemeAndDefinitions/bulk ###
import csv
import xml.etree.cElementTree as ET


def open_tsv_file(path=""):
    """Opens TSV file"""
    table = []
    with open(path, newline='') as csvfile:
        file_reader = csv.reader(csvfile, delimiter='\t')
        for row in file_reader:
            table += [row]
    return table


def convert_cpc_standard_to_xml_tree(data):
    """Takes CPC standard data and converts it to the a in memory XML tree."""

    root = ET.Element('section', attrib={
        "code": data[0][0],
        "title": data[0][2],
    })

    # Assuming max depth of 20
    nested_list = 20*[None]

    for row in data[1:]:
        nested_index = int(row[1]) if row[1] != "" else 0
        if len(row[0]) == 3:
            # This is a main group
            main_group = ET.SubElement(root, 'main_group', attrib={
                "code": row[0],
                "title": row[2]
            })
        
        if len(row[0]) == 4:
            # This is a sub group
            sub_group = ET.SubElement(main_group, 'sub_group', attrib={
                "code": row[0],
                "title": row[2]
            })

        if len(row[0]) >= 4:
            if nested_index == 0:
                # This is a main class. Needs to be separate as it pretains to sub group not to a class
                main_class = ET.SubElement(sub_group, 'main_class', attrib={
                "code": row[0],
                "title": row[2]
                })
                nested_list[0] = main_class

            if nested_index > 0:
                # This is a sub group
                sub_class = ET.SubElement(nested_list[nested_index-1], f'sub_class_{row[1]}', attrib={
                    "code": row[0],
                    "title": row[2]
                })
                nested_list[nested_index] = sub_class

    return ET.ElementTree(root)


a = convert_cpc_standard_to_xml_tree(open_tsv_file(
    'data/CPCTitleList202208/cpc-section-E_20220801.txt'))
a.write("filename.xml")
