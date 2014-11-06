from Tkinter import *
import tkMessageBox
import tkFileDialog
import motus
import gait_loader as ld

class App(object):
    def __init__(self):
        self._label_output = None
        self.output = ()
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
        self.output = ()
        self.label_out.config(text='')

    @property
    def root(self):
        return self._root
    
    @property
    def commands(self):
        return self._commands   
    @property
    def middle_frame(self):
        return self._middle_frame

    @property
    def label_out(self):
        return self._label_output
    
    @label_out.setter
    def label_out(self, value):
        self._label_output = value

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
        self._app = app
        self.pack(side=TOP, expand=True, fill=BOTH)

        Label(self, text = 'Description').grid(row=0, column=0)
        self.desc = Entry(self)
        self.desc.grid(row=0, column=1)

        Label(self, text = 'Activations').grid(row=1, column=0)
        self.activations = Spinbox(self, from_=1, to=30)
        self.activations.grid(row=1, column=1)

        Label(self, text = 'Num. Iterations').grid(row=0, column=3)
        self.numiterations = Spinbox(self, from_=1, to=200)
        self.numiterations.grid(row=0, column=4)

        frame = Frame(self)
        frame.grid(row=1, column=3)
        Label(frame, text='Output').pack(side=LEFT)
        Button(frame, text="Change", command=self._select_output).pack(side=LEFT)
        
        self._app.label_out = Label(self)
        self._app.label_out.grid(row=1, column=4)
        if len(self._app.output)>1:
            self._app.label_out.config(text= self._app.output[1])
    
    def _select_output(self):
        SelectOutput(self._app)
        

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
        out = self.app.output
        f.write(str(out[0]) + ' ' + str(out[1]) + '\n')
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
            output = f.readline().split()
            self.app.output=(output[0], output[1])
            self.app.label_out.config(text= output[1])
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
            if len(self.app.output) ==0:
                raise motus.ParameterInvalid('Inform the output parameter')
            ann = motus.Motus(self.app.topframe.desc.get(), int(self.app.topframe.activations.get()), self.app.middle_frame.selections, self.app.output[0])
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

class SelectOutput():
    def __init__(self, app):
        self._app = app
        self._window = Toplevel(app.root)
        self._value = IntVar(self._window)
        loader = ld.loadWalk3()
        self._descs = []
        for desc in loader.data_descs:
            self._descs.append(desc.desc)
            option = Radiobutton(self._window, variable=self._value, value=desc.index, text=desc.desc)
            option.pack(anchor=NW)
        frame = Frame(self._window)
        frame.pack(side=TOP)
        Button(frame, text='Ok', command=self._ok).pack(side=LEFT)
        Button(frame, text='Cancel', command=self._window.destroy).pack(side=RIGHT)
        if len(app.output) >0:
            self._value.set(app.output[0])
        #self._window.transient(app.root)
        self._window.grab_set()
        app.root.wait_window(self._window)

    def _ok(self):
        self._app.output = (self._value.get(), self._descs[int(self._value.get())])
        self._app.label_out.config(text=self._app.output[1])
        self._window.destroy()

def main():
    app = App()
    app.run()

if __name__=='__main__':
    main()
