import tkinter as tk
from tkinter import ttk
import os

from thoughts import Collection, Project, Note

# TODOS:
# TODO: Fix error when adding note
# TODO: Make note editor work when switching notes / creating notes
# TODO: Apply this https://stackoverflow.com/questions/71859022/tkinter-notebook-create-new-tabs-by-clicking-on-a-plus-tab-like-every-web-brow/71861284#71861284
# TODO: Make delete options for notes, projects and collections
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
        self.project_entries = dict()

        self.active_project = None
        self.active_note = None
        self.note_edditor = None
        self.new_collection_entry = None
        self.create_new_note_button = None

        # Draw the main frame and
        self.root = tk.Tk()
        self.root.geometry('850x450')
        self.root.minsize(850, 450)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Add notebook structure where each notebook corresponds to a
        # collection
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        # Append all collections based on folders in the path
        # Notice, this is NOT robust to outside temporing with the files
        collection_folders = os.listdir(app_folder)
        for collection_name in collection_folders:
            self.add_collection_page(collection_name=collection_name)

        # Add a an extra frame which purpose is to add new frames
        self.add_new_collection_fan_button()

        self.root.title("Thoughts")
        self.root.geometry('1600x900')
        self.root.protocol("WM_DELETE_WINDOW", self.clean_up)
        self.root.mainloop()

    def add_new_collection_fan_button(self):
        self.new_collection_entry = tk.Entry(self.notebook, text="CollectionName")
        self.new_collection_entry.bind(sequence='<Return>', func=self.add_new_collection_from_entry)
        self.notebook.add(self.new_collection_entry, text="+")

    def add_new_collection_from_entry(self, *args):
        collection_name = self.new_collection_entry.get()
        if collection_name not in self.collections.keys():
            self.new_collection_entry.destroy()
            self.add_collection_page(collection_name=collection_name)
            self.add_new_collection_fan_button()
        else:
            tab_id = list(self.collections.keys()).index(collection_name)
            self.notebook.select(tab_id)

    def add_collection_page(self, collection_name):
        collection_frame = ttk.Frame(self.notebook)
        collection_frame.grid_rowconfigure(0, weight=1)
        collection_frame.grid_columnconfigure(2, weight=1)

        projects_frame = tk.Label(collection_frame,
                                  text="ProjectsFrameHere",
                                  anchor=tk.CENTER)
        projects_frame.grid(row=0, column=0, sticky="nsew")

        notes_frame = tk.Label(collection_frame, text="NotesFrameHere",
                               anchor=tk.CENTER)
        notes_frame.grid(row=0, column=1, sticky="nsew")

        action_frame = tk.Label(collection_frame, text="ActionFrameHere",
                                anchor=tk.CENTER)
        action_frame.grid(row=0, column=2, columnspan=3, rowspan=2,
                          sticky="nsew")

        self.notebook.add(collection_frame, text=collection_name)

        self.collections.update({collection_name: Collection(
            folder=app_folder, name=collection_name)})
        self.collection_frames.update({collection_name: collection_frame})
        self.projects_frames.update({collection_name: projects_frame})
        self.notes_frames.update({collection_name: notes_frame})
        self.action_frames.update({collection_name: action_frame})

        # Add selection buttons to the projects frame
        for key in self.collections[collection_name].projects.keys():
            # Notice, by assigning the button project_name in a lambda
            # the project_name becomes fixed
            # and thus references the actual project name
            project_button = tk.Button(
                master=projects_frame,
                text=key,
                activebackground="lightgrey",
                bg="grey",
                command=lambda project_name=key: self.project_button_click(
                    project_name)
            )
            project_button.pack(fill='both')

        # Add a "create new project" button
        self.add_create_new_project_button(collection_name=collection_name, projects_frame=projects_frame)

    def add_create_new_project_button(self, collection_name, projects_frame):
        create_new_project_button = tk.Entry(
            master=projects_frame,
            text="New Project Name",
        )
        create_new_project_button.bind(sequence='<Return>', func=self.add_new_project)
        create_new_project_button.pack(fill='both')
        self.project_entries.update({collection_name: create_new_project_button})

    def add_new_project(self, *args):
        project_name_entry = self.project_entries[self.active_collection.name]
        new_project_name = project_name_entry.get()
        project_name_entry.destroy()

        self.active_collection.add_project(project_name=new_project_name)
        self.add_project_button(
            project_name=new_project_name,
            project_frame=self.projects_frames[self.active_collection.name]
        )
        # Add a "create new project" button
        self.add_create_new_project_button(collection_name=self.active_collection.name,
                                           projects_frame=self.projects_frames[self.active_collection.name])

    def add_project_button(self, project_name, project_frame):
        project_button = tk.Button(
            master=project_frame,
            text=project_name,
            activebackground="lightgrey",
            bg="grey",
            command=lambda project_name=project_name: self.project_button_click(
                project_name)
        )
        project_button.pack(fill='both')

    def clean_up(self):
        if self.note_edditor is not None:
            self.active_note.update_text(self.note_edditor.get(1.0, tk.END))

        self.root.destroy()

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
            # Notice, by assigning the button project_name in a lambda,
            # the project_name becomes fixed
            # and thus references the actual project name
            note_button = tk.Button(
                master=self.notes_frames[self.active_collection.name],
                text=key,
                activebackground="lightgrey",
                bg="grey",
                command=lambda note_name=key: self.note_button_click(note_name)
            )
            note_button.pack(fill='both')

        # Add a note button to add a new note
        self.add_create_new_note_button(notes_frames=self.notes_frames[self.active_collection.name])

    def add_create_new_note_button(self, notes_frames):
        self.create_new_note_button = tk.Entry(
            master=notes_frames,
            text="New Project Name",
        )
        self.create_new_note_button.bind(sequence='<Return>', func=lambda x=notes_frames: self.add_new_note_from_entry(notes_frame=x))
        self.create_new_note_button.pack(fill='both')

    def add_new_note_from_entry(self, notes_frame):
        new_note_name = self.create_new_note_button.get()
        self.add_new_note(note_name=new_note_name, notes_frames=notes_frame)
        self.create_new_note_button.destroy()
        self.add_create_new_note_button(notes_frames=notes_frame)

    def add_new_note(self, note_name, notes_frames):
        # Notice, by assigning the button project_name in a lambda,
        # the project_name becomes fixed
        # and thus references the actual project name
        note_button = tk.Button(
            master=notes_frames,
            text=note_name,
            activebackground="lightgrey",
            bg="grey",
            command=lambda x=note_name: self.note_button_click(x)
        )
        self.active_project.add_note(name=note_name)
        note_button.pack(fill='both')

    def note_button_click(self, note_name):
        # Clear the old editor
        if self.note_edditor is not None:
            self.active_note.update_text(self.note_edditor.get(1.0, tk.END))
            self.note_edditor.destroy()

        # Get the note text and make a new editor
        self.note_edditor = tk.Text(
            self.action_frames[self.active_collection.name]
        )
        # TODO: Check whether notes are saved correctly
        self.active_note = self.active_project.notes[note_name]
        self.note_edditor.insert(tk.INSERT, self.active_note.text)
        self.note_edditor.pack()

# Organizing in row/columns: for notes
# https://stackoverflow.com/questions/21738149/make-tkinter-buttons-for-every-item-in-a-list

app_folder = "C:/test/thoughts/"

app = ThoughtsApp(app_folder=app_folder)






# TODO: Make a GUI
