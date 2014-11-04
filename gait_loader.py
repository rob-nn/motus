from numpy import *
class DataLoader(object):
	def __init__(self, file_name):
		self._data = None	
		self._file_name = file_name
		self._load_data()
		self._data_descs =[]
		self._generate_data_descs()

	def _load_data(self):
		file = open(self._file_name)
		data = file.readlines()
		file.close()
		j = 0
		data_list = []
		for i in range(len(data)):
			line = data[j]
			if len(line) <=1 or line[0] == '#':
				data.pop(j)
				j = j -1
			else:
				words = line.split()
				temp = []
				for word in words:
					temp.append(float(word))
				data_list.append(temp)
			j = j + 1
		self._data = array(data_list)

	def _generate_data_descs(self):
		self._data_descs.append(self._generate_data_desc(0, 'Left angular velocities'))
		self._data_descs.append(self._generate_data_desc(1, 'Right angular velocities'))
		self._data_descs.append(self._generate_data_desc(2, 'Left angles'))
		self._data_descs.append(self._generate_data_desc(3, 'Right angles'))
		self._data_descs.append(self._generate_data_desc(4, 'Left angular accelarations'))
		self._data_descs.append(self._generate_data_desc(5, 'Right angular accelerations'))
		self._data_descs.append(self._generate_data_desc(6, 'Left x angular velocities'))
		self._data_descs.append(self._generate_data_desc(7, 'Left y angular velocities'))
		self._data_descs.append(self._generate_data_desc(8, 'Left z angular velocities'))
		self._data_descs.append(self._generate_data_desc(9, 'Right x angular velocities'))
		self._data_descs.append(self._generate_data_desc(10, 'Right y angular velocities'))
		self._data_descs.append(self._generate_data_desc(11, 'Right z angular velocities'))

	def _generate_data_desc(self, index, desc):
		column = self.data[:, index]
		return DataDesc(index, desc, column.min(), column.max()) 

	@property
	def data(self):
		return self._data

	@property
	def data_descs(self):
		return self._data_descs

        def normalize(self, index):
                return array((self.data[:, index]  - self.data_descs[index].min_val) / \
                    (self.data_descs[index].max_val - self.data_descs[index].min_val))
        def normalize_all(self):
            new_data = array([])
            for i in range(self.data.shape[1]):
                    new_data = concatenate((new_data, self.normalize(i)))
            return reshape(new_data, self.data.shape) 

class DataDesc(object):
	def __init__(self, index, desc, min_val, max_val):
		self._index = index
		self._min_val = min_val
		self._max_val = max_val
		self._desc = desc

	@property
	def index(self):
		return self._index

	@property
	def min_val(self):
		return self._min_val
	
	@property
	def max_val(self):
		return self._max_val

        @property
        def desc(self):
            return self._desc
	

def loadWalk3():
	return DataLoader('./dynamics_data/dynamics_walk3.mat')
