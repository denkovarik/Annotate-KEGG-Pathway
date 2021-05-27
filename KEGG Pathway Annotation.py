from pathlib import Path
import PySimpleGUI as sg
from utils import *
import webbrowser


sg.theme("DarkBlue")

welcome_msg = "Welcome to KEGG Pathway Annotation!\n\n"
welcome_msg += "This program was designed to help researches in Bioinformatics analyze the biochemical pathways present in\n"
welcome_msg += "organisms using the genome annotation of the species and the downloaded complete webpage of a KEGG Pathway.\n"
welcome_msg += "This program will parse an excel spreadsheet for the E.C. Numbers present in a genome annotatoin completed by\n"
welcome_msg += "either RAST, PATRIC, or both. It will then use these E.C. numbers to indicate which proteins from your organism are\n"
welcome_msg += "also present in any KEGG Pathway.\n\n"
welcome_msg += "Usage:\n"
welcome_msg += "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
welcome_msg += "First downloaded the complete webpage of the KEGG Pathway you want to annotate and save it an a known location.\n"
welcome_msg += "Please note that the saved pathway should consist of an .htm file and a folder containing more files and images. To\n"
welcome_msg += "save the complete webpage to your local device, open the KEGG Pathway you want to annotate in your browser.\n"
welcome_msg += "Select 'File', then 'Select Save Page...'. Select the directory that you wish to save the page to, and make sure that\n"
welcome_msg += "the option 'Save as type:' is selected in the 'Save as type:' box. Then select save, and the complete webpage should\n"
welcome_msg += "be saved in the selected folder on you local device.\n\n"

welcome_msg += "Upon startup, this program will ask for 4 filepaths. Enter either the filepath for the RAST genome annotataion excel\n"
welcome_msg += "spreadsheet, the filepath for the PATRIC genome annotataion excel spreadsheet, or both. Please note that only one of\n"
welcome_msg += "these excel spreadsheets are needed, but the program will also except both. Select the .htm file from the downloaded\n"
welcome_msg += "pathway that you want to annotate. Finally, select the output directory that you want the program to place the annotated\n"
welcome_msg += "KEGG Pathway in. This will be a webpage that should open up in your browser.\n\n"

welcome_msg += "Finally, select 'Go'. The pathway will be annotated indicating which proteins in the pathway are also present in your \n"
welcome_msg += "organism. A green box means that the gene for a protein was found in both the RAST and PATRIC genome annotations.\n"
welcome_msg += "An orange box indicates that the gene for the protein was only found in the RAST genome annotation. Blue boxes means\n"
welcome_msg += "that the gene for the protein was only found in the PATRIC genome annotation.\n\n\n"
welcome_msg += "Select Files to Complete an Annotation of a KEGG Pathway\n"
welcome_msg += "========================================================================================\n"

layout = [
    [sg.Text(welcome_msg)],
    [sg.Text('Select RAST Excel Spreadsheet Genome Annotation: '), sg.InputText(key='-RAST_file-'), sg.FileBrowse()],
    [sg.Text('Select PATRIC Excel Spreadsheet Genome Annotation: '), sg.InputText(key='-PATRIC_file-'), sg.FileBrowse()],
    [sg.Text('Select Input Pathway .htm File to Annotate: '), sg.InputText(key='-Input Pathway-'), sg.FileBrowse()],
    [sg.Text('Select Output Directory for Annotated Pathway Files: '), sg.InputText(key='-Output Dir-'), sg.FolderBrowse()],
    [sg.Button("Go")],
]

window = sg.Window('KEGG Pathway Genome Annotation', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
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
            annotated_filepath = annotate_pathway(pathwayName, inDir, outDir, rast_ec, patric_ec)
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