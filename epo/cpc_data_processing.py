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

def export_xml_file(data, output_path="data/E_test.xml"):
    
    
    root = ET.Element('section', attrib={
        "code": data[0][0],
        "title": data[0][2],
    })
    
    nest_counter = 0
    
    for row in data[1:]:
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

        if len(row[0]) > 4:
            # This is a class or sub-class. Got to review this nested logic
            if int(row[1]) == 0:
                main_class = ET.SubElement(sub_group, 'main_class', attrib={
                    "code": row[0],
                    "title": row[2]
                })
                nest_counter = 0
            
            if int(row[1]) == 1:
                classification_class = ET.SubElement(main_class, 'sub_class', attrib={
                    "code": row[0],
                    "title": row[2]
                })
                nest_counter = 1


    return ET.ElementTree(root)

a = export_xml_file(open_tsv_file('data/CPCTitleList202208/cpc-section-E_20220801.txt'))
a.write("filename.xml")
