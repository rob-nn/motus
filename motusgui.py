from Tkinter import *
import motus
class App(object):
    def __init__(self):
        self._root = Tk()
        #self._root.geometry('800x600')
        self._commands = Commands()
        self._generate_menu_bar()
        self._create_top_frame()
        self._create_botton_frame()

    def run(self):
        self._root.mainloop()

    def _generate_menu_bar(self):
        TopMenu(self)

    def _create_top_frame(self):
        self.topframe = TopFrame(self)

    def _create_botton_frame(self):
        BottonFrame(self)

    @property
    def root(self):
        return self._root
    
    @property
    def commands(self):
        return self._commands   

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

        Label(self, text = 'Num. Values').pack(side=LEFT)
        self.numvalues = Spinbox(self, from_=1, to=200)
        self.numvalues.pack(side=LEFT)

class BottonFrame(Frame):
    def __init__(self, app):
        Frame.__init__(self, app.root)
        self.pack(side= TOP, expand=True, fill=BOTH)
        Button(self, text='Run & Plot', \
            command= (lambda: app.commands.run_plot( \
            app.topframe.desc.get(), \
            int(app.topframe.activations.get()),
            int(app.topframe.numvalues.get())))).pack(side=LEFT)

class Commands(object):
    def new_project(self):
        pass

    def run_plot(self, desc, activations, num_values):
        ann = motus.CMACLegProsthesis(desc, activations, num_values)
        ann.train()
        ann.plot_test()
    
def main():
    app = App()
    app.run()

if __name__=='__main__':
    main()
