#interface.py constructs a front-end GUI for a user to work with

#imports
import tkinter as tk
from tkinter.filedialog import askopenfilename
import pandas as pd
from pandastable import Table
import warnings

def run_gui():
    #ignore useless warnings of impending doom (i.e., future deprecated pandas functions)
    warnings.simplefilter(action='ignore', category=FutureWarning)

    #***init variables***
    #functions
    def get_entry():
        query = query_string.get()
        return query

    def get_path():
        path = askopenfilename(initialdir="Project_dir", filetypes=[("Comma Separated Values", "*.csv")])
        return path

    def load_data():
        path = get_path()
        df = pd.read_csv(path) #path was redefined to match the path directory returned in open_csv()
        table = pt = Table(viewer_frame, dataframe=df, showtoolbar=False, showstatusbar= True)
        pt.show()
        pt.redraw()



    #objects
    window = tk.Tk()

    #menu
    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Import", command=load_data)
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    #frames
    main_frame = tk.Frame(window)
    viewer_frame = tk.Frame(main_frame, padx=5, pady=10, bg="lightgreen")
    query_frame = tk.Frame(main_frame, height=25, padx=5, pady=10, bg = "green")
    text_entry = tk.Entry(query_frame, text= "Insert query here...", width=500)
    search_button = tk.Button(query_frame, text="Search", width=10)

    #non-tkinter vars
    icon = tk.PhotoImage(file="Project_dir/res/sloth_png.png")
    query_string = tk.StringVar(master=query_frame)
    path = ""

    #modify vars
    text_entry.configure(textvariable=query_string)
    window.config(menu=menubar)

    #window configs(title, size, icon, bg-color)
    window.title('SloSlu')
    window.geometry('800x500')
    window.iconphoto(True, icon)
    window.config(bg="skyblue")

    #frame locations
    main_frame.grid(row=0, column=0, padx=10, pady=10, sticky=('NSEW'))
    viewer_frame.grid(row=0, column=0, padx=10, pady=5, sticky=('NSEW'))
    query_frame.grid(row=1, column=0, padx=10, pady=5, sticky=('NSEW'))

    #adding components to Query Frame
    text_entry.grid(row=0, column=0, padx=5, pady=5)
    search_button.grid(row=0,column=1, padx=5, pady=5)


    #configure grid
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=1)

    viewer_frame.columnconfigure(0, weight=1)
    viewer_frame.rowconfigure(0, weight=1)

    query_frame.columnconfigure(0, weight=1)
    query_frame.rowconfigure(0, weight=1)

    #run
    window.mainloop()