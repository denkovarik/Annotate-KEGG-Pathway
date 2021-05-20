# Import Modules
import sys



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
    if len(sys.argv) > 1:
        if not excel_sheet_ext_good(sys.argv[1]):
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


def excel_sheet_ext_good(filename):
    """
    This function just checks that the string variable 'filename'
    passed into the function has a .xls extension. The string
    variable 'filename' represents the filename of the excel
    sheet genome annotation for the organism. This function
    will return True if 'filename' has the .xls extenstion.
    Otherwise it will return False.
    
    :param filename: Filename for the excel sheet.
    :return: True if filename has the .xls extension
    :return: False Otherwise
    """
    excel_file_name = sys.argv[1]
    # Find the position of the '.' char for determining the file
    # extension
    pos = excel_file_name.find(".")
    # Get the extension substring in the excel_file_name by 
    ext = excel_file_name[pos+1:]
    if ext == 'xls':
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

    
    