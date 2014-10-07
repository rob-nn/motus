from numpy import *
from gait_loader import *
import math

class CMAC(object):

    def __init__(self, sensory_configs, num_active_cells):
        self._num_active_cells = num_active_cells
        self._sensory_configs = sensory_configs
        self._set_sensory_mappings()

    def _set_sensory_mappings(self):
        for sensory_config in self._sensory_configs:
            sensory_config.cmac = self
            sensory_config.set_mapping()

    def make_hyperplane(self):
        hyper = []
        for conf in self.sensory_cell_configs:
            self._append_hyper(hyper, len(conf.mapping))
        
        for i in range(len(self.sensory_cell_configs)):
            for j in range(len(self.sensory_cell_configs[i].mapping)):
                
 
        self._hyperplane = array(hyper)

    def _append_hyper(self, hyper, num_elements):
        if type(hyper) is list and len(hyper) == 0:
            for i in range(num_elements):
                hyper.append([])
        else:
            for l in hyper:
                self._append_hyper(l, num_elements, final_conf)
                
            
            
    @property
    def num_active_cells(self):
        return self._num_active_cells

    @property
    def sensory_cell_configs(self):
        return self._sensory_configs
    
    @property
    def hyperplane(self):
        return self._hyperplane
                

class CMACLegProsthesis(object):
	def __init__(self, active_sensory_cells):
		self._active_sensory_cells = active_sensory_cells

	def train(self, data_loader): pass

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
