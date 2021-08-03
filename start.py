from pathlib import Path
import PySimpleGUI as sg
from utils import *
import webbrowser


sg.theme("DarkBlue")

welcome_msg = "Welcome to Annotate KEGG Pathway!\n\n"
welcome_msg += "This project was designed to help researchers use the biochemical pathways on KEGG (KEGG pathways) to\n"
welcome_msg += "analyze the genome of an organism. Specifically, it indicates which proteins from a KEGG pathway are\n"
welcome_msg += "present in an organism's genome. This project reads the excel file from an organism's genome annotation(s)\n"
welcome_msg += "and records the EC numbers for the proteins present in them. This program will take up to 5 genome\n"
welcome_msg += "annotations. It will also take another text file containing line separated protein abbreviations that you\n"
welcome_msg += "also want to include for the annotation of the KEGG-Pathway (sometimes protein abbreviations are used in\n"
welcome_msg += "KEGG-Pathways). Please note that this program will not look for protein abbreviations in the genome\n"
welcome_msg += "annotations. The program will then parse the html file of a KEGG pathway to determine the protein\n"
welcome_msg += "abbreviations and the EC numbers of the proteins present in the pathway. The program compares the proteins\n"
welcome_msg += "from the KEGG pathway to the proteins found in the organism's genome annotation and text files. Proteins\n"
welcome_msg += "from the genome annotation that are also found to be present in the KEGG Pathway are indicated by colored\n"
welcome_msg += "boxes around the protein's EC Number in the KEGG Pathway. For the annotated KEGG-Pathway, an EC number has\n"
welcome_msg += "a green rectangle drawn around it if the EC Number was present in all genome annotations given, and a yellow\n"
welcome_msg += "rectangle will be drawn around EC Numbers that were only present in some but not all of the genome\n"
welcome_msg += "annotations given. Protein abbreviations found in both the KEGG-Pathway and the supplemental protein\n"
welcome_msg += "abbreviation text file will always have yellow boxes drawn around them. When completed, the annotated KEGG\n"
welcome_msg += "pathway will be saved to your local computer, and it will open up in your browser as a working webpage.\n\n\n"


def create_genome_annote_layout(num_annotations=None, values=None):
    """
    Creates the layout for the Genome Annotaion Selection Window
    
    :param num_annotations: The number of Genome Annotations to use
    :param values: The input values from the window
    :return: The layout of the Genome Annotaion Selection Window
    """
    default_num_annots = 1
    if num_annotations is not None:
        default_num_annots = num_annotations
    layout = [
        [sg.Text('Annotate-KEGG-Pathway', size=(35, 1), justification='center', \
        font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)], 
        [sg.Text(welcome_msg)],
        [sg.Text('Select Genome Annotation Excel Files', justification='left', \
        font=("Helvetica", 15))],
        [sg.Text('Number of Genome Annotations to Use', size=(28, 1)), \
        sg.Spin(values=[i for i in range(1, 6)], \
        initial_value=default_num_annots, size=(6, 1), \
        key="num_annotations"), sg.Button("Confirm Number of Genome Annotations")],
    ]
    if num_annotations is not None:
        for i in range(num_annotations):
            annot_name = "Genome Annotation " + str(i + 1)
            if values is not None and annot_name in values.keys():
                layout += [sg.Text(annot_name), \
                    sg.InputText(values[annot_name], key=annot_name), \
                    sg.FileBrowse()],
            else:
                layout += [sg.Text(annot_name), sg.InputText(key=annot_name), \
                    sg.FileBrowse()],
        layout += [sg.Button("Help")],
        layout += [sg.Button("Next")],
    else:
        layout += [sg.Button("Help")],
    return layout
        

def genome_annotations_good(num_annotations, values):
    """
    Checks the genome annotations entered in for correctness.
    
    :param num_annotations: The number of Genome Annotations to use
    :param values: The input values from the window
    :return: True if genome annotations entered in are good.
    :return: False otherwise
    """
    if num_annotations < 1:
        return False
    for i in range(num_annotations):
        annot_name = "Genome Annotation " + str(i + 1)
        if values is None:
            msg = "Must select genome annotations to use"
            print(msg)
            sg.popup(msg)
            return False
        elif annot_name in values.keys():
            if values[annot_name] == "":
                msg = "Must select file for " + annot_name
                print(msg)
                sg.popup(msg)
                return False
            elif values[annot_name].split(".")[-1] != "xls":
                if values[annot_name].split(".")[-1] != "xlsx":
                    msg = "File for " + annot_name + " must be an excel file"
                    print(msg)
                    sg.popup(msg)
                    return False
        else:
            msg = "An unexpected error occured"
            print(msg)
            sg.popup(msg)
            return False
    return True
    
    

                
                
def launch_final_window(values):
    """
    Launches the window for selecting the protein column names for genome 
    annotations.
    
    :param values: The input values from the window
    """
    # Save the filepaths for the Genome Annotations to use
    help_msg  = "This is the final window before the program starts to "
    help_msg += "annotate the KEGG-Pathway. There are 2 required parameters, "
    help_msg += "and 1 optional parameter. The first required parameter is the "
    help_msg += ".htm or .html file for the KEGG-Pathway that you want to "
    help_msg += "annotate. Please note that the files for the downloaded "
    help_msg += "KEGG-Pathway should consist of an .htm or .html file along "
    help_msg += "with a folder of the same name. This is important because "
    help_msg += "the program will attempt to use files from this folder. "
    help_msg += "Please see the README on GitHub for more information. The "
    help_msg += "second required parameter is the directory to place the "
    help_msg += "annotated KEGG pathway files in. The one optional parameter "
    help_msg += "is a text file containing line separated protein "
    help_msg += "abbreviations. This program will not look for protein "
    help_msg += "abbreviations in the genome annotations. If you want protein "
    help_msg += "abbreviations in a KEGG-Pathway to be included in the "
    help_msg += "annotation, then you must specify a text file containing the "
    help_msg += "line separated protein abbreviations to include. Please see the "
    help_msg += "README for more information." 
    orgi_values = values.copy()
    sup_protein_file_msg = 'Text File Containing Line Separated Protein '
    sup_protein_file_msg += 'Abbreviations that are Expected to be In '
    sup_protein_file_msg += 'Genome\nAnnotation'
    layout = [
                [sg.Text('Annotate-KEGG-Pathway', size=(35, 1), \
                    justification='center', font=("Helvetica", 25), \
                    relief=sg.RELIEF_RIDGE)], 
                [sg.Text('Required Parameters', justification='left', \
                    font=("Helvetica", 15))],
                [sg.Text('----------------------------', justification='left', \
                    font=("Helvetica", 15))],
                [sg.Text('Select KEGG Pathway .htm File to Annotate', \
                    justification='left', font=("Helvetica", 12))],
                [sg.InputText(key="KEGG-Pathway"), sg.FileBrowse()],
                [sg.Text('Select Output Directory for Annotated Pathway Files: ', \
                    justification='left', font=("Helvetica", 12))], 
                [sg.InputText(key='-Output Dir-'), sg.FolderBrowse()],
                [sg.Text("")],
                [sg.Text('Optional Parameters', justification='left', \
                    font=("Helvetica", 15))],
                [sg.Text('----------------------------', justification='left', \
                    font=("Helvetica", 15))],
                [sg.Text(sup_protein_file_msg, justification='left', \
                    font=("Helvetica", 12))],
                [sg.InputText(key="protein abbrevs"), sg.FileBrowse()],
                [sg.Button("Help")],
                [sg.Button("Go")],
            ]

    window = sg.Window('Annotate KEGG Pathway', layout)      
    # Window for Select Protein Column Names     
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Help":
            sg.popup(help_msg, title="Help")
        elif event == "Go":
            err = False
            if values['KEGG-Pathway'] == "":
                err = True
                msg = "Please Select a KEGG-Pathway to Annotate"
                print(msg)
                sg.popup(msg)
            elif values['KEGG-Pathway'].split('.')[-1] != "htm":
                if values['KEGG-Pathway'].split('.')[-1] != "html":
                    err = True
                    msg = "KEGG-Pathway File Must be a .htm or .html File"
                    print(msg)
                    sg.popup(msg)
            elif values['-Output Dir-'] == "":
                err = True
                msg = "Please Select an Output Directory for the Annotated "
                msg += "KEGG-Pathway"
                print(msg)
                sg.popup(msg)
            elif values['protein abbrevs'] != "" \
            and values['protein abbrevs'].split(".")[-1] != "txt":
                err = True
                msg = "File Containing Protein Abbreviations Must be a .txt File"
                print(msg)
                sg.popup(msg)
            if not err:
                # Read protein abbreviations to add to Genome Annotatoin
                proteins = {}
                protein_abbrev = set(())
                if values['protein abbrevs'] != "":
                    protein_abbrev = read_protein_abbrevs(values['protein abbrevs'].replace("/","\\"))
                proteins['abbrevs'] = protein_abbrev
                # Read EC Numbers from Genome Annotations
                for i in range(orgi_values['num_annotations']):
                    annot_name = "Genome Annotation " + str(i + 1)
                    annot_col = annot_name + " col"
                    annot = orgi_values[annot_name].replace("/","\\")
                    col_name = orgi_values[annot_col]
                    proteins[annot_name] = read_genome_annot_EC(annot, col_name)
                # Read KEGG-Pathway
                kegg_pathway_path = values['KEGG-Pathway'][:values['KEGG-Pathway'].rfind("/") + 1]
                kegg_pathway_path = kegg_pathway_path.replace("/", "\\")
                pathwayName = values['KEGG-Pathway'][values['KEGG-Pathway'].rfind("/") \
                    +1:values['KEGG-Pathway'].rfind(".")]
                # Format Output Dir Filepath
                outDir = values['-Output Dir-'].replace("/","\\")
                # Annotate the Pathway
                webExt = values['KEGG-Pathway'][values['KEGG-Pathway'].rfind("."):]
                annotated_filepath = annotate_pathway(pathwayName, kegg_pathway_path, \
                    outDir, proteins, webExt)
                msg = "Annotation of '" + pathwayName + "' is "
                msg += "Complete!"
                
                sg.popup_ok(msg, title="Pathway Annotation Complete")
                # Launch the webpage
                url = "file:///" + annotated_filepath
                webbrowser.open(url, new=2)  # open in new tab
                window.close()
    
    
def launch_select_genome_annots_window():
    """
    Launches the window for selecting the genome annotations to use.
    
    :param num_annotations: The number of Genome Annotations to use
    :param values: The input values from the window
    """
    help_msg  = "This window is where you select the genome annotations that you "
    help_msg += "want to use to annotate the KEGG-Pathway. You can use up to 5 "
    help_msg += "genome annotations. First enter the number of annotations you "
    help_msg += "wish to use, then click the 'Confirm Number of Genome "
    help_msg += "Annotations' button. Afterwards, some filebrowse widgets will "
    help_msg += "appear. Use them to select the genome annotations that you "
    help_msg += "want to use. Please note that the genome annotations must be "
    help_msg += "excel files of a .xls or .xlsx format. When finished, click "
    help_msg += "next."
    layout = create_genome_annote_layout()
    window = sg.Window('Annotate KEGG Pathway', layout)

    # Window for Selecting the Genome Annotations
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Confirm Number of Genome Annotations":
            num_annotations = int(values["num_annotations"])
            layout = create_genome_annote_layout(num_annotations=num_annotations, \
                values=values)
            window.close()
            window = sg.Window('Annotate KEGG Pathway', layout)
        elif event == "Help":
            sg.popup(help_msg, title="Help")
        elif event == "Next":
            if genome_annotations_good(num_annotations, values):
                window.close()
                launch_select_protein_column_names_window(values)
    
    
def launch_select_protein_column_names_window(values):
    """
    Launches the window for selecting the protein column names for genome 
    annotations.
    
    :param values: The input values from the window
    """
    help_msg  = "This window is where you select the column names that you "
    help_msg += "would expect to find the protein EC Numbers in for each of "
    help_msg += "the genome annotations you entered. To see a list of column "
    help_msg += "header names, click the dropdown menus next to each of the "
    help_msg += "genome annotations. When finished, click 'Next'."
    orgi_vals = values.copy()
    layout =    [
                [sg.Text('Annotate-KEGG-Pathway', size=(35, 1), \
                    justification='center', font=("Helvetica", 25), \
                    relief=sg.RELIEF_RIDGE)], 
                [sg.Text('Specify Protein Columns for Genome Annotations', \
                    justification='left', font=("Helvetica", 15))],
                [sg.Text('--------------------------------------------------------', \
                    justification='left', font=("Helvetica", 15))],
            ]
    for i in range(values['num_annotations']):
        annot_name = "Genome Annotation " + str(i + 1)
        if annot_name in values.keys():
            filepath = values[annot_name]
            filename = filepath.split("/")[-1]
            col_labels = read_header(filepath)
            key = annot_name + " col"
            menu_cols = tuple(col_labels)
            layout += [sg.Text(annot_name + ": " + filename, \
                justification='left', font=("Helvetica", 12))], \
                [sg.Text("Select Column Containing Protein EC Numbers"), \
                sg.InputOptionMenu(menu_cols, key=key)], [sg.Text("")], 
    layout += [sg.Button("Help")],
    layout += [sg.Button("Next")],
        
    window = sg.Window('Annotate KEGG Pathway', layout)      
    # Window for Select Protein Column Names     
    while True:
        event, values = window.read()
        err = False
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Help":
            sg.popup(help_msg, title="Help")
        elif event == "Next":
            for i in range(orgi_vals['num_annotations']):
                annot_name = "Genome Annotation " + str(i + 1)
                col = annot_name + " col"
                if values[col] == "":
                    err = True
                    msg = "Please select column for " + annot_name
                    print(msg)
                    sg.popup_ok(msg)
            if not err:
                values = {**values, **orgi_vals}
                window.close()
                launch_final_window(values)
    

layout = [
    [sg.Text(welcome_msg)],
    [sg.Text('Select RAST Excel Spreadsheet Genome Annotation: '), \
        sg.InputText(key='-RAST_file-'), sg.FileBrowse(key="annotation_1")],
    [sg.Text('Select PATRIC Excel Spreadsheet Genome Annotation: '), \
        sg.InputText(key='-PATRIC_file-'), sg.FileBrowse()],
    [sg.Text('Select Input Pathway .htm File to Annotate: '), \
        sg.InputText(key='-Input Pathway-'), sg.FileBrowse()],
    [sg.Text('Select Output Directory for Annotated Pathway Files: '), \
        sg.InputText(key='-Output Dir-'), sg.FolderBrowse()],
    [sg.Button("Go")],
    [sg.Button("Help")],
]


launch_select_genome_annots_window()