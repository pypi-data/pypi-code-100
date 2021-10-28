# main.py
import argparse
from .create_yaml import create

# def main():
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-o','--outputfolder', help='output folder path to save the components', default='./example_vlocity_build')
# parser.add_argument('-p','--properties', help='properties file path containing credentials', required=True)
parser.add_argument('-y','--yaml', help='output yaml excel sheet name', default='vlocity_components.yaml')
parser.add_argument('-x','--xlsx', help='excel file path containing the components', required=True)
parser.add_argument('-s','--excelsheet', help='excel sheet name', required=True)
args = vars(parser.parse_args())
create(args)




