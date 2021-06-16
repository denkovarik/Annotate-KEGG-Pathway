import unittest
import io
import os, sys, inspect
import unittest
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)  
from utils import *


class allTests(unittest.TestCase):
    """
    Runs all te tests for the class.                                               
    """
    def test_Execution(self):
        """
        Tests tha ability of the class to run a test.
        
        :param self: Instance of the allTests class.
        """
        self.assertTrue(2 == 2)
        
     
    def test_file_ext_good(self):
        """
        Tests tha ability of the function 'file_ext_good' on its ability 
        to determine if a file has the correct extension.
        
        :param self: Instance of the allTests class.
        """
        self.assertTrue(file_ext_good("test.txt", "txt"))
        self.assertFalse(file_ext_good("test.txt", "htm"))
       
       
    def test_is_RAST_spreadsheet(self):
        """
        Tests tha ability of the function 'is_RAST_spreadsheet' on its 
        ability to determine if a file is an excel spreadsheet of genome 
        annotation from RAST.
        
        :param self: Instance of the allTests class.
        """
        filepath_RAST = currentdir +  '\\RAST_Geobacillus_LC41.xls'
        filepath_PATRIC = currentdir +  '\\PATRIC_genome_feature.xlsx'
        filepath_txt = currentdir +  '\\proteinAbbrev.txt'
        self.assertTrue(is_RAST_spreadsheet(filepath_RAST))
        self.assertFalse(is_RAST_spreadsheet(filepath_PATRIC))
        self.assertFalse(is_RAST_spreadsheet(filepath_txt))
        
        
    def test_is_PATRIC_spreadsheet(self):
        """
        Tests tha ability of the function 'is_PATRIC_spreadsheet' on its 
        ability to determine if a file is an excel spreadsheet of genome 
        annotation from PATRIC.
        
        :param self: Instance of the allTests class.
        """
        filepath_RAST = currentdir +  '\\RAST_Geobacillus_LC41.xls'
        filepath_PATRIC = currentdir +  '\\PATRIC_genome_feature.xlsx'
        filepath_txt = currentdir +  '\\proteinAbbrev.txt'
        self.assertFalse(is_PATRIC_spreadsheet(filepath_RAST))
        self.assertTrue(is_PATRIC_spreadsheet(filepath_PATRIC))
        self.assertFalse(is_PATRIC_spreadsheet(filepath_txt))
        
        
    def test_read_protein_abbrevs(self):
        """
        Tests tha ability of the function 'read_protein_abbrevs' on its 
        ability to read a txt file containing protein abbreviations.
        
        :param self: Instance of the allTests class.
        """
        expected = set(('LysR', 'ClpC', 'GroEL', 'MecA', 'GroES', 'Spo0F', \
        'KefA', 'HU', 'MutS', 'Csp', 'Cas6', 'YaaT', 'PTS', 'YtnP', 'Spo0B', \
        'ArsR', 'YmcA', 'RuvB', 'RuvA', 'LuxR', 'DegS', 'KtrD', 'BpsA', \
        'DnaK', 'KQT', 'EpsD', 'KtrC', 'EpsC', 'RecA', 'DnaJ', 'ACR3', \
        'YlbF', 'DegU', 'Spo0A', 'AbrB', 'RecR', 'MutL', 'UvrD', 'OpuD'))
        filepath_txt = currentdir +  '\\proteinAbbrev.txt'
        filepath_PATRIC = currentdir +  '\\PATRIC_genome_feature.xlsx'
        try:
            read_protein_abbrevs(filepath_PATRIC)
        except:
            self.assertTrue(True)
        try:
            proteins = read_protein_abbrevs(filepath_txt)
            self.assertTrue(expected == proteins)
        except:
            self.assertTrue(False)
            
            
    def test_read_RAST_EC_Nums(self):
        """
        Tests tha ability of the function 'read_RAST_EC_Nums' to read and 
        return a set of EC numbers for an excel spreadsheet of a genome 
        annotation completed by RAST.
        
        :param self: Instance of the allTests class.
        """
        filepath_RAST = currentdir +  '\\RAST_Geobacillus_LC41.xls'
        filepath_PATRIC = currentdir +  '\\PATRIC_genome_feature.xlsx'
        filepath_txt = currentdir +  '\\proteinAbbrev.txt'
        expected = set(('4.1.3.36', '4.2.3.130', '4.2.1.1', '2.7.7.27', \
        '5.4.4.2', '6.2.1.26', '2.5.1.6', '2.2.1.9', '2.4.1.21', '2.7.7.7', \
        '4.1.1.49', '2.4.1.18', '2.4.1.1', '2.5.1.74', '4.2.99.20', \
        '4.4.1.21'))
        self.assertTrue(expected == read_RAST_EC_Nums(filepath_RAST))
        try:
            read_RAST_EC_Nums(filepath_PATRIC)
        except:
            self.assertTrue(True)
        try:
            read_RAST_EC_Nums(filepath_txt)
        except:
            self.assertTrue(True)
            
            
    def test_read_PATRIC_EC_Nums(self):
        """
        Tests tha ability of the function 'read_PATRIC_EC_Nums' to read and 
        return a set of EC numbers for an excel spreadsheet of a genome 
        annotation completed by PATRIC.
        
        :param self: Instance of the allTests class.
        """
        expected = set(('6.1.1.1', '2.7.1.205', '5.99.1.3', '6.3.5.10', \
        '1.7.99.4', '4.2.1.8', '5.3.1.12', '1.1.1.261', '4.3.1.18', \
        '2.7.1.45', '2.1.1.151', '2.1.1.271', '3.7.1.12', '6.3.5.11', \
        '2.1.1.289', '4.1.2.29', '2.1.1.107', '2.7.1.56', '3.4.11.18', \
        '1.5.1.3', '4.3.1.19', '3.4.11.4', '2.1.1.195', '2.1.1.45', \
        '2.3.1.79', '5.1.3.4', '4.2.1.44', '4.2.1.17', '6.2.1.1', \
        '4.1.3.16', '2.7.1.202', '3.2.1.55', '2.5.1.17', '2.1.1.272', \
        '4.2.1.75', '1.1.1.192', '2.3.1.n3', '3.1.4.46', '1.2.7.1', \
        '1.7.99.6', '3.2.1.131', '3.7.1.22', '1.1.1.18', '1.11.1.9', \
        '6.3.4.21', '1.1.1.57', '2.7.1.17', '5.3.1.30', '3.6.3.19', \
        '1.2.1.18', '2.3.1.46', '3.6.3.3', '5.1.3.3', '5.4.99.60', \
        '5.3.1.5', '3.2.1.8', '5.3.1.4', '2.4.1.157', '2.4.2.21', \
        '2.4.1.129', '4.99.1.3', '5.99.1.2', '2.4.1.18', '1.3.1.106', \
        '2.7.1.92', '3.5.1.19', '3.2.1.86', '2.7.1.16', '3.1.3.25', \
        '3.2.1.37'))
        filepath_RAST = currentdir +  '\\RAST_Geobacillus_LC41.xls'
        filepath_PATRIC = currentdir +  '\\PATRIC_genome_feature.xlsx'
        filepath_txt = currentdir +  '\\proteinAbbrev.txt'
        proteins = read_PATRIC_EC_Nums(filepath_PATRIC)
        self.assertTrue(proteins == expected)
        
        
    def test_get_pathway_filepaths(self):
        """
        Tests tha ability of the function 'get_pathway_filepaths' to download and save a complete KEGG webpage to the local device in the 
        testing\testDownloads folder.
        
        :param self: Instance of the allTests class.
        """
        expected = set(('KEGG PATHWAY Terpenoid backbone biosynthesis - Reference pathway', 'KEGG PATHWAY Lysine biosynthesis - Reference pathway', 'KEGG PATHWAY Biofilm formation - Escherichia coli - Reference pathway', 'KEGG PATHWAY Pentose phosphate pathway - Reference pathway', 'KEGG PATHWAY Citrate cycle (TCA cycle) - Reference pathway', 'KEGG PATHWAY Thiamine metabolism - Reference pathway', 'KEGG PATHWAY Valine, leucine and isoleucine biosynthesis - Reference pathway', 'KEGG PATHWAY Vitamin B6 metabolism - Reference pathway', 'KEGG PATHWAY Biotin metabolism - Reference pathway', 'KEGG PATHWAY Glyoxylate and dicarboxylate metabolism - Reference pathway', 'KEGG PATHWAY ABC transporters - Reference pathway', 'KEGG PATHWAY Phenylalanine, tyrosine and tryptophan biosynthesis - Reference pathway', 'KEGG PATHWAY Quorum sensing - Reference pathway', 'KEGG PATHWAY Glycolysis _ Gluconeogenesis - Reference pathway', 'KEGG PATHWAY Riboflavin metabolism - Reference pathway'))
        pathwaysPath = currentdir + "\\pathways2"
        result = get_pathway_filepaths(pathwaysPath)
        self.assertTrue(result == expected)
        
 
if __name__ == '__main__':
    unittest.main()