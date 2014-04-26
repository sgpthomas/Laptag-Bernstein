#! python3
"""

Laptag Bernstein Wave Analyzation Program with Tkinter User Interface
written by Sam Thomas

"""
#imports
from tkinter import *
from tkinter.ttk import *
import matplotlib.pyplot as plt
import sys

#global vars
window_width = 800
window_height = 600

#argument
try:
    dataFilePath = sys.argv[1]
    mathFilePath = sys.argv[2]
except:
    dataFilePath = ''
    mathFilePath = ''
    print("No Path Given")
    print("No Math File Given")

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

        #menubar
        self.menubar = Menu(self.parent)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Save", command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit", command=self.quitWindow)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        #display menubar
        self.parent.config(menu=self.menubar)

        #some random bindings
        self.parent.bind("<Control-q>", self.quitWindow)

    def save(self):
        #TODO - add save functionality
        print('save')

    def quitWindow(self, *event):
        self.parent.destroy()

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
        self.parent = parent
        #path widgets
        self.font = ('Ubuntu', 12)
        self.initPathWidgets()
        self.initMathWidgets()
        self.initGraphWidgets()

        self.arrays = []
        self.mathFileImport = None

    def initGraphWidgets(self):
        #label
        self.graphLabel = Label(self.infoFrame, text='Graph Options', font=self.font)
        self.graphLabel['foreground'] = 'blue'
        self.graphLabel.grid(column=3, row=0, pady=5, padx=20)
        #graph button
        self.graphButton = Button(self.infoFrame, text="Graph", command=self.graphButtonCmd)
        self.graphButton.grid(column=3, row=1, pady=5, padx=20)
        #close graph button
        self.closeGraphButton = Button(self.infoFrame, text="Close Graph", command=plt.close)
        self.closeGraphButton.grid(column=3, row=2, pady=5, padx=20)

    def initMathWidgets(self):
        #Label
        self.mathLabel = Label(self.infoFrame, text='Math File', font=self.font)
        self.mathLabel['foreground'] = 'blue'
        self.mathLabel.grid(column=1, row=0, pady=5, padx=20)
        #LabelStatus
        self.mathLabelStatus = Label(self.infoFrame, text='File: NONE', font=self.font)
        self.mathLabelStatus['foreground'] = 'red'
        self.mathLabelStatus.grid(column=1, row=1, pady=5, padx=20)
        #maybe a math file entry box
        self.mathEntryText = StringVar()
        self.mathEntry = Entry(self.infoFrame, textvariable=self.mathEntryText)
        self.mathEntry.insert(0, mathFilePath)
        self.mathEntry.grid(column=1, row=2, pady=5, padx=20)
        #paste button
        self.mathPasteButton = Button(self.infoFrame, text="Paste", command=self.mathEntryPaste)
        self.mathPasteButton.grid(column=1, row=4, pady=5, padx=20)
        #button to make graph
        self.mathButton = Button(self.infoFrame, text="Define Math File", command=self.mathButtonCmd)
        self.mathButton.grid(column=1, row=3, pady=5, padx=20)

    def initPathWidgets(self):
        #Label
        self.infoFrameLabel = Label(self.infoFrame, text='Data File Path', font=self.font)
        self.infoFrameLabel['foreground'] = 'blue'
        self.infoFrameLabel.grid(column=0, row=0, pady=5, padx=10)
        #Label Status
        self.pathStatusLabel = Label(self.infoFrame, text='Path: NONE', font=self.font)
        self.pathStatusLabel['foreground'] = 'red'
        self.pathStatusLabel.grid(column=0, row=1, pady=5, padx=10)
        #path entry box
        self.pathEntryText = StringVar()
        self.pathEntry = Entry(self.infoFrame, textvariable=self.pathEntryText)
        self.pathEntry.insert(0, dataFilePath)
        self.pathEntry.grid(column=0, row=2, pady=5, padx=10)
        #paste button
        self.pathPasteButton = Button(self.infoFrame, text="Paste", command=self.pathEntryPaste)
        self.pathPasteButton.grid(column=0, row=4, pady=5, padx=10)
        #button
        self.pathButton = Button(self.infoFrame, text="Update", command=self.pathButtonCmd)
        self.pathButton.grid(column=0, row=3, pady=5, padx=10)

    def pathButtonCmd(self):
        path = self.pathEntry.get()
        self.arrays = dataTreeFrame.update_DataTree(path)
        if self.arrays != [[],[]]:
            self.pathStatusLabel['text'] = "Path: " + path
            self.pathStatusLabel['foreground'] = 'green'
            self.pathEntryText.set("")
        else:
            self.pathStatusLabel['text'] = "Path: NONE"
            self.pathStatusLabel['foreground'] = 'red'

    def mathButtonCmd(self):
        mathFilePath = self.mathEntry.get()
        try:
            self.mathFileImport = __import__(mathFilePath)
            self.mathLabelStatus['text'] = "File: " + mathFilePath
            self.mathLabelStatus['foreground'] = 'green'
            self.mathEntryText.set("")
        except:
            self.mathFileImport = None
            self.mathLabelStatus['text'] = "File: NONE"
            self.mathLabelStatus['foreground'] = 'red'

    def graphButtonCmd(self):
        try:   
            newArrays = self.mathFileImport.analyze(self.arrays)
            plt.plot(newArrays[0], newArrays[1])
        except:
            plt.plot(self.arrays[0], self.arrays[1])

        plt.show()

    def mathEntryPaste(self, *event):
        try:
            self.mathEntryText.set(self.parent.clipboard_get())
        except:
            print('Nothing On Clipboard')

    def pathEntryPaste(self, *event):
        try:
            self.pathEntryText.set(self.parent.clipboard_get())
        except:
            print('Nothing On Clipboard')
        
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
        tf_y = tf_fileClass.yArray
        tf_arrays = [tf_x, tf_y]
        
        dataTreeFrame.update_TreeView(tf_x, tf_y, dataTreeFrame.tf_dataTree, dataTreeFrame.tf_scrollbar)

        return tf_arrays


#main fcn that calls fcns to make window
def main():
    root = Tk()
    img = PhotoImage(file='icon.png')
    root.tk.call('wm', 'iconphoto', root._w, img)
    app = main_window(root)

    root.mainloop()
    #root.destroy()

#housekeeping to call main
if __name__ == '__main__':
    main()