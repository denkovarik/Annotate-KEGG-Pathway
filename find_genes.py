# Import Modules
import sys
import csv
import codecs
import pandas as pd



########################## Functions ############################

def check_cmd_args():
    """
    This function checks the command line arguments into the 
    program. To do this, this function will call other
    functions like 'excel_sheet_ext_good' and 'print_usage'. If
    the command line arguments are good, then this function
    will return True. Otherwise, it will print an error message
    and return False.
    
    :return: True if the command line arguments are correct.
    :return: False otherwise
    """
    # Read the excel file genome annotation, which should be 
    # the first command line argument and check the file 
    # extension
    if len(sys.argv) > 2:
        if not file_ext_good(sys.argv[1], 'xls'):
            # Print error message
            err = "Error: First command line argument must be "
            err += "an excel sheet\n"
            print(err)
            # Print usage statement
            print_usage()
    else:
        # Print error message
        err = "Error: Invalid number of command line " 
        err += "arguements\n"
        print(err)
        # Print usage statement
        print_usage()


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
    file_name = sys.argv[1]
    # Find the position of the '.' char for determining the file
    # extension
    pos = file_name.rfind(".")
    # Get the extension substring in the excel_file_name by 
    file_ext = file_name[pos+1:]
    if file_ext == ext:
        # File ext good, return True
        return True   
    # File ext not good, return False
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
    
#################################################################



########################### Main ################################

# Check the command line arguements
check_cmd_args()
# Read the xls file
df = pd.read_excel(sys.argv[1])
# Store EC numbers in a python set
proteins = set(())  
for protein in df.function:
    pos = protein.find("(EC ")
    if pos > 0:
        proteins.add(protein[pos+4:protein.find(")", pos)].strip())
        
for protein in proteins:
    print(protein)