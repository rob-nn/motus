from Tkinter import *

def train():
	x = 1+1

def make_interface():
	root = Tk()
	root.title = 'motus'
	Button(root, text='Train', command=train).pack()
	root.mainloop()
	

def main():
	make_interface();


if __name__ == '__main__':
	main()
