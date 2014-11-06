import unittest;
import motus;

class MotusTest(unittest.TestCase):
    def test_validate_description(self):
        self.assertRaises(motus.ParameterInvalid, motus.Motus, desc='') 

    def test_validate_acttivations(self):
        self.assertRaises(motus.ParameterInvalid, motus.Motus, desc='aaa', activations=0)
    
    def test_validade_configurations(self):
        self.assertRaises(motus.ParameterInvalid, motus.Motus, desc='bbb', activations = 4, configs=[(5, 3)])

    def test_select_parameter(self):
        self.assertRaises(motus.ParameterInvalid, motus.Motus, desc='ccc', activations = 5, configs=[], out_index=1)

    def test_out_index(self):
        self.assertRaises(motus.ParameterInvalid, motus.Motus, desc='ccc', activations = 5, configs=[], out_index=None)
