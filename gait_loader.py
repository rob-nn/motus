class DataLoader(object):

	def __init__(self, inputs, output_indexes):
		self._data = []
		self._inputs = inputs
		self._output_indexes = output_indexes
		self._input_data = []
		self._output_data = []
		self._load_data()
		self._generate_inputs_outputs()

	def _load_data(self):
		file = open('./dynamics_data/dynamics_walk3.mat')
		data = file.readlines()
		file.close()
		j = 0
		for i in range(len(data)):
			line = data[j]
			if len(line)<=1 or line[0] == '#':
				data.pop(j)
				j = j -1
			else:
				words = line.split()
				temp = []
				for word in words:
					temp.append(float(word))
				self._data.append(temp)
			j = j + 1

	def _generate_inputs_outputs(self):
		for item in self._data:
			inputs = []
			outputs = []
			for i in self._inputs:
				inputs.append(item[i.index])		
			self._input_data.append(inputs)
			for o in self._output_indexes:
				outputs.append(item[o])
			self._output_data.append(outputs)
		
	@property
	def input_data(self):
		return self._input_data

	@property
	def output_data(self):
		return self._output_data

	@property
	def data(self):
		return self._data

class Input(object):
	def __init__(self, index, desc, min_val, max_val):
		self._index = index
		self._min_val = min_val
		self._max_val = max_val
		self._desc = desc

	@property
	def index(self):
		return self._index
