import sys
import tkinter as tk
import parse
from PIL import ImageTk, Image
"""
idea:
- table with all modules 
- checkbox for each module => if selected then modules will be included 
- maybe select which part of module (grade, number, name, passed etc) => more than 2 rows per entry
- submit button to continue to graph => include image of graph in application
"""

returnValues = []
root = None
checkBtns = []
modules = []
img = None


def generateImage():
    global img
    parse.plotModule(returnValues, headless=True).savefig("tmp.png")
    returnValues.clear()
    img = ImageTk.PhotoImage(Image.open("tmp.png").resize((500, 500), Image.ANTIALIAS))
    tk.Label(root, image=img).grid(row=0,column=2, rowspan=len(checkBtns), sticky=tk.NS)


def selectModules(returnsSomething=True):
    global modules, returnValues
    if root:
        returnValues = [modules[i] for i in range(len(modules)) if checkBtns[i].get() == 1]
        if returnsSomething:
            root.destroy()
        else:
            generateImage()

def visualize(mods, returnsSomething=True):
    global root,checkBtns, modules, returnValues
    returnValues = []
    modules = mods
    root = tk.Tk()
    root.title("Notenspiegel Visualizer")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width,height))
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=3)
    root.columnconfigure(2, weight=5)
    # root.geometry("500x600")
    # tk.Label(root, text="Notenspiegel", width=20, font="Arial").grid(row=0, column=0)
    # tk.Button(root, text="Auswahl bestätigen", width=10, font="Arial").grid(row=1, column=0)
    for i in range(len(modules)):
        btnVal = tk.IntVar()
        tk.Checkbutton(root, variable=btnVal).grid(row=(i + 1), column=0)
        checkBtns.append(btnVal)
    [tk.Label(root, text=modules[i][0]).grid(row=(i + 1), column=1, sticky=tk.W, ipadx=0) for i in range(len(modules))]
    tk.Button(root, text="Auswahl bestätigen", width=30, font="Arial", command=lambda: selectModules(returnsSomething)).grid(row=len(modules) + 1,
                                                                                                   column=0)
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit())
    root.mainloop()

    if returnsSomething:
        # reset vars
        root = None
        checkBtns = []
        m_cpy = [module for module in modules]
        modules = []
        if len(returnValues) == 0:
            return m_cpy
        return returnValues

# print(visualize(modules))