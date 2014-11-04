from Tkinter import *
import motus
import gait_loader as ld
class App(object):
    def __init__(self):
        self._root = Tk()
        #self._root.geometry('800x600')
        self._commands = Commands()
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
        self._config_table = MiddleFrame(self).config_table

    def _create_botton_frame(self):
        BottonFrame(self)

    @property
    def root(self):
        return self._root
    
    @property
    def commands(self):
        return self._commands   

    @property
    def config_table(self):
        return self._config_table

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
        self._st = SimpleTable(self, labels)
        self._st.pack(side=TOP, expand=True, fill=BOTH)

    @property
    def config_table(self):
        return self._st

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
            command= (lambda: app.commands.run_plot( \
            desc = app.topframe.desc.get(), \
            activations = int(app.topframe.activations.get()),
            configs = app.config_table.selections, \
            num_iterations = int(app.topframe.numiterations.get())))).pack(side=LEFT)
        new_parameter = None
        Button(self, text="New Parameter", \
            command=(lambda:(app.commands.add_parameter(app.root, app.config_table)))).pack(side=LEFT)

class NewParameter:
    def __init__(self, parent):
        self._root = parent
        self._top = Toplevel(parent)
        loader = ld.loadWalk3()
        self._value = None

        Label(self.top, text='Select a parameter').pack(anchor=W)

        data = loader.data_descs
        self._v = IntVar()
        self._entry_values = []
        for i in range(len(data)):
            f = Frame(self.top)
            f.pack(expand=True, fill=BOTH)
            b = Radiobutton(f, text = data[i].desc, variable = self._v,  value = data[i].index)
            b.grid(row=i, column=0, sticky=W)
            ev = Spinbox(f, from_=1,  to=200)
            ev.grid(row=i, column=1, sticky=E)
            self._entry_values.append(ev)

        f = Frame(self.top)
        f.pack(side=TOP, expand=True, fill=Y)
        ok = Button(f, text='Ok', command=self.ok)
        cancel = Button(f, text='Cancel', command=self.cancel)
        ok.pack(side = LEFT) 
        cancel.pack(side=RIGHT)

    def ok(self):
        self._value = (self._v, int(self._entry_values[self._v.get()].get()))
        self.top.destroy()
    
    def cancel(self):
        self._value = None        
        self.top.destroy()

    def show_return(self):
        self._root.wait_window(self.top)
        return self.value

    @property
    def top(self):
        return self._top

    @property
    def value(self):
        return self._value

class Commands(object):
    def new_project(self):
        pass
    def run_plot(self, desc, activations, configs, num_iterations):
        ann = motus.CMACLegProsthesis(desc, activations, configs)
        ann.train(num_iterations = num_iterations)
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
