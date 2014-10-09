import unittest
import cmac
from numpy import *
import random

class TestCmac(unittest.TestCase):

    def setUp(self):
        self._sense_conf = cmac.SensoryCellConfig(0., 12., 13)
        self._sense_conf_2 = cmac.SensoryCellConfig(0.1, 1., 10)
        self._sense_conf_3 = cmac.SensoryCellConfig(-1, 1., 2)
        confs = []
        confs.append(self._sense_conf)
        confs.append(self._sense_conf_2)
	confs.append(self._sense_conf_3)
        self._cmac = cmac.CMAC(confs, 4)

    def tearDown(self):
        self._sense_conf = None

    def test_mapping_address_first_value(self):
        self.assertTrue(self._sense_conf.mapping_address[0] == self._sense_conf.s_min)

    def test_mapping_address_last_value(self):
        self.assertTrue(self._sense_conf.mapping_address[-1] == self._sense_conf.s_max)
   
    def test_mapping_address_size(self):
    	self.assertTrue(len(self._sense_conf.mapping_address) == 13)

    def test_mapping_address_all(self):
	self.assertTrue( \
		(around(self._sense_conf.mapping_address,0) == \
		around(array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11., 12.]),0)).all())
	self.assertTrue( \
		(around(self._sense_conf_2.mapping_address.tolist(), 1) == \
		around([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.], 1)).all())
    def test_get_index(self):
	self.assertTrue(self._cmac.get_index(0.25, self._sense_conf_2) == 1)
	self.assertTrue(self._cmac.get_index(1., self._sense_conf_2) == 9)
	self.assertTrue(self._cmac.get_index(5, self._sense_conf_2) == 9)
	self.assertTrue(self._cmac.get_index(0.1, self._sense_conf_2) == 0)
	self.assertTrue(self._cmac.get_index(0, self._sense_conf_2) == 0)
	self.assertTrue(self._cmac.get_index(0.95, self._sense_conf_2) == 8)
	self.assertTrue(self._cmac.get_index(0.4, self._sense_conf_2) == 3)


    def test_mapping_lines_sens_conf2(self):
        self.assertTrue(self._sense_conf_2.mapping[0].tolist() == [0, 1, 2, 3])
        self.assertTrue(self._sense_conf_2.mapping[1].tolist() == [4, 1, 2, 3])
        self.assertTrue(self._sense_conf_2.mapping[2].tolist() == [4, 5, 2, 3])
        self.assertTrue(self._sense_conf_2.mapping[3].tolist() == [4, 5, 6, 3])
        self.assertTrue(self._sense_conf_2.mapping[4].tolist() == [4, 5, 6, 7])
        self.assertTrue(self._sense_conf_2.mapping[5].tolist() == [8, 5, 6, 7])
        self.assertTrue(self._sense_conf_2.mapping[6].tolist() == [8, 9, 6, 7])
        self.assertTrue(self._sense_conf_2.mapping[7].tolist() == [8, 9, 10, 7])
        self.assertTrue(self._sense_conf_2.mapping[8].tolist() == [8, 9, 10, 11])
        self.assertTrue(self._sense_conf_2.mapping[9].tolist() == [12, 9, 10, 11])
 
    def test_mapping_all_lines_sens_conf(self):
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

    def test_make_hyperplane(self):
	self._cmac.make_hyperplane()
	self.assertTrue(len(self._cmac.hyperplane) == (13 *10*2))
	self.assertTrue(self._cmac.hyperplane[0] == [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]])
	self.assertTrue(self._cmac.hyperplane[-1] == [[12, 13, 14, 15], [12, 9, 10, 11], [4, 1, 2, 3]])
	self._cmac.make_weight_table()
	self.assertTrue(max(self._cmac.weight_table.keys()) == 41212)
	self.assertTrue(self._cmac.recode([12., 1., 1.])== [41212, 10913, 21014, 31115])
	self.assertTrue(self._cmac.recode([0,0,0])== [0, 10101, 20202, 30303])
	self.assertTrue(self._cmac.recode([5.25, 0.37, -0.2])== [408, 10505, 20206, 30307])
	self.assertIsNotNone(self._cmac.weight_table[41212])
	self.assertIsNotNone(self._cmac.weight_table[10913])
	self.assertIsNotNone(self._cmac.weight_table[21014])
	self.assertIsNotNone(self._cmac.weight_table[31115])
	self.assertIsNotNone(self._cmac.weight_table[10101])
	self.assertIsNotNone(self._cmac.weight_table[20202])
	self.assertIsNotNone(self._cmac.weight_table[30303])
	self.assertIsNotNone(self._cmac.weight_table[408])
	self.assertIsNotNone(self._cmac.weight_table[10505])
	self.assertIsNotNone(self._cmac.weight_table[20206])
	self.assertIsNotNone(self._cmac.weight_table[30307])
	self.assertTrue(self._cmac.fire([4, 0.3, -0.5]) != 0)
 

    def test_mapping_shape_all_sensory_cell_configs(self):
	for sens in self._cmac.sensory_cell_configs:
	        self.assertTrue(sens.mapping.shape == (sens.num_possible_values, sens.num_active_cells))

class TestTrain(unittest.TestCase):
    def setUp(self):
        confs = []
        confs.append(cmac.SensoryCellConfig(-10., 10., 100))
        confs.append(cmac.SensoryCellConfig(-10., 10., 100))
        _cmac = cmac.CMAC(confs, 4)
        _cmac.generate_tables()
        data_in = array([])
        data_out = array([])
        for i in range(100):
            n1 = random.uniform(-100, 100)
            n2 = random.uniform(-100, 100)
            temp = array([n1, n2])
            data_in = concatenate((data_in, temp))
            data_out = concatenate((data_out, array([random.uniform(-100, 100)])))
        self._train = cmac.Train(cmac, data_in, data_out, 0.5, 10)
        
        
    
    def test_train(self): 
        self._train.train()
        
   

if __name__ == '__main__':
    unittest.main()
