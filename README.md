# Annotate-KEGG-Pathway

<img src="https://github.com/denkovarik/Annotate-KEGG-Pathway/blob/main/images/biochem_pathway_intro.jpg" width="500" />

## Introduction
This project was designed to help researchers use the biochemical pathways on KEGG (KEGG pathways) to analyze the genome of an organism. Specifically, it indicates which proteins from a KEGG pathway are present in an organism's genome. This project reads the excel file from an organism's genome annotation(s) and records the EC numbers for the proteins present in them. This program will take up to 5 genome annotations. It will also take another text file containing line separated protein abbreviations that you also want to include for the annotation of the KEGG-Pathway (sometimes protein abbreviations are used in KEGG-Pathways). Please note that this program will not look for protein abbreviations in the genome annotations. The program will then parse the html file of a KEGG pathway to determine the protein abbreviations and the EC numbers of the proteins present in the pathway. The program compares the proteins from the KEGG pathway to the proteins found in the organism's genome annotation and text files. Proteins from the genome annotation that are also found to be present in the KEGG Pathway are indicated by colored boxes around the protein's EC Number in the KEGG Pathway. For the annotated KEGG-Pathway, an EC number has a green rectangle drawn around it if the EC Number was present in all genome annotations given, and a yellow rectangle will be drawn around EC Numbers that were only present in some but not all of the genome annotations given. Protein abbreviations found in both the KEGG-Pathway and the supplemental protein abbreviation text file will always have yellow boxes drawn around them. When completed, the annotated KEGG pathway will be saved to your local computer, and it will open up in your browser as a working webpage.

## Setup
This project was developed for the Window's Operating System on a 64 bit machine.

### Dependencies
* Git
* Python 3
* pillow
* pandas
* openpyxl
* PySimpleGUI
* xlrd

### Install Git on Windows
The first thing you need to do is to make sure that Git is installed on your device. This will allow you to clone and download this repository on your device. If necessary, the tutorial [Install Git](https://github.com/git-guides/install-git) will walk you through how to do this.

### Install Python 3.9
This project relies on Python 3.9 to run and PIP to install other dependencies. You can download Python via this link, [Python 3.9 Download](https://www.python.org/downloads/). Once the download is complete, launch the installer. 

Make sure that you check the box 'Add Python 3.9 to PATH'.\

![Python Setup](https://github.com/denkovarik/Annotate-KEGG-Pathway/blob/main/images/Python_install.PNG)

Otherwise, use all the default parameters and just click through the setup wizard to install Python. Once the install is complete, you can verify if python was installed correctly by doing the following. Close out of the command prompt if open an then run it again. Then type 'py' and press Enter on the command prompt to invoke python. 

![Invoke Python](https://github.com/denkovarik/Annotate-KEGG-Pathway/blob/main/images/invoke_python.PNG)

If you get something like the above image, then python was installed correctly. Otherwise, something went wrong with your installation of Python. Try reinstalling it.

### Cloning This Repo with HTTPS
To download this repository on your device, you must clone this repo using either HTTPS or SSH. The easiest way to clone this repository on your local device is through HTTPS. If your SDK allows you to clone a repo through HTTPS, then do so. Otherwise, you can do it directly on the command prompt. To do so, open up the command prompt and move into the desired directory. Then simply run the following command and press Enter.

```
git clone https://github.com/denkovarik/Annotate-KEGG-Pathway.git
```

Enter in your credentials if prompted to do so. After the repo has been cloned on your device, move into the Annotate-KEGG-Pathway directory from the command line.

```
cd Annotate-KEGG-Pathway
```

### Cloning This Repo with SSH
You can also clone this repo using SSH. Follow the instructions below to clone the repo using SSH. Please note that if you have already cloned the repo using HTTPS, then you can skip to the 'Install Dependencies' step. If you wish to clone this repo using SSH, then please note that you will need an account on Github or Gitlab.

#### Generate an SSH Key Pair
In order to clone this repository, you need to add your public SSH key to this repo. If you don't have one, then you would need to generate one. [How to Generate SSH key in Windows 10? Easy Methods!!](https://techpaal.com/how-to-generate-ssh-key-in-windows-10-easy-methods/) should help you generate an SSH key pair.

#### Add Your Public SSH Key to GitHub
Once you have an SSH Key Pair generated, you need to add your public SSH key to GitHub. Follow [How to view your SSH keys in Linux, macOS, and Windows](https://www.techrepublic.com/article/how-to-view-your-ssh-keys-in-linux-macos-and-windows/) to access you public key. Then follow [Adding a new SSH key to your GitHub account](https://docs.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account) to add your public SSH key to GitHub.

#### Clone the Repository
If your SDK allows for it, then clone this repository through your SDK. Otherwise, open up the command prompt, move into the directory of your choice, then run the following command.
```
git clone git@github.com:denkovarik/Annotate-KEGG-Pathway.git
```
After the repo has been cloned on your device, move into the Annotate-KEGG-Pathway directory from the command line.
```
cd Annotate-KEGG-Pathway
```

### Install Dependencies
Next, install the dependencies needed for the project. This can be done by simply running 'setup.bat' by doulble clicking on it in the file explorer. Alternatively, you can run this script by executing the following command on the command line from within the project directory.
```
setup.bat
```

## Usage
### First downloaded the complete webpage of the KEGG Pathway you want to annotate and save it an a known location. 

1. On the KEGG homepage, select 'KEGG PATHWAY'. 

![KEGG Homepage](https://github.com/denkovarik/Annotate-KEGG-Pathway/blob/main/images/KEGG_homepage.png)

2. Then enter a biochemical pathway that you want to annotate. In this example, we will annotate the Gluconeogenesis pathway.

![Search Pathways](https://github.com/denkovarik/Annotate-KEGG-Pathway/blob/main/images/Search_for_pathway.PNG)

3. Select the KEGG Pathway you want to annotate from the search results.

![Select KEGG Pathway](https://github.com/denkovarik/Annotate-KEGG-Pathway/blob/main/images/Select_KEGG_Pathway.PNG)

4. Right click on the page and select 'save as'.

![Download Pathway](https://github.com/denkovarik/Annotate-KEGG-Pathway/blob/main/images/download.png)

5. Select location to save the KEGG Pathway on local device. Please ensure that 'Webpage, complete' option is selected under the 'Save as type:' field.

![Download Webpage Complete](https://github.com/denkovarik/Annotate-KEGG-Pathway/blob/main/images/download_complete_webpage.png)

Please note that the saved pathway should consist of an .htm file and a folder containing more files and images. If the above steps were completed correctly, then you should be able to open the KEGG Pathway from file, and it should work as a functional webpage.

### Ensure that you have the RAST and/or PATRIC genome annotations for your organism
As of the writing of this article, this program requires a RAST and/or PATRIC genome annotaion for the organism. Please ensure that you have the excel files for these genome annotations in a known location.

![Genome Annotation Locations](https://github.com/denkovarik/Annotate-KEGG-Pathway/blob/main/images/genome%20annotations.png)

### Run Annotate-KEGG-Pathway

1. To start the program, run 'start.py'. This can be done by double clicking on 'start.py' in the file explorer. Alternativley, you can run it from the command line. To do so, open the command prompt, move into the project directory, and then run the following command on the command line.

```
py start.py
```

Upon startup, a window like the following will appear.

## Author
* Dennis Kovarik
