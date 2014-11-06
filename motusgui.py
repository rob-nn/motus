from Tkinter import *
import tkMessageBox
import tkFileDialog
import motus
import gait_loader as ld

class App(object):
    def __init__(self):
        self._root = Tk()
        self._root.title('Motus')
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

    def clear(self):
        self.topframe.clear()
        self.middle_frame.clear()
        self._commands.filename = None

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
        file_menu.add_command(label='Save Project', command=app.commands.save)
        file_menu.add_command(label='Save Project as', command=app.commands.save_as)
        file_menu.add_command(label='Load Project', command=app.commands.load)
        file_menu.add_separator()
        file_menu.add_command(label='Quit', command=app.root.quit)

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

    def clear(self):
        vdesc = StringVar()
        vdesc.set('')
        self.desc.config(textvariable=vdesc)
        vact = IntVar()
        vact.set(1)
        self.activations.config(textvariable=vact)
        vint = IntVar()
        vint.set(1)
        self.numiterations.config(textvariable=vint)
            
class MiddleFrame(Frame):
    def __init__(self, app):
        Frame.__init__(self, app.root)
        self.pack(side=TOP, expand=True, fill=BOTH)
        Label(self, text= 'Parameters Configuration', font=('Helvetica', '16', 'bold')).pack(side=TOP, expand=True, fill=Y)
        self.pack_parameters()

    def pack_parameters(self):
        loader = ld.loadWalk3()
        descs = loader.data_descs
        self._check_values = []
        self._spins = []
        f = Frame(self, bd=1, relief=SUNKEN)
        f.pack(expand=True, fill=BOTH)
        for i in range(len(descs)):
            self._check_values.append(IntVar())
            c = Checkbutton(f, text=descs[i].desc, variable=self._check_values[i])
            c.grid(row=i, column=0, sticky=W)
            sv = Spinbox(f, from_=1, to= 200)
            sv.grid(row=i, column=1, sticky=E)
            self._spins.append(sv)
    
    def clear(self):
        for i in range(len(self.check_values)):
            self.check_values[i].set(False)
            val = IntVar()
            val.set(0)
            self._spins[i].config(textvariable=val)

    @property
    def selections(self):
        values = []
        for i in range(len(self._check_values)):
            if self._check_values[i].get() ==1:
                values.append((int(i), int(self._spins[i].get())))            
        return values
    
    @property
    def check_values(self):
        return self._check_values
    
    @property
    def spins(self):
        return self._spins

class BottonFrame(Frame): 
    def __init__(self, app):
        Frame.__init__(self, app.root)
        self.pack(side= TOP, expand=True, fill=BOTH)
        Button(self, text='Run & Plot', \
            command= app.commands.run_plot).pack(side=LEFT)

class Commands(object):
    def __init__(self, app):
        self._app = app
        self.file_opt = options = {}
        options['defaultextension'] = '.mts'
        options['filetypes'] = [('motus files', '.mts')]
        options['initialdir'] = '~'
        options['parent'] = app.root
        options['title'] = 'Save a motus project file'
        self.filename = None
  
    @property
    def app(self):
        return self._app
    
    def save(self):
        if self.filename:
            self._save()
        else:
            self.save_as() 

    def save_as(self):
        self.filename = tkFileDialog.asksaveasfilename(**self.file_opt)
        if self.filename:
            self._save()

    def _save(self):
        f = open(self.filename, 'w')
        f.write(self.app.topframe.desc.get() + '\n')
        f.write(self.app.topframe.activations.get() + '\n')
        f.write(self.app.topframe.numiterations.get() + '\n')
        for item in self.app.middle_frame.selections:   
            f.write(str(item[0]) + ' ' + str(item[1]) + '\n')
        f.close()

    def load(self):
        self.app.clear()
        filename = tkFileDialog.askopenfilename(**self.file_opt)
        if filename:
            self.filename = filename
            f = open(self.filename, 'r')
            desc = StringVar()
            desc.set(f.readline().strip())
            self.app.topframe.desc.config(textvariable=desc)
            activations = StringVar()
            activations.set(f.readline().strip())
            self.app.topframe.activations.configure(textvariable=activations)
            iterations = StringVar()
            iterations.set(f.readline().strip())
            self.app.topframe.numiterations.configure(textvariable=iterations)
            for item in f:
                values = item.split()
                self.app.middle_frame.check_values[int(values[0])].set(True)
                value = IntVar()
                value.set(values[1])
                self.app.middle_frame.spins[int(values[0])].config(textvariable=value)
            f.close()

    def new_project(self):
        self.app.clear()

    def run_plot(self):
        try:
            ann = motus.Motus(self.app.topframe.desc.get(), int(self.app.topframe.activations.get()), self.app.middle_frame.selections)
            ann.train(num_iterations = int(self.app.topframe.numiterations.get()))
        except motus.ParameterInvalid as invalid:
            tkMessageBox.showerror(title= 'Invalid parameter', message= invalid.description, icon=tkMessageBox.ERROR)
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
