import unittest
import cmac

class TestCmac(unittest.TestCase):
    def setUp(self):
        inputs = []
	for i in range(9):
		inputs.append(cmac.Input(i, 'Attr ' + str(i), -10, 10))
        self.cmac = cmac.CMACLegProsthesis(active_sensory_cells = 4)
        self.data_loader = cmac.DataLoader(inputs, [9, 10, 11])
    
    def tearDown(self):
        self.cmac = None
        self.data_loader = None

    def test_train(self):
        self.cmac.train(self.data_loader)


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        inputs = []
	for i in range(9):
		inputs.append(cmac.Input(i, 'Attr ' + str(i), -10, 10))
        self.data_loader = cmac.DataLoader(inputs, [9, 10, 11])

    def tearDown(self):
        self.data_loader = None

    def test_input_data(self):
        self.assertTrue(len(self.data_loader.input_data) > 0, 'Input data not loaded')
        self.assertTrue(len(self.data_loader.input_data[0]) == 9, 'Number of inputs wrong!')

    def test_output_data(self):
        self.assertTrue(len(self.data_loader.output_data) > 0, 'Output data not loaded')
        self.assertTrue(len(self.data_loader.output_data[0]) == 3, 'Number of outputs wrong!')

    
