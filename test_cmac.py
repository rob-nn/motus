import unittest
import cmac

class TestCmac(unittest.TestCase):
    def setUp(self):
        self._cmac = cmac.CMAC(0., 12., 13, 4)

    def tearDown(self):
        self._cmac = None

    def test_mapping_address_first_value(self):
            self.assertTrue(self._cmac.mapping_address[0] == self._cmac.s_min)

    def test_mapping_address_last_value(self):
            self.assertTrue(self._cmac.mapping_address[-1] == self._cmac.s_max)
   
    def test_mapping_address_size(self):
            self.assertTrue(len(self._cmac.mapping_address) == 13)


    def test_mapping_all_lines(self):
        self.assertTrue(self._cmac.mapping[0].tolist() == [0, 1, 2, 3])
        self.assertTrue(self._cmac.mapping[1].tolist() == [4, 1, 2, 3])
        self.assertTrue(self._cmac.mapping[2].tolist() == [4, 5, 2, 3])
        self.assertTrue(self._cmac.mapping[3].tolist() == [4, 5, 6, 3])
        self.assertTrue(self._cmac.mapping[4].tolist() == [4, 5, 6, 7])
        self.assertTrue(self._cmac.mapping[5].tolist() == [8, 5, 6, 7])
        self.assertTrue(self._cmac.mapping[6].tolist() == [8, 9, 6, 7])
        self.assertTrue(self._cmac.mapping[7].tolist() == [8, 9, 10, 7])
        self.assertTrue(self._cmac.mapping[8].tolist() == [8, 9, 10, 11])
        self.assertTrue(self._cmac.mapping[9].tolist() == [12, 9, 10, 11])
        self.assertTrue(self._cmac.mapping[10].tolist() == [12, 13, 10, 11])
        self.assertTrue(self._cmac.mapping[11].tolist() == [12, 13, 14, 11])
        self.assertTrue(self._cmac.mapping[12].tolist() == [12, 13, 14, 15])
 

    def test_mapping_size(self):
        self.assertTrue(self._cmac.mapping.shape == (self._cmac.num_possible_values, self._cmac.num_active_cells))

 

class TestCmacLegProsthesis(unittest.TestCase):
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
if __name__ == '__main__':
    unittest.main()
