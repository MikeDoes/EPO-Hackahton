### Library that deals with the processing of CPC data from https://www.cooperativepatentclassification.org/cpcSchemeAndDefinitions/bulk ###
import csv

def open_tsv_file(path=""):
    """Opens TSV file"""
    table = []
    with open(path, newline='') as csvfile:
        file_reader = csv.reader(csvfile, delimiter='\t')
        for row in file_reader:
            table += [row]
    return table

def export_xml_file(data, output_path="data/E_test.xml"):


data = open_tsv_file('data/CPCTitleList202208/cpc-section-E_20220801.txt')


for i, data in open_tsv_file('')