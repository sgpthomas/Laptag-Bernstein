"""

Laptag Bernstein Wave Analyzation Program with Tkinter User Interface
written by Sam Thomas

"""
#imports
from tkinter import *
from tkinter.ttk import *
import matplotlib

import matplotlib.pyplot as plt
import numpy as np
import sys

#global vars
window_width = 800
window_height = 600

#argument
try:
    dataFilePath = sys.argv[1]
except:
    dataFilePath = ''
    print("No Path Given")

#TK Window
class main_window(Frame):
    def __init__(self, parent):
        #call frame init class
        Frame.__init__(self, parent)

        self.parent = parent
        self.notebook = Notebook(parent)

        #calls other fcns in the class
        self._initUI()
        self.centerWindow()

        self.make_frame()
        self.pop_notebook()

        self.notebook.pack(fill=BOTH, expand=1)

    def pop_notebook(self):
        self.notebook.add(self.infoFrame.infoFrame, text="Info")
        self.notebook.add(self.dataFrame.tf_dataFrame, text="Data")

    #add the frames
    def make_frame(self):
        self.infoFrame = infoFrameClass(self.notebook)
        self.dataFrame = dataTreeFrame(self.notebook)

    #init the tk ui
    def _initUI(self):
        #names the window
        self.parent.title("Laptag Bernstein Wave TK - WIP")

    #center window
    def centerWindow(self):
        w,h = window_width, window_height
        sw, sh = self.parent.winfo_screenwidth(), self.parent.winfo_screenheight()

        x = (sw-w)/2
        y = (sh-h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

#class that parses the data from the data file given
class readFileClass(object):
    def __init__(self, fileName):
        self.fileName = fileName
        print(self.fileName)
        self.xArray = []
        self.yArray = []

        if self.fileName != '':
            self.extractData()

    def extractData(self):

        readFile = open(self.fileName, 'r')

        sepFile = readFile.read().split('\n')

        readFile.close()

        for plotPair in sepFile:
            xAndY = plotPair.split(',')
            self.xArray.append(float(xAndY[0]))
            self.yArray.append(float(xAndY[1]))

#class the defines the info frame class
class infoFrameClass(Frame):
    def __init__(self, parent):
        #frame
        self.infoFrame = Frame(parent)
        #path widgets
        self.font = ('Ubuntu', 12)
        self.initPathWidgets()
        self.initMathWidgets()

    def initMathWidgets(self):
        #Label
        self.mathLabel = Label(self.infoFrame, text='Math Analysis', font=self.font)
        self.mathLabel['foreground'] = 'blue'
        self.mathLabel.grid(column=1, row=0, pady=5, padx=20)
        #maybe a math file entry box
        self.mathEntryText = StringVar()
        self.mathEntry = Entry(self.infoFrame, text=self.mathEntryText)
        self.mathEntry.insert(0, 'Maybe Temporary')
        self.mathEntry.grid(column=1, row=1, pady=5, padx=20)
        #button to make graph
        self.mathButton = Button(self.infoFrame, text="Graph", command=self.mathButtonCmd)
        self.mathButton.grid(column=1, row=2, pady=5, padx=20)

    def initPathWidgets(self):
        #Label
        self.infoFrameLabel = Label(self.infoFrame, text='Data File Path', font=self.font)
        self.infoFrameLabel['foreground'] = 'green'
        self.infoFrameLabel.grid(column=0, row=0, pady=5, padx=10)
        #path entry box
        self.pathEntryText = StringVar()
        self.pathEntry = Entry(self.infoFrame, text=self.pathEntryText)
        self.pathEntry.insert(0, dataFilePath)
        self.pathEntry.grid(column=0, row=1, pady=5, padx=10)
        #button
        self.pathButton = Button(self.infoFrame, text="Update", command=self.pathButtonCmd)
        self.pathButton.grid(column=0, row=2, pady=5, padx=10)
    def pathButtonCmd(self):
        path = self.pathEntry.get()
        dataTreeFrame.update_DataTree(path)
    def mathButtonCmd(self):
        print("You clicked the Graph Button")


#class that defines the datatree class
#attempt at a sort of static class
class dataTreeFrame(Frame):

    tf_dataTree = None
    tf_scrollbar = None
    
    def __init__(self, parent):

        dataTreeFrame.tf_dataFrame = Frame(parent)
        dataTreeFrame.tf_dataTree = dataTreeFrame.make_dataTree()
        dataTreeFrame.tf_scrollbar = dataTreeFrame.make_ScrollBar()
        dataTreeFrame.update_DataTree(dataFilePath)

    def assignFile(fileString):
        return readFileClass(fileString)

    def make_dataTree():
        #makes columns and assigns names
        columns = ("#", "X Value", "Y Value")
        tf_dataTree = Treeview(dataTreeFrame.tf_dataFrame, columns=columns, show="headings")
        for col in columns:
            tf_dataTree.column(col)
            tf_dataTree.heading(col, text=col)

        return tf_dataTree

    def make_ScrollBar():
        return Scrollbar(dataTreeFrame.tf_dataTree, orient=VERTICAL, command=dataTreeFrame.tf_dataTree.yview)

    def choose_tag(num):
        newNum = num % 2
        if (newNum == 0): 
            return 'even'
        else:
            return 'odd'

    def update_TreeView(x, y, dt, sb):
        #first deletes all existing data
        for child_id in dt.get_children():
            dt.delete(child_id)

        #populates columns with data from file
        i = 0
        while i < len(x):
            dt.insert('', 'end', values=(i+1,x[i],y[i]), tags=(dataTreeFrame.choose_tag(i)))
            i = i + 1
        #correct placement and scroll bar
        dt.tag_configure('even', background='gray')
        dt.tag_configure('even', background='#BCC6CC')
        dt.pack(fill=BOTH, expand=1)
        dt['yscrollcommand'] = sb.set
        sb.pack(side=RIGHT, fill=BOTH)

    def update_DataTree(path):
        tf_fileClass = dataTreeFrame.assignFile(path)
        tf_x = tf_fileClass.xArray
        print(tf_x)
        tf_y = tf_fileClass.yArray
        
        dataTreeFrame.update_TreeView(tf_x, tf_y, dataTreeFrame.tf_dataTree, dataTreeFrame.tf_scrollbar)


#main fcn that calls fcns to make window
def main():
    root = Tk()
    app = main_window(root)

    root.mainloop()
    #root.destroy()

#housekeeping to call main
if __name__ == '__main__':
    main()