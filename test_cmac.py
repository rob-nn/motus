import unittest
import cmac

class TestCmac(unittest.TestCase):
    def setUp(self):
        self._sense_conf = cmac.SensoryCellConfig(0., 12., 13)
        self._sense_conf_2 = cmac.SensoryCellConfig(0., 1., 10)
        confs = []
        confs.append(self._sense_conf)
        confs.append(self._sense_conf_2)
        self._cmac = cmac.CMAC(confs, 4)

    def tearDown(self):
        self._sense_conf = None

    def test_mapping_address_first_value(self):
            self.assertTrue(self._sense_conf.mapping_address[0] == self._sense_conf.s_min)

    def test_mapping_address_last_value(self):
            self.assertTrue(self._sense_conf.mapping_address[-1] == self._sense_conf.s_max)
   
    def test_mapping_address_size(self):
            self.assertTrue(len(self._sense_conf.mapping_address) == 13)


    def test_mapping_all_lines(self):
        self.assertTrue(self._sense_conf.mapping[0].tolist() == [0, 1, 2, 3])
        self.assertTrue(self._sense_conf.mapping[1].tolist() == [4, 1, 2, 3])
        self.assertTrue(self._sense_conf.mapping[2].tolist() == [4, 5, 2, 3])
        self.assertTrue(self._sense_conf.mapping[3].tolist() == [4, 5, 6, 3])
        self.assertTrue(self._sense_conf.mapping[4].tolist() == [4, 5, 6, 7])
        self.assertTrue(self._sense_conf.mapping[5].tolist() == [8, 5, 6, 7])
        self.assertTrue(self._sense_conf.mapping[6].tolist() == [8, 9, 6, 7])
        self.assertTrue(self._sense_conf.mapping[7].tolist() == [8, 9, 10, 7])
        self.assertTrue(self._sense_conf.mapping[8].tolist() == [8, 9, 10, 11])
        self.assertTrue(self._sense_conf.mapping[9].tolist() == [12, 9, 10, 11])
        self.assertTrue(self._sense_conf.mapping[10].tolist() == [12, 13, 10, 11])
        self.assertTrue(self._sense_conf.mapping[11].tolist() == [12, 13, 14, 11])
        self.assertTrue(self._sense_conf.mapping[12].tolist() == [12, 13, 14, 15])
 

    def test_mapping_size(self):
        self.assertTrue(self._sense_conf.mapping.shape == (self._sense_conf.num_possible_values, self._sense_conf.num_active_cells))

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
