from pathlib import Path
import PySimpleGUI as sg
from utils import *
import webbrowser


sg.theme("DarkBlue")

welcome_msg = "Welcome to Annotate KEGG Pathway!\n\n"
welcome_msg += "This project was designed to help researchers use the biochemical pathways on KEGG (KEGG pathways)\n"
welcome_msg += "to analyze the genome of an organism. Specifically, it indicates which proteins from a KEGG pathway\n"
welcome_msg += "are present in an organism's genome. This project reads the excel file from an organism's genome\n"
welcome_msg += "annotation(s) (completed by RAST and/or PATRIC) and records the EC numbers for the proteins present\n"
welcome_msg += "in them. Then it parses the html file of a KEGG pathway to determine the EC numbers of the proteins\n"
welcome_msg += "present in the pathway. The program compares the proteins from the KEGG pathway to the proteins found\n"
welcome_msg += "in the organism's genome annotation. Proteins from the genome annotation that are also found to be present\n"
welcome_msg += "in the KEGG Pathway are indicated by colored boxes around the protein's EC Number in the KEGG Pathway.\n"
welcome_msg += "When completed, the annotated KEGG pathway will be saved to your local computer, and it will open up in your\n"
welcome_msg += "browser as a working webpage.\n\n\n"
welcome_msg += "Select Files to Complete an Annotation of a KEGG Pathway\n"
welcome_msg += "==========================================================================================="

usage = "First downloaded the complete webpage of the KEGG Pathway you want to annotate and save it an a known location. "
usage += "Please note that the saved pathway should consist of an .htm file and a folder containing more files and images. To "
usage += "save the complete webpage to your local device, open the KEGG Pathway you want to annotate in your browser. "
usage += "Select 'File', then 'Select Save Page...'. Select the directory that you wish to save the page to, and make sure that "
usage += "the option 'Save as type:' is selected in the 'Save as type:' box. Then select save, and the complete webpage should "
usage += "be saved in the selected folder on you local device.\n\n"

usage += "Upon startup, this program will ask for 4 filepaths. Enter either the filepath for the RAST genome annotataion excel "
usage += "spreadsheet, the filepath for the PATRIC genome annotataion excel spreadsheet, or both. Please note that only one of "
usage += "these excel spreadsheets are needed, but the program will also except both. Select the .htm file from the downloaded "
usage += "pathway that you want to annotate. Finally, select the output directory that you want the program to place the annotated "
usage += "KEGG Pathway in. This will be a webpage that should open up in your browser.\n\n"

usage += "Finally, select 'Go'. The pathway will be annotated indicating which proteins in the pathway are also present in your "
usage += "organism. A green box means that the gene for a protein was found in both the RAST and PATRIC genome annotations. "
usage += "An orange box indicates that the gene for the protein was only found in the RAST genome annotation. Blue boxes means "
usage += "that the gene for the protein was only found in the PATRIC genome annotation.\n\n\n"

layout = [
    [sg.Text(welcome_msg)],
    [sg.Text('Select RAST Excel Spreadsheet Genome Annotation: '), sg.InputText(key='-RAST_file-'), sg.FileBrowse()],
    [sg.Text('Select PATRIC Excel Spreadsheet Genome Annotation: '), sg.InputText(key='-PATRIC_file-'), sg.FileBrowse()],
    [sg.Text('Select Input Pathway .htm File to Annotate: '), sg.InputText(key='-Input Pathway-'), sg.FileBrowse()],
    [sg.Text('Select Output Directory for Annotated Pathway Files: '), sg.InputText(key='-Output Dir-'), sg.FolderBrowse()],
    [sg.Button("Go")],
    [sg.Button("Help")],
]

window = sg.Window('Annotate KEGG Pathway', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Help":
        sg.popup_ok(usage, title="Usage")
    elif event == "Go":
        if valid_selections(values):
            # Format Filepaths
            RAST_filepath = values['-RAST_file-'].replace("/","\\")
            PATRIC_filepath = values['-PATRIC_file-'].replace("/","\\")
            path = values['-Input Pathway-'].replace("/","\\")
            pathwayName = path[path.rfind("\\")+1:path.rfind(".")]
            inDir = path[:path.rfind("\\")]
            outDir = values['-Output Dir-'].replace("/","\\")
            # Read RAST Spreadsheet
            rast_ec = read_RAST_EC_Nums(RAST_filepath)
            # Read PATRIC Spreadsheet
            patric_ec = read_PATRIC_EC_Nums(PATRIC_filepath)
            # Annotate the Pathway
            webExt = path[path.rfind("."):]
            annotated_filepath = annotate_pathway(pathwayName, inDir, outDir, rast_ec, patric_ec, webExt)
            msg = "Annotation of '" + pathwayName + "' is "
            msg += "Complete!\n\nThe proteins present in this pathway, "
            msg += "that are also present in your organism, are indicated "
            msg += "by the colored boxes. A green box means that the gene "
            msg += "for a protein was found in both the RAST and PATRIC "
            msg += "genome annotations. An orange box indicates that the "
            msg += "gene for the protein was only found in the RAST genome "
            msg += "annotation. Blue boxes means that the gene for the "
            msg += "protein was only found in the PATRIC genome annotation."
            
            sg.popup_ok(msg, title="Pathway Annotation Complete")
            # Launch the webpage
            url = "file:///" + annotated_filepath
            webbrowser.open(url, new=2)  # open in new tab

window.close()