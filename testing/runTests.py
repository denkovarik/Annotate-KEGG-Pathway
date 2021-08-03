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
    def test_read_protein_abbrevs(self):
        """
        Tests utility function on ability to read txt file of line separated 
        protein abbreviations.
        
        :param self: An instance of the allTests class.
        """
        filepath = currentdir + "\\test_protein_abbrevs\\testProteinAbbrev.txt"
        self.assertTrue(os.path.isfile(filepath))
        rslt = read_protein_abbrevs(filepath)
        exp = set(("eutg", "ispe"))
        for ec in rslt:
            self.assertTrue(ec.lower() in exp)
        
        
    def test_read_genome_annot_EC(self):
        """
        Tests utility function on ability to read a genome annotation and 
        extract the ec numbers from them.
        
        :param self: An instance of the allTests class.
        """
        annot = currentdir + "\\test_genome_annotations\\RAST_Geobacillus_sp_WSUCF1_small.xlsx"
        self.assertTrue(os.path.isfile(annot))
        expected = set(('1.15.1.1', '3.6.4.13', '3.1.21.2', '1.17.7.4', '1.17.7.3'))
        col_name = 'function'
        rslt = read_genome_annot_EC(annot, col_name)
        self.assertTrue(rslt == expected)
        # Every protein in Gluconeogenesis pathway on KEGG
        annot = currentdir + "\\test_genome_annotations\\RAST_Geobacillus_sp_WSUCF1.xlsx"
        self.assertTrue(os.path.isfile(annot))
        expected = set(('5.4.2.2', '2.7.1.199', '2.7.1.2','5.3.1.9', '3.1.3.11','2.7.1.11', '4.1.2.13','2.7.1.-','3.2.1.86','4.1.2.13','5.3.1.1','1.2.1.12','2.7.2.3','5.4.2.12','4.2.1.11','4.1.1.49','2.7.1.40','1.2.7.1','2.3.1.12','1.2.4.1','1.1.1.27','6.2.1.1','1.8.1.4','1.1.1.1','1.2.1.3'))
        not_expected = set(('3.1.3.10','3.1.3.9','2.7.1.63','2.7.1.147','5.1.3.3','5.1.3.15','2.7.1.146','2.7.1.90','1.2.1.59','1.2.1.9','1.2.7.6','5.4.2.4','1.2.1.90','5.4.2.11','3.1.3.80','4.1.1.32','1.2.7.11','2.7.9.1','2.7.9.2','6.2.1.13','1.1.5.5','1.1.2.7','1.1.2.8','1.2.1.5','1.2.1.-','2.7.1.1','1.1.1.2','4.1.1.1'))
        rslt = read_genome_annot_EC(annot, col_name)
        for ec in expected:
            self.assertTrue(ec in rslt)
        for ec in not_expected:
            self.assertFalse(ec in rslt)
        
        
        
    def test_ec_strip(self):
        """
        Tests utility function on ability to strip an ec number of chars that 
        are not part of an EC number.
        
        :param self: An instance of the allTests class.
        """
        test1 = "2.7.7.7"
        test2 = "3.1.3.-"
        test3 = "3.5.-.-"
        test4 = "2.7.7.7)"
        test5 = "(1.1.1.1"
        test6 = "1.1.1.1("
        test7 = ")2.7.7.7"
        test8 = "(1.1.1.1("
        test9 = "(1.1.1.1)"
        test10 = "ec 2.7.7.7"
        test11 = "ec: 2.7.7.7"
        test12 = "ec2.7.7.7"
        test13 = "ec:2.7.7.7"
        test14 = "(ec 2.7.7.7)"
        test15 = "(ec: 2.7.7.7)"
        test16 = "(ec2.7.7.7)"
        test17 = "(ec:2.7.7.7)"
        test18 = "  2.7.7.7      "
        test19 = "2.7.7.7."
        test20 = "2.7.7.7. Hi"
        test21 = "2.7.7.7.Hi"
        test22 = "2.7.7.7.8"
        
        self.assertTrue(ec_strip(test1) == "2.7.7.7")
        self.assertTrue(ec_strip(test2) == "3.1.3.-")
        self.assertTrue(ec_strip(test3) == "3.5.-.-")
        self.assertTrue(ec_strip(test4) == "2.7.7.7")
        self.assertTrue(ec_strip(test5) == "1.1.1.1")
        self.assertTrue(ec_strip(test6) == "1.1.1.1")
        self.assertTrue(ec_strip(test7) == "2.7.7.7")
        self.assertTrue(ec_strip(test8) == "1.1.1.1")
        self.assertTrue(ec_strip(test9) == "1.1.1.1")
        self.assertTrue(ec_strip(test10) == "2.7.7.7")
        self.assertTrue(ec_strip(test11) == "2.7.7.7") 
        self.assertTrue(ec_strip(test12) == "2.7.7.7")
        self.assertTrue(ec_strip(test13) == "2.7.7.7")
        self.assertTrue(ec_strip(test14) == "2.7.7.7")
        self.assertTrue(ec_strip(test15) == "2.7.7.7")
        self.assertTrue(ec_strip(test16) == "2.7.7.7")
        self.assertTrue(ec_strip(test17) == "2.7.7.7")
        self.assertTrue(ec_strip(test18) == "2.7.7.7")
        self.assertTrue(ec_strip(test19) == "2.7.7.7")
        self.assertTrue(ec_strip(test20) == "2.7.7.7")
        self.assertTrue(ec_strip(test21) == "2.7.7.7")
        self.assertTrue(ec_strip(test22) == "")
        
       
    def test_is_ec(self):
        """
        Tests utility function on determining if a string is an ec number
        or not.
        
        :param self: An instance of the allTests class.
        """
        test0 = ""
        test1 = "Hi there"
        test2 = "EC"
        test3 = "2.EC"
        test4 = "2.E.C.C"
        test5 = "2.E.C.7"
        test6 = "2.7.7.7"
        test7 = "3.1.3.-"
        test8 = "3.5.-.-"
        test9 = "2.7.7.7"
        test10 = "7.023"
        test11 = "8.21..5"
        test12 = "(1.1.1.1"
        test13 = "1.1.1.1("
        test14 = "1.(1.1.1"
        test15 = "2.7.7.7)"
        test16 = ")2.7.7.7"
        test17 = "2.7).7.7"
        test18 = "(1.1.1.1("
        test19 = "(1.1.(1.1("
        test20 = "(1.1.)1.1("
        test21 = "(1.1.1.1)"
        self.assertFalse(is_ec(test0))
        self.assertFalse(is_ec(test1))
        self.assertFalse(is_ec(test2))
        self.assertFalse(is_ec(test3))
        self.assertFalse(is_ec(test4))
        self.assertFalse(is_ec(test5))
        self.assertTrue(is_ec(test6))
        self.assertTrue(is_ec(test7))
        self.assertTrue(is_ec(test8))
        self.assertTrue(is_ec(test9))
        self.assertFalse(is_ec(test10))
        self.assertFalse(is_ec(test11))
        self.assertTrue(is_ec(test12))
        self.assertTrue(is_ec(test13))
        self.assertFalse(is_ec(test14))
        self.assertTrue(is_ec(test15))
        self.assertTrue(is_ec(test16))
        self.assertFalse(is_ec(test17))
        self.assertTrue(is_ec(test18))
        self.assertFalse(is_ec(test19))
        self.assertFalse(is_ec(test20))
        self.assertTrue(is_ec(test21))
        
        
    def test_extract_ec(self):
        """
        Tests utility function on extracting the ec number from a string.
        
        :param self: An instance of the allTests class.
        """
        test1 = "hypothetical protein"
        test2 = "DNA polymerase IV (EC 2.7.7.7)"
        test3 = "Sigma-X negative effector (EC 3 and more)"
        test4 = "Hypothetical protein TEPIRE1_21570 (predicted: PeP phosphonomutase (predicted EC 2.7.8.23) (predicted EC 4.1.3.30))"
        test5 = "Glutaminase (EC 3.5.-.-)"
        test6 = "Histidinol-phosphatase (EC 3.1.3.-)"
        test7 = " (predicted EC 2.3.1.1)"
        test8 = "hypothetical protein (predicted: MULTISPECIES: GNAT family N-acetyltransferase [Geobacillus] (predicted EC 2.3.1.1))"
        test9 = "Aminodeoxychorismate lyase, EC 4.1.3.38"
        test10 = "Aminodeoxychorismate lyase, EC: 4.1.3.38"
        test11 = "Aminodeoxychorismate lyase, EC: -.-.-.-"
        test12 = "Histidinol-phosphatase (EC -.1.3.1)"
        test13 = "DNA polymerase IV (Web Scaped EC 2.7.7.7)"
        test14 = "Hypothetical protein TEPIRE1_21570 (predicted: PeP phosphonomutase (predicted EC 2.7.8.23) (predicted EC: 4.1.3.30))"
        test15 = "Hypothetical protein TEPIRE1_21570 (predicted: PeP phosphonomutase (predicted EC 2.7.8.23) (predicted EC: 4.1.3.30)) (predicted: PeP phosphonomutase (predicted EC3.7.8.23) (predicted EC:9.1.3.30)"
        self.assertTrue(extract_ec(test1) == set(()))
        self.assertTrue(extract_ec(test2) == set(("2.7.7.7",)))
        self.assertTrue(extract_ec(test3) == set(()))
        self.assertTrue(extract_ec(test4) == set(("2.7.8.23","4.1.3.30")))
        self.assertTrue(extract_ec(test5) == set(("3.5.-.-",)))
        self.assertTrue(extract_ec(test6) == set(("3.1.3.-",)))
        self.assertTrue(extract_ec(test7) == set(("2.3.1.1",)))    
        self.assertTrue(extract_ec(test8) == set(("2.3.1.1",)))
        self.assertTrue(extract_ec(test9) == set(("4.1.3.38",)))
        self.assertTrue(extract_ec(test10) == set(("4.1.3.38",)))
        self.assertTrue(extract_ec(test11) == set(()))
        self.assertTrue(extract_ec(test12) == set(()))
        self.assertTrue(extract_ec(test13) == set(("2.7.7.7",)))
        self.assertTrue(extract_ec(test14) == set(("2.7.8.23","4.1.3.30",)))
        self.assertTrue(extract_ec(test15) == set(("2.7.8.23","4.1.3.30","3.7.8.23","9.1.3.30",)))
        
        
    def test_has_ec(self):
        """
        Tests utility function on determining if a gene already has an 
        associated ec number.
        
        :param self: An instance of the allTests class.
        """
        test1 = "hypothetical protein"
        test2 = "DNA polymerase IV (EC 2.7.7.7)"
        test3 = "Sigma-X negative effector (EC 3 and more)"
        test4 = "Hypothetical protein TEPIRE1_21570 (predicted: PeP phosphonomutase (predicted EC 2.7.8.23) (predicted EC 4.1.3.30))"
        test5 = "Glutaminase (EC 3.5.-.-)"
        test6 = "Histidinol-phosphatase (EC 3.1.3.-)"
        test7 = " (predicted EC 2.3.1.1)"
        test8 = "hypothetical protein (predicted: MULTISPECIES: GNAT family N-acetyltransferase [Geobacillus] (predicted EC 2.3.1.1))"
        test9 = "Aminodeoxychorismate lyase, EC 4.1.3.38"
        test10 = "Aminodeoxychorismate lyase, EC: 4.1.3.38"
        test11 = "Aminodeoxychorismate lyase, EC: -.-.-.-"
        test12 = "Histidinol-phosphatase (EC -.1.3.1)"
        test13 = "DNA polymerase IV (Web Scaped EC 2.7.7.7)"
        
        self.assertFalse(has_ec(test1))
        self.assertTrue(has_ec(test2))
        self.assertFalse(has_ec(test3))
        self.assertTrue(has_ec(test4))
        self.assertTrue(has_ec(test5))
        self.assertTrue(has_ec(test6))
        self.assertTrue(has_ec(test7))
        self.assertTrue(has_ec(test8))
        self.assertTrue(has_ec(test9))
        self.assertTrue(has_ec(test10))
        self.assertFalse(has_ec(test11))
        self.assertFalse(has_ec(test12))
        self.assertTrue(has_ec(test13))
        
        
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
        
        
    def test_read_header(self):
        """
        Tests the ability of the utility function 'read_header()' on its
        ability to read the header of a genome annotation and return the column
        names.
        
        :param self: Instance of the allTests class.
        """
        # RAST genome annoation .xls format
        filename = "RAST_Geobacillus_sp_WSUCF1.xls"
        annot1_path = currentdir + "\\test_genome_annotations\\" + filename
        self.assertTrue(os.path.isfile(annot1_path))
        exp = ['contig_id', 'feature_id', 'type', 'location', 'start', 'stop', \
            'strand', 'function', 'aliases', 'figfam', 'evidence_codes', \
            'nucleotide_sequence', 'aa_sequence']
        header = read_header(annot1_path)
        self.assertTrue(header == exp)
        # RAST genome annoation .xlsx format
        filename = "RAST_Geobacillus_sp_WSUCF1.xlsx"
        annot1_path = currentdir + "\\test_genome_annotations\\" + filename
        self.assertTrue(os.path.isfile(annot1_path))
        exp = ['contig_id', 'feature_id', 'type', 'location', 'start', 'stop', \
            'strand', 'function', 'aliases', 'figfam', 'evidence_codes', \
            'nucleotide_sequence', 'aa_sequence']
        header = read_header(annot1_path)
        self.assertTrue(header == exp)
        # PATRIC genome annoation .xlsx format
        filename = "PATRIC_genome_feature_Geobacillus_sp_WSUCF1.xlsx"
        annot1_path = currentdir + "\\test_genome_annotations\\" + filename
        self.assertTrue(os.path.isfile(annot1_path))
        exp = ['Genome', 'Genome ID', 'Accession', 'PATRIC ID', \
            'RefSeq Locus Tag', 'Alt Locus Tag', 'Feature ID', 'Annotation', \
            'Feature Type', 'Start', 'End', 'Length', 'Strand', 'FIGfam ID', \
            'PATRIC genus-specific families (PLfams)', \
            'PATRIC cross-genus families (PGfams)', 'Protein ID', 'AA Length', \
            'Gene Symbol', 'Product', 'GO']
        header = read_header(annot1_path)
        self.assertTrue(header == exp)
        
 
if __name__ == '__main__':
    unittest.main()