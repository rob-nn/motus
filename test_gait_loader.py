import unittest
from numpy import *
from gait_loader import *
class TestDataLoader(unittest.TestCase):
	def setUp(self):
		self._loader3 = loadWalk3()

	def tearDown(self):
        	self._loader3 = None

    	def test_shape(self):
		self.assertTrue(self._loader3.data.shape ==(696, 12))

	def test_data_descs(self):
		self.assertTrue(len(self._loader3.data_descs) == 12)

        def test_normalize(self):
                self.assertTrue(all(self._loader3.normalize(0)<=1)) 

        def test_normalize_all(self):
                self.assertTrue(all(self._loader3.normalize_all() <= 1)) 

if __name__ == '__main__':
    unittest.main()
