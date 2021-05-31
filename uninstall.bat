:: This batch file uninstalls all the dependencies for the project except for Python
:: Please note this script will not delete the project
ECHO OFF
:: Uninstall Pandas
call py -m pip uninstall pandas
:: Uninstall Pillow
call py -m pip uninstall Pillow
:: Uninstall openpyxl
call py -m pip uninstall openpyxl
:: Uninstall PySimpleGUI
call py -m pip uninstall PySimpleGUI