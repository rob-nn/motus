from numpy import *
import math

class CMAC(object):
    def __init__(self, s_min, s_max, num_possible_values, num_active_cells):
        self._s_min = s_min
        self._s_max = s_max
        self._num_possible_values = num_possible_values
        self._num_active_cells = num_active_cells
        self._set_mapping_address()
        self._set_mapping()

    def _set_mapping(self):
        temp_map = []
        i = 0
        qtd = 0
        stop = False
        while True:
            temp = []
            for j in range(self.num_active_cells):
                line = []
                for k in range(j, self.num_active_cells):
                    line.append(k)
                temp.append(line)
                qtd = qtd + 1
                if qtd == self.num_possible_values:
                    stop = True
                    break 
            for l in range(len(temp)):
               for m in range(len(temp[l])):
                    temp[l][m] = temp[l][m] + i
            acc = 0 
            for j in range(self.num_active_cells):
                if stop and j >= len(temp):
                    break;
                if j == 0:
                    acc = temp[0][-1]
                for k in range(self.num_active_cells - len(temp[j])):
                    temp[j].insert(k, acc+k+1)
                    
            temp_map.extend(temp)    
            if stop: break
            i = i + self.num_active_cells 

        self._mapping = array(temp_map)

    def _set_mapping_address(self):
        self._mapping_address = linspace(self._s_min, self._s_max, self._num_possible_values)

    @property
    def mapping(self):
        return self._mapping
    @property
    def mapping_address(self):
        return self._mapping_address
    @property
    def num_active_cells(self):
        return self._num_active_cells
    @property
    def num_possible_values(self):
        return self._num_possible_values
    @property
    def s_min(self):
        return self._s_min
    @property
    def s_max(self):
        return self._s_max

                

class CMACLegProsthesis(object):
	def __init__(self, active_sensory_cells):
		self._active_sensory_cells = active_sensory_cells

	def train(self, data_loader): pass

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


def generate_inputs():
	inputs = []
	for i in range(9):
		inputs.append(Input(i, 'Attr ' + str(i), -10, 10))
	return inputs

