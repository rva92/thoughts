import tkinter as tk
from tkinter import ttk
import os


from thoughts import Collection, Project, Note

# Organizing in row/columns: for notes
# https://stackoverflow.com/questions/21738149/make-tkinter-buttons-for-every-item-in-a-list

app_folder = "C:/test/thoughts/"

# Create or load a collection
collection = Collection(folder=app_folder, name="MyFirstCollection")

# Create a project under the collection
project1 = collection.add_project(project_name="MyFirstProject")
project2 = collection.add_project(project_name="MySecondProject")
project3 = collection.add_project(project_name="MyThirdProject")


collections = sub_folders = [f.name for f in os.scandir(app_folder) if f.is_dir()]
collections += ""

root = tk.Tk()
root.geometry('850x450')
root.minsize(850, 450)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky='nsew')


for collection in collections:
    collection_frame = ttk.Frame(notebook)
    collection_frame.grid_rowconfigure(0, weight=1)
    collection_frame.grid_columnconfigure(2, weight=1)

    # TODO: Make these dynamic based on collections
    projects_frame = tk.Label(collection_frame, text="ProjectsFrameHere", anchor=tk.CENTER)
    projects_frame.grid(row=0, column=0, sticky="nsew")

    notes_frame = tk.Label(collection_frame, text="NotesFrameHere", anchor=tk.CENTER)
    notes_frame.grid(row=0, column=1, sticky="nsew")

    action_frame = tk.Label(collection_frame, text="ActionFrameHere", anchor=tk.CENTER)
    action_frame.grid(row=0, column=2, columnspan=3, rowspan=2, sticky="nsew")

    notebook.add(collection_frame, text=collection)

root.title("Thoughts")
root.geometry('1600x900')


root.mainloop()









# TODO: Make a GUI
