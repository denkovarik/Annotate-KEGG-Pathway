# Import Modules
import sys
import os
import csv
import codecs
import pandas as pd
import urllib.request
from PIL import Image, ImageDraw as D



########################## Functions ############################

def parse_cmd_args():
    """
    This function parses the command line arguments
    
    :return: A dictionary of the arguments
    """
    args = {}
    for arg in sys.argv:
        pos = arg.find("=")
        if pos > -1:
            args[arg[:pos]] = arg[pos+1:]
    return args


def file_ext_good(filename, ext):
    """
    This function just checks that the string variable 'filename'
    passed into the function has the correct extension. The string
    variable 'filename' represents the filename of the excel
    sheet genome annotation for the organism. The string 'ext' 
    represent the file extension that the filename is expected to 
    have. This function will return True if 'filename' has the 
    extenstion equal to the string stored in the 'ext' parameter.
    Otherwise it will return False.
    
    :param filename: Filename for input file.
    :param ext: The expected extension for 'filename'
    :return: True if filename has the .xls extension
    :return: False Otherwise
    """
    # Find the position of the '.' char for determining the file
    # extension
    pos = filename.rfind(".")
    # Get the extension substring in the excel_file_name by 
    file_ext = filename[pos+1:]
    if file_ext == ext:
        # File ext good, return True
        return True   
    # File ext not good, return False
    return False
    
    
def getCoords(pos):
    """
    Function to get the coordinates of a protein from the pathway .htm file
    
    :param pos: The start position to find the nearest coordinates before 
                that point in the file
    :return: The start coordinates as a tuple
    :return: The end coordinates as a tuple
    """
    coordPos = source_code.rfind("coords", 0, pos)
    coordsStart = source_code.find('"', coordPos) + 1
    coordsEnd = source_code.find('"', coordsStart)
    theCoords = source_code[coordsStart:coordsEnd]
    sep = theCoords.find(",")
    sep2 = theCoords.find(",", sep+1)
    sep3 = theCoords.find(",", sep2+1)
    startCoords = (int(theCoords[0:sep]), \
                   int(theCoords[sep+1:sep2]))
    endCoords   = (int(theCoords[sep2+1:sep3]), \
                   int(theCoords[sep3+1:]))
    return startCoords, endCoords
    
    
def getPathwayFiles(baseName):
    """
    Function to return the .htm and pathway image filepaths associated
    with a pathway. 
    
    :param baseName: The basename for the pathway
    :return: Filepath for the htm file associated with the pathway
    :return: Filepath for the pathway's map image
    """
    htmFilepath = baseName + ".htm"
    pathwayFiles = baseName + "_files"
    if not os.path.isfile(htmFilepath):
        print(htmFilepath + " does not exist\nQuitting...")
        exit(1)
    # Get pathway map filepath
    if not os.path.isdir(pathwayFiles):
        print(pathwayFiles + " does not exist")
        print("Quitting...")
        exit(2)
    for f2 in os.listdir(pathwayFiles):
        if f2[:3] == "map" and not (f2.rfind(".") > -1 \
        and f2.rfind("_") > -1 \
        and f2[f2.rfind("_"):f2.rfind(".")] == "_annotated"):
            pathwayMapIm = pathwayFiles + "\\" + f2
    if not os.path.isfile(pathwayMapIm):
        print(pathwayMapIm + " does not exist\nQuitting...")
        exit(3)
    return htmFilepath, pathwayMapIm
    
    
def print_usage():
    """
    Function that prints the usage statement for the program.
    """
    usage = "Usage:\n"
    usage += "\tpy find_genes.py excel_sheet_download.py "
    usage += "file_containing_EC_numbers.txt"
    print(usage)
    return
    
#################################################################



########################### Main ################################

# Parse command line arguments
args = parse_cmd_args()

# Read the xls file
df = pd.read_excel(args["RAST_Spreadsheet"])
# Store EC numbers in a python set
ecNumbers = set(())  
for protein in df.function:
    pos = protein.find("(EC ")
    if pos > 0:
        ecNumbers.add(protein[pos+4:protein.find(")", pos)].strip())
# Read and store protein abbreviations
proteinAbbrevs = set(())
if "protein_abbrev" in args:
    with open(args["protein_abbrev"],'r') as file:  
        # reading each line    
        for line in file:
            # reading each word        
            for abbrev in line.split(): 
                # displaying the words           
                proteinAbbrevs.add(abbrev.strip())
       
pathwaysPath = args["pathways"]
while pathwaysPath[len(pathwaysPath)-1] == "\\":
    pathwaysPath = pathwaysPath[:len(pathwaysPath)-1]
    
pathwayNames = set(())
for f in os.listdir(pathwaysPath):
    if not(len(f) > 11 and f[len(f)-12:] == "_updated.htm") \
    and file_ext_good(f, 'htm'):
        baseName = f[:f.rfind(".")]
        pathwayNames.add(baseName)
        
for baseName in pathwayNames:
    # Get htm file
    htmFilepath, pathwayMapIm = getPathwayFiles(pathwaysPath + "\\" \
                              + baseName)
        
    i=Image.open(pathwayMapIm)
    draw=D.Draw(i)
    HtmlFile = open(htmFilepath, 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    # Draw Green boxes around EC Numbers
    for ec in ecNumbers:
        pos = 0
        while pos > -1:
            pos = source_code.find("+"+ec+'+', pos+1)
            if pos > -1:
                startCoords, endCoords = getCoords(pos)
                draw.rectangle([startCoords,endCoords],outline="green")
    # Draw Green boxes around Protein Abbreviations
    for abbrev in proteinAbbrevs:
        pos = 0
        while pos > -1:
            pos = source_code.find("("+abbrev+')', pos+1)
            if pos > -1:
                print(abbrev)
                startCoords, endCoords = getCoords(pos)
                draw.rectangle([startCoords,endCoords],outline="green")
    newPathwayMapIm = pathwayMapIm[:pathwayMapIm.rfind(".")] + "_annotated" \
                    + pathwayMapIm[pathwayMapIm.rfind("."):]
    imPath = source_code.find('<img src="KEGG%20PATHWAY')
    imPathStart = source_code.find('"', imPath)
    imPathEnd = source_code.find('"', imPathStart+1)
    source_code = source_code[:imPathStart+1] + newPathwayMapIm \
                + source_code[imPathEnd:]
    newHtmFilepath = htmFilepath[:htmFilepath.rfind(".")] + "_updated" \
                   + htmFilepath[htmFilepath.rfind("."):] 
    i.save(newPathwayMapIm)
    updatedHtmlFile = open(newHtmFilepath, "w", encoding='utf-8')
    updatedHtmlFile.write(source_code)
    #i.show()
    HtmlFile.close()
    updatedHtmlFile.close()
    i.close()
