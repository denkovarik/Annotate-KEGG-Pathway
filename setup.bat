:: This batch file installs the dependencies for the project
ECHO OFF
:: Update PIP
call py -m pip install --upgrade pip
:: Install Pandas
call py -m pip install pandas
:: Install Pillow
call py -m pip install Pillow
:: Install openpyxl
call py -m pip install openpyxl
:: Install xlrd
call py -m pip install xlrd
:: Install PySimpleGUI
call py -m pip install PySimpleGUI