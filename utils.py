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

webFileExt = ''


################################ Functions ##################################

def annotate_pathway(baseName, inDir, outDir, proteins, webExt=None):
    """
    This function annotates the pathway from KEGG.
    
    :param baseName: The base name for the pathway
    :param inDir: Pathway to baseName KEGG Pathway
    :param outDir: Pathway to ouput dir
    :param proteins: Dictionary of proteins
    :param webExt: Extention of the web file
    :return: The filepath for the annotated pathway .htm file.
    """ 
    # Source and destination filepaths for pathway
    inPathway = inDir + "\\" + baseName
    outPathway = outDir + "\\" + baseName
    # Check if files already exist in destination  
    htmFilepath = outPathway + webExt
    if os.path.isfile(htmFilepath):
        os.remove(htmFilepath) 
    filesPath = outPathway+"_files"
    if os.path.isdir(filesPath):
        shutil.rmtree(filesPath)
    # Copy files into destination directory
    shutil.copyfile(inPathway+webExt, htmFilepath)
    shutil.copytree(inPathway+"_files", outPathway+"_files")
    # Parse htm source code for pathway image filepath
    HtmlFile = open(htmFilepath, 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    pathwayMapIm = getPathwayImPath(outPathway, source_code) 
    # Create a Set containing all EC numbers
    ec_all = set(())
    for s in proteins.keys():
        if s.split(" ")[0] == 'Genome' and s.split(" ")[1] == 'Annotation':
            for ec in proteins[s]:
                if not ec in ec_all:
                    ec_all.add(ec)
    i=Image.open(pathwayMapIm)
    draw=D.Draw(i)
    # Search for protein Abbrevs
    source_code_temp = source_code.lower()
    for abbrev in proteins['abbrevs']:
        pos = source_code_temp.find("(" + abbrev.lower() + ")")
        if pos != -1:
            coordPos = source_code_temp.rfind("coords", 0, pos)
            coordsStart = source_code_temp.find('"', coordPos) + 1
            coordsEnd = source_code_temp.find('"', coordsStart)
            theCoords = source_code_temp[coordsStart:coordsEnd]
            sep = theCoords.find(",")
            sep2 = theCoords.find(",", sep+1)
            sep3 = theCoords.find(",", sep2+1)
            startCoords = (int(theCoords[0:sep]), \
                           int(theCoords[sep+1:sep2]))
            endCoords   = (int(theCoords[sep2+1:sep3]), \
                           int(theCoords[sep3+1:]))
            color = 'yellow'
            draw.rectangle([startCoords,endCoords],outline=color,width=2)
    # Draw Green boxes around EC Numbers
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
                present_in_all = True
                for s in proteins.keys():
                    if s.split(" ")[0] == 'Genome' and s.split(" ")[1] == 'Annotation':
                        if not ec in proteins[s]:
                            present_in_all = False
                if present_in_all:
                    color = 'green'
                else:
                    color = 'yellow'                    
                draw.rectangle([startCoords,endCoords],outline=color,width=2)
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
        
        
def ec_strip(ec):
    """
    Strips the ec number of whitespace and other characters that are not apart 
    of the EC number.
    
    :param ec: The String of the ec number to strip
    :return: The stripped ec number.
    """
    ec = ec.strip()
    s = 0
    e = s
    while s < len(ec):
        if ec[s].isdigit():
            e = s
            # Search for the 3 periods in an ec number
            e = ec.find(".", e)
            if e == -1:
                return ""
            e = ec.find(".", e + 1)
            if e == -1:
                return ""
            e = ec.find(".", e + 1)
            if e == -1:
                return ""
            elif e >= len(ec):
                return ""
            e += 1   
            # Find the end of the EC number
            if ec[e] == '-':
                if is_ec(ec[s:e+1]):
                    return ec[s:e+1]
            elif ec[e].isdigit():
                while e < len(ec) and ec[e].isdigit():
                    e += 1
            # Make sure not #.#.#.#.#
            if e < len(ec) and ec[e] == '.' and e + 1 < len(ec) and ec[e+1].isdigit():
                return ""
            if is_ec(ec[s:e]):
                return ec[s:e]
        s += 1
    return ""
        
        
def check_file_exists(filepath):
    """
    Function to check if a file exists. This file will exit the program if 
    the file does not exist.
    
    :param filepath: The filepath to check
    """
    if not os.path.isfile(filepath):
        print(filepath + " does not exist\nQuitting...")
        exit(1)
        
        
def extract_ec(string):
    """
    Extracts the EC number from a string.
    
    :param string: The string to extract the EC number from.
    :return: The EC number as a list of strings
    :return: empty set if no EC number found in string
    """
    if not has_ec(string):
        return set(())
    ec_nums = set(())
    
    # search for ec followed by space
    ec_nums = ec_nums.union(extract_ec_by_keyword(string, "ec: "))
    # search for ec: followed by space
    ec_nums = ec_nums.union(extract_ec_by_keyword(string, "ec "))
    # search for ec followed by no space
    ec_nums = ec_nums.union(extract_ec_by_keyword(string, "ec:"))
    # search for ec: followed by no space
    ec_nums = ec_nums.union(extract_ec_by_keyword(string, "ec"))
    
    return ec_nums
    
    
def extract_ec_by_keyword(string, keyword):
    """
    Extracts the EC number from a string by searching for a keyword.
    
    :param string: The string to extract the EC number from.
    :param keyword: The keyword used to search of ec numbers
    :return: The EC number as a list of strings
    :return: Empty set if no EC number found in string
    """
    ec_nums = set(())
    i = 0
    the_str = string.lower()
    
     # search for ec number by keyword
    while i < len(string) and i != -1:
        i = the_str.find(keyword, i)
        if i != -1:
            i += len(keyword)
            j = i
            # Find the 3 periods
            j = the_str.find(".", j + 1)
            if j == -1:
                break
            j = the_str.find(".", j + 1)
            if j == -1:
                break
            j = the_str.find(".", j + 1)
            if j == -1:
                i = j
                break
            j += 1
            if the_str[j] == '-':
                j += 1
                if is_ec(string[i:j]):
                    ec_nums.add(ec_strip(string[i:j]))
            elif the_str[j].isdigit():
                while j < len(the_str) and the_str[j].isdigit():
                    j += 1
                if is_ec(string[i:j]):
                    ec_nums.add(ec_strip(string[i:j]))
        if i != -1:
            i += 1  
    return ec_nums
    

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
    
    
def has_ec(word):
    """
    Determines if a string has an EC number contained in it. This 
    function looks for the following string patterns.
            
    :param word: A string to determine if is an EC number or not.
    :return: Boolean indicating if a string contains an EC number
    """
    word = word.strip()
    word = word.lower()
    words = word.split(" ")
    # Search for "ec" keyword
    for i in range(len(words)):
        if words[i].lower() == "ec" and len(words) > i:
            if is_ec(words[i+1].lower()):
                return True
        if words[i].lower() == "ec:" and len(words) > i:
            if is_ec(words[i+1].lower()):
                return True
        if words[i].lower() == "(ec" and len(words) > i:
            if is_ec(words[i+1].lower()):
                return True
        if words[i].lower() == "(ec:" and len(words) > i:
            if is_ec(words[i+1].lower()):
                return True
    return False
    
    
def is_ec(word):
    """
    Determines if 'word' is an ec number or not.
            
    :param word: A string to determine if is an EC number or not.
    :return: A boolean indicating if a string is an EC number
    """
    word = word.strip()
    # Remove '(' characters
    s = 0
    while s != -1:
        s = word.find("(")
        if s != -1:
            if s < len(word) - 2:
                word = word[s+1:]
            else:
                word = word[:s]
    # Remove ')' characters
    s = 0
    while s != -1:
        s = word.find(")")
        if s != -1:
            if s < len(word) - 2:
                word = word[s+1:]
            else:
                word = word[:s]
            
    # The string must be non-empty
    if len(word) == 0:
        return False
    # Must be a single word
    if word.find(" ") != -1:
        return False
    # First character must be a digit
    if not word[0].isdigit():
        return False
    # Must have 3 periods
    if word.count('.') != 3:
        return False
    # The last character must be a digit or -
    if not word[len(word)-1].isdigit() and word[len(word)-1] != '-':
        return False
    # Make sure digits seperate the periods
    if word.find("..") > 0:
        return False
    # Make sure every character is either a digit, -, or .
    for i in word:
        if i.isdigit():
            pass
        elif i == '-':
            pass
        elif i == '.':
            pass
        else:
            return False
    return True


def print_usage():
    """
    Function that prints the usage statement for the program.
    """
    usage = "Usage:\n"
    usage += "\tpy find_genes.py excel_sheet_download.py "
    usage += "file_containing_EC_numbers.txt"
    print(usage)
    return
    
    
def read_header(filepath):
    """
    Reads the header of a genome annotation and returns the column names as a 
    list.
    
    :param filepath: Filepath to the genome annotation
    :return: A list of the column names
    """  
    col_labels = []
    excel_data_df = pd.read_excel(filepath)
    for col in excel_data_df.columns:
        col_labels += [col]
    return col_labels
    
    
def read_genome_annot_EC(filepath, col):
    """
    Reads the ec numbers from a genome annotation excel sheet.
    
    :param filepath: The filepath for the genome annotation
    :param col: The column to read
    :return: A set of EC numbers
    """
    ec_nums = set(())
    # Read genome annotation excel file
    annot_df = pd.read_excel(filepath)
    # Iterate over rows
    for ind in annot_df.index:
        ec_nums = ec_nums.union(extract_ec(annot_df[col][ind]))
    return ec_nums
    
    
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
    
##############################################################################
