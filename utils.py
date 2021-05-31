# Import Modules
import sys
import os
import csv
import codecs
import pandas as pd
import urllib.request
from PIL import Image, ImageDraw as D
import openpyxl
import shutil
from pathlib import Path
import PySimpleGUI as sg


################################ Functions ##################################

def annotate_pathway(baseName, inDir, outDir, ec_RAST=None, ec_PATRIC=None):
    """
    This function annotates the pathway from KEGG.
    
    :param baseName: The base name for the pathway
    :return: The filepath for the annotated pathway .htm file.
    """ 
    # Source and destination filepaths for pathway
    inPathway = inDir + "\\" + baseName
    outPathway = outDir + "\\" + baseName
    # Check if files already exist in destination  
    htmFilepath = outPathway + ".htm"
    if os.path.isfile(htmFilepath):
        os.remove(htmFilepath) 
    filesPath = outPathway+"_files"
    if os.path.isdir(filesPath):
        shutil.rmtree(filesPath)
    # Copy files into destination directory
    shutil.copyfile(inPathway+".htm", htmFilepath)
    shutil.copytree(inPathway+"_files", outPathway+"_files")
    # Parse htm source code for pathway image filepath
    HtmlFile = open(htmFilepath, 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    pathwayMapIm = getPathwayImPath(outPathway, source_code) 
    # Create a Set containing all EC numbers
    ec_all = set(())
    if ec_RAST is not None:
        ec_all = ec_all.union(ec_RAST)
    if ec_PATRIC is not None:
        ec_all = ec_all.union(ec_PATRIC)  
    # Draw Green boxes around EC Numbers
    i=Image.open(pathwayMapIm)
    draw=D.Draw(i)
    for ec in ec_all:
        pos = 0
        while pos > -1:
            pos = source_code.find("+"+ec+'+', pos+1)
            if pos > -1:
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
                color = ''
                if ec_RAST is not None and ec in ec_RAST:
                    if ec_PATRIC is not None and ec in ec_PATRIC:
                        color = 'green'
                    else:
                        color = 'orange'
                elif ec_PATRIC is not None and ec in ec_PATRIC:
                    color = 'blue'
                    
                if color != '':
                    draw.rectangle([startCoords,endCoords],outline=color)

    newPathwayMapIm = pathwayMapIm[:pathwayMapIm.rfind(".")] \
                    + pathwayMapIm[pathwayMapIm.rfind("."):]
    i.save(newPathwayMapIm)
    HtmlFile.close()
    i.close()
    return htmFilepath


def check_dir_exists(path):
    """
    Function to check if a directory exists. This file will exit the program
    if the directory does not exist.
    
    :param path: The path to check
    """
    if not os.path.isdir(path):
        print(path + " does not exist")
        print("Quitting...")
        exit(2)
        
        
def check_file_exists(filepath):
    """
    Function to check if a file exists. This file will exit the program if 
    the file does not exist.
    
    :param filepath: The filepath to check
    """
    if not os.path.isfile(filepath):
        print(filepath + " does not exist\nQuitting...")
        exit(1)
        

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
    
    
def getPathwayImPath(basePath, content):
    """
    Function to return filepath of the pathways map image used in the htm
    document.
    
    :param basePath: The basename for the pathway
    :param content: The source code for the htm file 
    :return: Filepath for the pathway's map image
    """
    # Path to the pathways _files directory
    pathwayFilesPath = basePath + "_files\\"   
    check_dir_exists(pathwayFilesPath)
    # Search for location of pathway's map image name in the htm document
    pos = content.find('<img src="')
    pos = content.find('"', pos+1)
    end = content.find('"', pos+1)
    start = content.rfind("/", pos, end) + 1
    # Get pathway map image filepath by scanning htm doc source code 
    pathwayMapIm = pathwayFilesPath + content[start:end]
    check_file_exists(pathwayMapIm)
    return pathwayMapIm
    
    
def get_pathway_filepaths(path):
    """
    This function simply returns a set of pathway names. A pathway name is expected to be an htm file. 
    
    :param path: The path to the directory containing the pathways.
    :return: A set of filepaths to each pathway located in a directory.
    """
    pathwayNames = set(())
    for f in os.listdir(path):
        if not(len(f) > 11 and f[len(f)-12:] == "_updated.htm") \
        and file_ext_good(f, 'htm'):
            baseName = f[:f.rfind(".")]
            pathwayNames.add(baseName)
    return pathwayNames
    
    
def is_PATRIC_spreadsheet(filepath):
    """
    This function determines if a file is an excel spreadsheet of a genome
    annotation completed by RAST.
    
    :param filepath: The filepath of the file to check
    :return: True if file is an excel spreadsheet of a RAST genome annotation
    :return: False otherwise
    """
    # Check the file extension for .xls extension
    ext = filepath[filepath.rfind("."):]
    if ext != '.xlsx':
        return False
    # Check that file exists
    if not os.path.isfile(filepath):
        print(filepath + " does not exist")
        return False
    # List of expected column names for a genome annotation excel 
    # spreadsheet from PATRIC
    expected_col_names = ['Genome', 'Genome ID', 'Accession', 'PATRIC ID', 'RefSeq Locus Tag', 'Alt Locus Tag', 'Feature ID', 'Annotation', 'Feature Type', 'Start', 'End', 'Length', 'Strand', 'FIGfam ID', 'PATRIC genus-specific families (PLfams)', 'PATRIC cross-genus families (PGfams)', 'Protein ID', 'AA Length', 'Gene Symbol', 'Product', 'GO']

    try:
        # Make sure file has expected columen names for PATRIC spreadsheet
        wb_obj = openpyxl.load_workbook(filepath)
        sheet = wb_obj.active
        for row in sheet.iter_rows(max_row=1):
            for cell, exp in zip(row, expected_col_names):
                if cell.value != exp:
                    return False
        return True
    except:
        err = "An error occured while reading file column names for PATRIC "
        err += "excel file."
        print(err)
    # Otherwise return False
    return False


def is_RAST_spreadsheet(filepath):
    """
    This function determines if a file is an excel spreadsheet of a genome
    annotation completed by RAST.
    
    :param filepath: The filepath of the file to check
    :return: True if file is an excel spreadsheet of a RAST genome annotation
    :return: False otherwise
    """
    # Check the file extension for .xls extension
    if filepath[filepath.rfind("."):] != '.xls':
        return False
    # Check that file exists
    if not os.path.isfile(filepath):
        print(filepath + " does not exist")
        return False
    # List of expected column names for a genome annotation excel 
    # spreadsheet from RAST
    expected_col_names = ['contig_id', 'feature_id', 'type', 'location', \
    'start', 'stop', 'strand', 'function', 'aliases', 'figfam', \
    'evidence_codes', 'nucleotide_sequence', 'aa_sequence']
    # Make sure file has expected columen names for RAST spreadsheet
    try:
        df = pd.read_excel(filepath)
        file_col_names = df.columns.view()
        if (file_col_names == expected_col_names).all():
            return True
    except:
        err = "An error occured while reading file column names for RAST "
        err += "excel file."
        print(err)
    # Otherwise return False
    return False


def print_usage():
    """
    Function that prints the usage statement for the program.
    """
    usage = "Usage:\n"
    usage += "\tpy find_genes.py excel_sheet_download.py "
    usage += "file_containing_EC_numbers.txt"
    print(usage)
    return
    
    
def read_PATRIC_EC_Nums(filepath):
    """
    This function reads all the EC numbers in an excel spreadsheet from a 
    genome annotation completed by PATRIC. This function will store these EC 
    numbers in a set and return it.
    
    :param filepath: The filepath of the PATRIC file
    :return: A set of protein EC numbers
    """
    if not is_PATRIC_spreadsheet(filepath):
        raise Exception("File is not a RAST excel spreadsheet")
    ecNumbers = set(())  
    try:       
        wb = openpyxl.load_workbook(filepath)
        first_sheet = wb.sheetnames[0]
        worksheet = wb[first_sheet]

        #here you iterate over the rows in the specific column
        for row in range(2,worksheet.max_row+1):  
            for column in "T":  
                cell_name = "{}{}".format(column, row)
                protein = worksheet[cell_name].value
                pos = protein.find("(EC ")
                if pos > 0:
                    ec = protein[pos+4:protein.find(")", pos)]
                    ecNumbers.add(ec.strip())
        return ecNumbers
    except:
        err = "An error occured while reading file column names for PATRIC "
        err += "excel file."
        print(err)
    return ecNumbers
    
    
def read_protein_abbrevs(filepath):
    """
    This function reads a txt file contain line or space separated protein 
    abbreviations and returns them as a set.
    
    :param filepath: The filepath of the file to check
    :return: A set of protein abbreviations
    """
    # Check for correct file extension
    if filepath[filepath.rfind("."):] != ".txt":
        raise Exception("Incorrect filetype for protein abbreviations file") 
    # Read and store protein abbreviations
    proteinAbbrevs = set(())
    with open(filepath,'r') as file:  
        # reading each line    
        for line in file:
            # reading each word        
            for abbrev in line.split(): 
                # displaying the words           
                proteinAbbrevs.add(abbrev.strip())
    # Return the set
    return proteinAbbrevs
    
    
def read_RAST_EC_Nums(filepath):
    """
    This function reads all the EC numbers in an excel spreadsheet from a 
    genome annotation completed by RAST. This function will store these EC 
    numbers in a set and return it.
    
    :param filepath: The filepath of the RAST file
    :return: A set of protein EC numbers
    """
    if not is_RAST_spreadsheet(filepath):
        raise Exception("File is not a RAST excel spreadsheet")
        
    # Read the xls file
    df = pd.read_excel(filepath)
    # Store EC numbers in a python set
    ecNumbers = set(())  
    for protein in df.function:
        pos = protein.find("(EC ")
        if pos > 0:
            ecNumbers.add(protein[pos+4:protein.find(")", pos)].strip())
    return ecNumbers
    
    
def valid_in_pathway_selection(filepath):
    """
    Validates the selection for the input pathway to annotate.
    
    :param filepath: The filepath of the input pathway .htm file to validate.
    :return: True if selection was valid
    :return: False otherwise
    """
    # Check if a file was selected
    if filepath == '':
        msg = "You must select a .htm file for the input pathway to continue!"
        title = "Invalid Pathway Selection"
        sg.popup_ok(msg,title=title)
        return False
    # Check that file has .htm extension
    elif filepath[filepath.rfind("."):] != '.htm':
        msg = "The input pathway file must be a .htm file!"
        title = "Invalid Pathway File Extension"
        sg.popup_ok(msg,title=title)
        return False
    # Check that the selected file is a file
    if not os.path.isfile(filepath):
        msg = "The input pathway file doesn't exit!"
        title = "File Not Found"
        sg.popup_ok(msg,title=title)
        return False
    return True
    
    
def valid_output_dir_selection(dirpath):
    """
    Validates the selection for the output directory.
    
    :param dirpath: The path to the output dir.
    :return: True if the path is valid 
    :return: False otherwise
    """
    # Make sure that an output directory was selected
    if dirpath == "":
        msg = "You must select an output directory to continue!"
        title = "Invalid Output Directory"
        sg.popup_ok(msg,title=title)
        return False
    return True
        
        
def valid_selections(values):
    """
    Validates the filepath selections for the input RAST excel spreadsheet, the input PATRIC excel spreadsheet, the input pathway .htm file to annotate, and the output directory to place the annotated pathway in.
    
    :param values: Dictionary containing the filepaths to validate
    """
    # Validate the RAST and PATRIC spreadsheet filepaths
    if not valid_spreadsheet_selections(values["-RAST_file-"], \
    values["-PATRIC_file-"]):
        return False
    # Validate the input pathway slection
    elif not valid_in_pathway_selection(values['-Input Pathway-']):
        return False
    # Validate the output directory path selection
    elif not valid_output_dir_selection(values['-Output Dir-']):
        return False
    # Make sure the input and output directories are not the same
    elif values['-Input Pathway-'][:values['-Input Pathway-'].rfind("/")] \
    == values['-Output Dir-']:
        msg = "The directory containing the input .htm file must be different from the output directory!"
        title = "Input Folder Same as Output Folder"
        sg.popup_ok(msg,title=title)
        return False        
    return True


def valid_spreadsheet_selections(RAST_filepath, PATRIC_filepath):
    """
    This function validates the selections for the RAST and Patric excel 
    spreadsheets.
    
    :param RAST_filepath: The filepath for the RAST excel spreadsheet
    :param PATRIC_filepath: The filepath for the PATRIC excel spreadsheet
    :return: True if the selections were validates
    :return: False otherwise
    """
    # Make sure a genome annotation excel spreadsheet is selected
    if RAST_filepath == '' and PATRIC_filepath == '':
        err_msg = "You must either have a RAST genome annotation excel spreadsheet, a PATRIC genome annotation excel spreadsheet, or both selected to continue." 
        sg.popup_ok(err_msg,title="Select a Genome Annotation")
        return False
    # Validate selected RAST Excel Spreadsheet
    elif RAST_filepath != '' and (not Path(RAST_filepath).is_file() or not is_RAST_spreadsheet(RAST_filepath)):
        if not Path(RAST_filepath).is_file():
            msg = "RAST Excel file does not exist!"
            title = "File Not Found"
            sg.popup_ok(msg, title=title)
        elif not is_RAST_spreadsheet(RAST_filepath):
            msg = "The selected file for the RAST Excel Spreadsheet is not a RAST Excel Spreadsheet!"
            title = "Invalid RAST Excel Spreadsheet"
            sg.popup_ok(msg, title=title)
        return False
    # Validate selected PATRIC Excel Spreadsheet
    elif PATRIC_filepath != '' and (not Path(PATRIC_filepath).is_file() or not is_PATRIC_spreadsheet(PATRIC_filepath)):
        if not Path(PATRIC_filepath).is_file():
            msg = "PATRIC Excel file does not exist!"
            title = "File Not Found"
            sg.popup_ok(msg, title=title)
        elif not is_PATRIC_spreadsheet(PATRIC_filepath):
            msg = "The selected file for the PATRIC Excel Spreadsheet is not a PATRIC Excel Spreadsheet!"
            title = "Invalid PATRIC Excel Spreadsheet"
            sg.popup_ok(msg, title=title)
        return False
    return True
    
##############################################################################
