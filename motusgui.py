from Tkinter import *
class App(object):
    def __init__(self):
        self._root = Tk()
        self._root.geometry('800x600')
        self._commands = Commands()
        self._generate_menu_bar()
        self._create_cmac_frame()

    def _create_cmac_frame(self):
        f = Frame(self._root)
        f.pack(anchor=W)
        Label(f, text = 'Description').grid(row=0, column=0, sticky=E)
        Label(f, text = 'Activations').grid(row=1, column=0, sticky=E)
        Label(f, text = 'Iterations').grid(row=2, column=0, sticky=E)

        Entry(f).grid(row=0, column=1, sticky=W)
        Spinbox(f, from_=1, to=30).grid(row=1, column=1, sticky=W)
        Spinbox(f, from_=1, to=200).grid(row=2, column=1, sticky=W)
    
    def _generate_menu_bar(self):
        menu_bar = Menu(self._root)
        self._root.configure(menu=menu_bar)

        file_menu =  Menu(menu_bar)
        menu_bar.add_cascade(label='File', menu=file_menu)

        file_menu.add_command(label='New Project', command=self._commands.new_project)
        file_menu.add_command(label='Save Project', command=self._commands.new_project)
        file_menu.add_command(label='Save as Project', command=self._commands.new_project)

        file_menu.add_separator()

        file_menu.add_command(label='Quit', command=self._root.quit)

    def run(self):
        self._root.mainloop()

class Commands(object):
    def new_project(self):
        pass
    
def main():
    app = App()
    app.run()

if __name__=='__main__':
    main()
