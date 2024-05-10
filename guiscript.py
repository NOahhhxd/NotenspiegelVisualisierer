import tkinter as tk

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
def selectModules():
    global modules, returnValues
    if root:
        returnValues = [modules[i] for i in range(len(modules)) if checkBtns[i].get() == 1]
        # print(selected)
        root.destroy()

def visualize(mods):

    global root,checkBtns, modules
    modules = mods
    root = tk.Tk()
    root.title("Notenspiegel Visualizer")
    # tk.Label(root, text="Notenspiegel", width=20, font="Arial").grid(row=0, column=0)
    # tk.Button(root, text="Auswahl bestätigen", width=10, font="Arial").grid(row=1, column=0)
    for i in range(len(modules)):
        btnVal = tk.IntVar()
        tk.Checkbutton(root, variable=btnVal).grid(row=(i + 1), column=0)
        checkBtns.append(btnVal)
    [tk.Label(root, text=modules[i][0]).grid(row=(i + 1), column=1, ipadx=0) for i in range(len(modules))]
    tk.Button(root, text="Auswahl bestätigen", width=10, font="Arial", command=selectModules).grid(row=len(modules) + 1,
                                                                                                   column=0)
    root.mainloop()

    # reset vars
    root = None
    checkBtns = []
    modules = []
    return returnValues

# print(visualize(modules))