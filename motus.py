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
	

class CMACLegProsthesis(cmac.CMAC):
    def __init__(self):
        loader = gait_loader.loadWalk3() 
        confs = []
        data = None
        data_i = [0, 8]
        for i in data_i: 
            desc = loader.data_descs[i]
            new_sensory_config = cmac.SensoryCellConfig(desc.min_val, desc.max_val, 100)
            confs.append(new_sensory_config)
            column = loader.data[:,i]
            new_data = reshape(column, (len(column), 1))
            if data == None:
                data = new_data
            else:
                data = concatenate((data, new_data), axis = 1)

        super(CMACLegProsthesis, self).__init__(confs, 4)
        self.generate_tables()
        data_out = None
        data_out_test = None
        data_in = None
        data_test = None
        for i in range(data.shape[0]):
            new = reshape(data[i, :], (1, data.shape[1]))
            out = reshape(loader.data[i,3], (1,1))
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

    def train(self): 
        t = cmac.Train(self, self._data_in, self._data_out, 0.1, 200)
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
        test_result = self.fire_test()
        plt.figure()
        plt.hold(True)
        plt.plot(self._data_out_test.tolist(), 'b')
        plt.plot(test_result, 'r')
        plt.show()

def main():
    cmac = CMACLegProsthesis()
    #cmac.plot_data()
    cmac.train()
    cmac.plot_test()


if __name__ == '__main__':
    main()
