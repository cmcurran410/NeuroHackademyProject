#this script builds a GUI that will open upon clicking a pandas cell and then display 
# data/visualizations. It will also give the option to save the window as a file (what kind?)

#imports
import tkinter as tk

#vars-global

def display_window():
    #init window
    window = tk.Tk()

    #vars--local
    icon = tk.PhotoImage(file="Project_dir/res/images/sloth_sleuth.png")

    #window configs
    window.title("SlothSleuth DisplayPort")
    window.geometry('420x560')
    window.iconphoto(True, icon)
    window.config(bg="skyblue")

    #frames
    viewframe = tk.Frame(master=window)
    viewframe.grid(row=0, column=0, padx=10, pady=5, sticky=('NSEW'))

    viewframe.columnconfigure(0, weight=1)
    viewframe.rowconfigure(0, weight=1)
    
    #init components
    title_label = tk.Label(text="Title", font=("Times New Roman", 24, "bold"))
    author_label = tk.Label(text="Authors et al.", font=("Times New Roman", 16, "bold"))
    date_label = tk.Label(text="2024", bg = "skyblue", font=("Times New Roman", 16, "bold"))

    saveButton = tk.Button(text="Save")

    #organize components onto frame
    title_label.grid(row=0, column=0, padx=5, pady=5)
    author_label.grid(row=1, column=0, padx=5, pady=5)
    date_label.grid(row=2, column=0, padx=5, pady=5)
    saveButton.grid(row=4, column=4, padx= 5, pady= 5)

    #run
    window.mainloop()

display_window()