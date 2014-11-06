from Tkinter import *
import cmac
import gait_loader
from numpy import *
import matplotlib.pyplot as plt

def train():
	x = 1+1

def make_interface():
	root = Tk()
	root.title = 'motus'
	Button(root, text='Train', command=train).pack()
	root.mainloop()
	

class Motus(cmac.CMAC):
    def __init__(self, \
            desc=None, \
            activations=3, \
            configs= None):
        if configs == None:
            configs = [(9, 10),(10, 10),(11, 10)]
        self.validate_parameters(desc, activations, configs)
        loader = gait_loader.loadWalk3() 
        confs = []
        data = None
        out_index = 1 
        for conf in configs: 
            index = conf[0]
            num_values = conf[1]
            desc_conf = loader.data_descs[index]
            new_sensory_config = cmac.SensoryCellConfig(desc.min_val, desc.max_val, num_values, desc_conf)
            confs.append(new_sensory_config)
            column = loader.data[:, index]
            new_data = reshape(column, (len(column), 1))
            if data == None:
                data = new_data
            else:
                data = concatenate((data, new_data), axis = 1)

        super(Motus, self).__init__(confs, activations)
        self.make_weight_table()
        data_out = None
        data_out_test = None
        data_in = None
        data_test = None
        for i in range(data.shape[0]):
            new = reshape(data[i, :], (1, data.shape[1]))
            out = reshape(loader.data[i, out_index], (1,1))
            if i % 2 == 0:
                if data_in == None:
                    data_in = new
                    data_out = out
                else:
                    data_in = concatenate((data_in, new))
                    data_out = concatenate((data_out, out))
            else:
                if data_test == None:
                    data_test = new
                    data_out_test = out
                else:
                    data_test = concatenate((data_test, new))
                    data_out_test = concatenate((data_out_test, out))

        self._data_out = data_out 
        self._data_out_test = data_out_test
        self._data_in = data_in
        self._loader = loader
        self._data_test = data_test
    
    def validate_parameters(self, desc, activations, configs):
        if desc == None or desc.strip() =='':
            raise ParameterInvalid('Invalid Description.')
        if activations == None or activations <=0:
            raise ParameterInvalid('Number of activations must be greater than zero')
        for conf in configs:
            if conf[1] <= activations:
                loader = gait_loader.loadWalk3() 
                desc = loader.data_descs[conf[0]]
                raise ParameterInvalid('The parameter %s must be greater than the number of activations' % desc)

    def train(self, num_iterations = 50): 
        t = cmac.Train(self, self._data_in, self._data_out, 1, num_iterations)
        t.train()
        self.t = t
    
    def plot_data(self):
        for i in range(self._data_in.shape[1]):
            plt.figure()
            plt.plot(self._data_in[:,i].tolist())
        plt.figure()
        plt.plot(self._data_out)
        plt.show()
    
    def fire_test(self):
        result = []
        for data in self._data_test:
            result.append(self.fire(data))
        return result

    def plot_test(self):
        plt.figure()
        plt.plot(self.t.E)
        
        t = arange(0, self._data_out_test.shape[0]) *(2.*(1./315.) )
        test_result = self.fire_test()
        
        
        plt.figure()
        plt.hold(True)
        p1 = plt.plot(t.tolist(), self._data_out_test.tolist(), 'b', linewidth=4)
        p2 = plt.plot(t.tolist(), test_result, 'r', linewidth=2)
        plt.xlabel('t (segundos)', fontsize=15)
        plt.ylabel('Velocidades angulares (rads/seg)', fontsize=15)
        plt.legend(['Joelho humano', 'MISO CMAC'])
        plt.show()

class ParameterInvalid(BaseException):
    def __init__(self, description):
        self._description = description

    @property
    def description(self):
        return self._description

def main():
    cmac = Motus(desc='motus')
    #cmac.plot_data()
    cmac.train()
    cmac.plot_test()
    return cmac


if __name__ == '__main__':
    main()


            
