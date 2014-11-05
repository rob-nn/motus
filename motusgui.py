from Tkinter import *
import motus
import gait_loader as ld

class App(object):
    def __init__(self):
        self._root = Tk()
        #self._root.geometry('800x600')
        self._commands = Commands(self)
        self._generate_menu_bar()
        self._create_top_frame()
        self._create_middle_frame()
        self._create_botton_frame()

    def run(self):
        self._root.mainloop()

    def _generate_menu_bar(self):
        TopMenu(self)

    def _create_top_frame(self):
        self.topframe = TopFrame(self)

    def _create_middle_frame(self):
        self._middle_frame = MiddleFrame(self)
        

    def _create_botton_frame(self):
        BottonFrame(self)

    @property
    def root(self):
        return self._root
    
    @property
    def commands(self):
        return self._commands   
    @property
    def middle_frame(self):
        return self._middle_frame

class TopMenu(Menu):
    def __init__(self, app):
        Menu.__init__(self, app.root)
        app.root.configure(menu=self)
        file_menu =  Menu(self)
        self.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New Project', command=app.commands.new_project)
        file_menu.add_command(label='Save Project', command=app.commands.new_project)
        file_menu.add_command(label='Save as Project', command=app.commands.new_project)
        file_menu.add_separator()
        file_menu.add_command(label='Quit', command=app.root.quit)

class MiddleFrame(Frame):
    def __init__(self, app):
        Frame.__init__(self, app.root)
        self.pack(side=TOP, expand=True, fill=BOTH)
        Label(self, text= 'Parameters Configuration').pack(side=TOP, expand=True, fill=Y)
        labels = ['Description', 'Min value', 'Max value', 'Possible Numbers']
        fp = Frame(self)
        fp.pack(side=TOP, expand=True, fill=BOTH)
        self.pack_parameters()

    def pack_parameters(self):
        loader = ld.loadWalk3()
        descs = loader.data_descs
        self._check_values = []
        self._spins = []
        Label(self, text='Select a parameter').pack(anchor=W)
        for i in range(len(descs)):
            f = Frame(self)
            f.pack(expand=True, fill=BOTH)
            self._check_values.append(IntVar())
            c = Checkbutton(f, text=descs[i].desc, variable=self._check_values[i])
            c.grid(row=i, column=0, sticky=W)
            sv = Spinbox(f, from_=1, to= 200)
            sv.grid(row=i, column=1, sticky=E)
            self._spins.append(sv)

    @property
    def selections(self):
        values = []
        for i in range(len(self._check_values)):
            if self._check_values[i].get() ==1:
                values.append((int(i), int(self._spins[i].get())))            
        return values

class TopFrame(Frame):
    def __init__(self, app):
        Frame.__init__(self, app.root)
        self.pack(side=TOP, expand=True, fill=BOTH)
        Label(self, text = 'Description').pack(side=LEFT)
        self.desc = Entry(self)
        self.desc.pack(side=LEFT)

        Label(self, text = 'Activations').pack(side=LEFT)
        self.activations = Spinbox(self, from_=1, to=30)
        self.activations.pack(side=LEFT)

        Label(self, text = 'Num. Iterations').pack(side=LEFT)
        self.numiterations = Spinbox(self, from_=1, to=200)
        self.numiterations.pack(side=LEFT)

class BottonFrame(Frame): 
    def __init__(self, app):
        Frame.__init__(self, app.root)
        self.pack(side= TOP, expand=True, fill=BOTH)
        Button(self, text='Run & Plot', \
            command= app.commands.run_plot).pack(side=LEFT)

class Commands(object):
    def __init__(self, app):
        self._app = app

    @property
    def app(self):
        return self._app

    def new_project(self):
        pass

    def run_plot(self):
        app = self.app
        ann = motus.CMACLegProsthesis(app.topframe.desc.get(), int(app.topframe.activations.get()), app.middle_frame.selections)
        ann.train(num_iterations = int(app.topframe.numiterations.get()))
        ann.plot_test()

    def add_parameter(self, root, table):
        d = NewParameter(root)
        value = d.show_return()
        d.top.destroy()
        if value != None:
            table.add(value)         

# inspired be http://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter
# by Bryan Oakley
class SimpleTable(Frame):
    def __init__(self, parent,  labels):
        Frame.__init__(self, parent)
        for column in range(len(labels)):
            label = Label(self, text=labels[column])
            label.grid(row=0, column=column)
        self._selections = []

    def add(self, selection):
        index = selection[0].get()
        num_values = selection[1]

        data = ld.loadWalk3().data_descs[index]

        row = self.grid_size()[1] + 1

        label=Label(self, text=data.desc)
        label.grid(row=row, column=0)
        label=Label(self, text=data.min_val)
        label.grid(row=row, column=1)
        label=Label(self, text=data.max_val)
        label.grid(row=row, column=2)
        label=Label(self, text=num_values)
        label.grid(row=row, column=3)

        self._selections.append((index, num_values))

    @property
    def selections(self):
        return self._selections 
            
def main():
    app = App()
    app.run()

if __name__=='__main__':
    main()
