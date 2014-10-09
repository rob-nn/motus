from numpy import *
from gait_loader import *
import math
import random
import gait_loader
import matplotlib.pyplot as plt

class CMAC(object):

    def __init__(self, sensory_configs, num_active_cells):
        self._num_active_cells = num_active_cells
        self._sensory_configs = sensory_configs
        self._set_sensory_mappings()
        random.seed()

    def generate_tables(self):
        self.make_hyperplane()
        self.make_weight_table()

    def _set_sensory_mappings(self):
        for sensory_config in self._sensory_configs:
            sensory_config.cmac = self
            sensory_config.set_mapping()

    def make_hyperplane(self):
#        hyper = []
#        for conf in self.sensory_cell_configs:
#            self._append_hyper(hyper, len(conf.mapping))
#        self._hyperplane = array(hyper)
        l =[]
        for dim in self.sensory_cell_configs:
            l = self._append_dim(l, dim.mapping)
        self._hyperplane = l

    def _append_dim(self, l, values):
        if l == []:
            for i in values:
                temp = []
                temp.append(i.tolist())
                l.append(temp)
            return l
        new_list = []
        for item in l:
            for value in values:
                new_item = item[:]
                new_item.append(value.tolist())
                new_list.append(new_item)
        return new_list

#    def _append_hyper(self, hyper, num_elements):
#        if type(hyper) is list and len(hyper) == 0:
#            for i in range(num_elements):
#                hyper.append([])
#        else:
#            for l in hyper:
#                self._append_hyper(l, num_elements)
            
    def get_address(self, recode_vector):
        num_dig = []
        for conf in self.sensory_cell_configs:
            num_dig.append(int(floor(log10(conf.mapping.max())+1)))
        address = 0
        acc = 0
        for j in range(len(self.sensory_cell_configs)):
            address = address + int(recode_vector[j]) * 10 ** acc
            acc = acc + num_dig[j] 
        return address

    def make_weight_table(self):
        table = {}
        for item in self.hyperplane:
            sens_values = array(item, dtype=int64)                
            for i in range(self.num_active_cells):
                temp = sens_values[:, i].tolist()
                address = self.get_address(temp)
                table[address] = random.uniform(-0.2,0.2)
        self._table = table

    def recode(self, input_vector):
        recode_vector = []
        sens_values = []
        for i in range(len(self.sensory_cell_configs)):
            index = self.get_index(input_vector[i], self.sensory_cell_configs[i])
            sens_values.append(self.sensory_cell_configs[i].mapping[index])
        sens_values = array(sens_values, dtype=int64)
        for i in range(self.num_active_cells):
            temp = sens_values[:, i].tolist()
            address = self.get_address(temp)
            recode_vector.append(address)
        return recode_vector
    
    def get_index(self, value, config):
        if value <= config.s_min:
            return 0;
        if value >= config.s_max:
            return len(config.mapping_address) -1
        for i in range(len(config.mapping_address)):
            if config.mapping_address[i] > value:
                return i-1 

    def fire(self, input_vector):
        recode_vector = self.recode(input_vector)
        p = 0
        for address in recode_vector:
            p = p + self.weight_table[address]    
        return p
            
    @property
    def weight_table(self):
        return self._table            
    @property
    def num_active_cells(self):
        return self._num_active_cells

    @property
    def sensory_cell_configs(self):
        return self._sensory_configs
    
    @property
    def hyperplane(self):
        return self._hyperplane

class Train(object):
    def __init__(self, cmac, data_in, data_out, alpha, num_iterations):
        self._cmac = cmac
        self._data_in = data_in
        self._data_out = data_out
        self._alpha = alpha
        self._num_iterations = num_iterations

    def train(self):
	self.E = []
        for iteration in range(self._num_iterations):
	    err =0
            for i in range(len(self.data_in)):
                input_vector = self.data_in[i, :].tolist()
                out = self.cmac.fire(input_vector)
                recode_vector = self.cmac.recode(input_vector)
                for recode in recode_vector:
                    self.cmac.weight_table[recode] = self.cmac.weight_table[recode] + self.alpha * (self.data_out[i] -out) / self.cmac.num_active_cells
		    err = err+ ((self.data_out[i] -out)**2)/2
	    self.E.append(err)
	    if iteration % 10 == 0: print iteration
           
    @property 
    def alpha(self):
        return self._alpha 

    @property
    def data_in(self):
        return self._data_in

    @property
    def data_out(self):
        return self._data_out
    
    @property
    def cmac(self):
        return self._cmac

class SensoryCellConfig(object):
    def __init__(self, s_min, s_max, num_possible_values):
        self._s_min = s_min
        self._s_max = s_max
        self._num_possible_values = num_possible_values
        self._cmac = None

    def set_mapping(self):
        self._set_mapping_address()
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
    def cmac(self):
        return self._cmac
    @cmac.setter
    def cmac(self, value):
        self._cmac = value
    @property
    def mapping(self):
        return self._mapping
    @property
    def mapping_address(self):
        return self._mapping_address
    @property
    def num_active_cells(self):
        return self._cmac.num_active_cells
    @property
    def num_possible_values(self):
        return self._num_possible_values
    @property
    def s_min(self):
        return self._s_min
    @property
    def s_max(self):
        return self._s_max
