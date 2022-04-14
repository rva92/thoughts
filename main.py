import tkinter as tk
from tkinter import ttk
import os


from thoughts import Collection, Project, Note

# TODOS:
# TODO: Ensure notes are saved when switching and when closing the application
# TODO: Add autosave?
# TODO: Make a "create new collection button"
# TODO: Make a "create a new note button"
# TODO: Make a "create a new project button"
# TODO: Improve button design
# TODO: Improve layout
# TODO: Make color schemes


class ThoughtsApp:
    def __init__(self, app_folder: str):
        self.app_folder = app_folder
        self.collections = dict()
        self.collection_frames = dict()
        self.projects_frames = dict()
        self.notes_frames = dict()
        self.action_frames = dict()

        self.active_project = None
        self.active_note = None
        self.note_edditor = None

        # Draw the main frame and
        self.root = tk.Tk()
        self.root.geometry('850x450')
        self.root.minsize(850, 450)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Add notebook structure where each notebook corresponds to a collection
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        # Append all collections based on folders in the path
        # Notice, this is NOT robust to outside temporing with the files
        collection_folders = os.listdir(app_folder)
        for collection_name in collection_folders:
            collection_frame = ttk.Frame(self.notebook)
            collection_frame.grid_rowconfigure(0, weight=1)
            collection_frame.grid_columnconfigure(2, weight=1)

            projects_frame = tk.Label(collection_frame, text="ProjectsFrameHere", anchor=tk.CENTER)
            projects_frame.grid(row=0, column=0, sticky="nsew")

            notes_frame = tk.Label(collection_frame, text="NotesFrameHere", anchor=tk.CENTER)
            notes_frame.grid(row=0, column=1, sticky="nsew")

            action_frame = tk.Label(collection_frame, text="ActionFrameHere", anchor=tk.CENTER)
            action_frame.grid(row=0, column=2, columnspan=3, rowspan=2, sticky="nsew")

            self.notebook.add(collection_frame, text=collection_name)

            self.collections.update({collection_name: Collection(folder=app_folder, name=collection_name)})
            self.collection_frames.update({collection_name: collection_frame})
            self.projects_frames.update({collection_name: projects_frame})
            self.notes_frames.update({collection_name: notes_frame})
            self.action_frames.update({collection_name: action_frame})

            # Add selection buttons to the projects frame
            for key in self.collections[collection_name].projects.keys():
                # Notice, by assigning the button project_name in a lambda, the project_name becomes fixed
                # and thus references the actual project name
                project_button = tk.Button(
                    master=projects_frame,
                    text=key,
                    activebackground="lightgrey",
                    bg="grey",
                    command=lambda project_name=key : self.project_button_click(project_name)
                )
                project_button.pack(fill='both')

        self.root.title("Thoughts")
        self.root.geometry('1600x900')
        self.root.mainloop()

    @property
    def active_collection(self):
        collection_position_id = self.notebook.index("current")
        return self.collections[list(self.collections.keys())[collection_position_id]]

    def project_button_click(self, project_name):
        if self.active_note is not None:
            print("Remember to save note!")

        # Deselect the current note
        self.active_note = None

        # Clear current notes frame
        for widgets in self.notes_frames[self.active_collection.name].winfo_children():
            widgets.destroy()

        # Add notes button for the selected project
        self.active_project = self.active_collection.projects[project_name]

        for key in self.active_project.notes.keys():
            # Notice, by assigning the button project_name in a lambda, the project_name becomes fixed
            # and thus references the actual project name
            note_button = tk.Button(
                master=self.notes_frames[self.active_collection.name],
                text=key,
                activebackground="lightgrey",
                bg="grey",
                command=lambda note_name=key: self.note_button_click(note_name)
            )
            note_button.pack(fill='both')

    def note_button_click(self, note_name):
        # Clear the old editor
        if self.note_edditor is not None:
            self.note_edditor.destroy()

        # Get the note text and make a new editor
        self.note_edditor = tk.Text(
            self.action_frames[self.active_collection.name]
        )
        self.note_edditor.insert(tk.INSERT, self.active_project.notes[note_name].text)
        self.note_edditor.pack()

# Organizing in row/columns: for notes
# https://stackoverflow.com/questions/21738149/make-tkinter-buttons-for-every-item-in-a-list

app_folder = "C:/test/thoughts/"

app = ThoughtsApp(app_folder=app_folder)






# TODO: Make a GUI
