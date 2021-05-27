# Import Modules
import sys
import os
import csv
import codecs
import pandas as pd
import urllib.request
from PIL import Image, ImageDraw as D
from utils import *





################################# Main ######################################

ecNumbers = read_RAST_EC_Nums("..\\RAST_Geobacillus_LC41.xls")
patric_ec = read_PATRIC_EC_Nums("..\\PATRIC_genome_feature.xlsx")

inputPathwaysPath = "C:\\Users\\1985937\\Documents\\BI_Sum_2021\\pathways"
outPathwaysPath = 'C:\\Users\\1985937\\Documents\\BI_Sum_2021\\Bioinformatics-Tools\\annotated_pathways'

pathwayNames = get_pathway_filepaths(inputPathwaysPath)

for baseName in pathwayNames:        
    annotate_pathway(baseName, inputPathwaysPath, outPathwaysPath, ecNumbers, patric_ec)
