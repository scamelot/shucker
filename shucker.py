from tkinter import *
from tkinter import filedialog
import subprocess
import os

PICTURES = ["png","gif","jpg"]
VIDEOS = ["mov","mp4","mkv"]
DOCUMENTS = ["xls*","doc*","pages","keynote","pdf"]

master = Tk()
master.title("Shucker")
opt_keepdirs = IntVar()
inpath = StringVar(master)
outpath = StringVar(master)

filetypes = StringVar(master)
filetypes.set("pictures")
dd_filetypes = OptionMenu(master, filetypes, "pictures", "videos", "documents", "all")

chk_dirs = Checkbutton(master, text='Preserve directory tree',variable=opt_keepdirs, onvalue=1, offvalue=0)

def browseFunc(direction):
	filename = filedialog.askdirectory()
	if direction == "in":
		inpath.set(filename)
	else:
		outpath.set(filename)

btn_inpath = Button(master, text="Source Folder", command= lambda: browseFunc("in"))
ent_inpath = Entry(master, text=inpath, width=50)

btn_outpath = Button(master, text="Destination Folder", command= lambda: browseFunc("out"))
ent_outpath = Entry(master, text=outpath, width=50)

if filetypes.get() == "pictures":
	extensions = PICTURES
elif filetypes.get() == "videos":
	extensions = VIDEOS
elif filetypes.get() == "documents":
	extensions = DOCUMENTS

btn_execute = Button(master, text="Shuck It!", command= lambda: shuck(extensions, inpath.get(), outpath.get(), chk_dirs))

btn_inpath.pack()
ent_inpath.pack()

chk_dirs.pack()
dd_filetypes.pack()

btn_outpath.pack()
ent_outpath.pack()
btn_execute.pack()

##find . -name '*.png' | cpio -pdm ./Screenshots
def shuck(extensions, inpath, outpath, chk_dirs):

	#source compliation
	command = ['find', '-E', inpath, '-iregex']
	sources = ""
	for extension in extensions:
			sources += extension + "|" #collate filetypes
	sources = sources[:-1] #cut off the last |
	command.append(r'".*\.('+sources+')\"')
	if chk_dirs:
		flags = "-pdm"
	else:
		flags = "-pm"
	outcmd = ["|","cpio",flags , outpath]

	command.extend(outcmd)
	command = ' '.join([str(elem) for elem in command])
	print(command)
	os.system(command)
#TODO : use os.system to call the command as a single string

mainloop()
