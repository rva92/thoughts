import os

from .note import Note


class Project:
    def __init__(self, parent_folder: str, name: str):
        self.parent_folder = parent_folder
        self.name = name
        self.project_path = self.parent_folder + self.name + "/"
        self.notes = {}
        if not os.path.isdir(self.project_path):
            # Note in this case mkdir is used as projects are only used
            # inside a collection, hence the outerfolder should exists the
            # app is in a corrupted state. In the future, handling of this
            # is a priority
            os.mkdir(self.project_path)

        # Load all notes under the collection, if any
        sub_folders = os.listdir(self.project_path)
        for note_file_name in sub_folders:
            note_id = note_file_name.replace(".txt", "")
            self.notes.update({note_id: Note(
                parent_folder=self.project_path,
                note_id=note_id
            )})

    def delete(self):
        """
        Deletes the project. Notice, this an irreversible decision
        """
        for k, note in self.notes:
            note.delete()

    def add_note(self, name=None):
        """
        Adds a note to the project. If the name already exists this
        function has not action.

        If a name is not provided, a random note name is made as:
            "Note note_number"

        -----
        :param name:
            String with the name of the note

        :return:
            The note instance
        """
        if name is None:
            # Find the hihgest of either the lenght of note or a previous
            # custom note name
            number_of_notes = len(self.notes.keys())
            notes_number = [
                int(x.lower().split("note ")[1].replace(".txt", ""))
                for x in self.notes.keys() if "Note " in x
            ]
            largest_note_number = max(notes_number) if notes_number else 0
            new_node_number = max(number_of_notes, largest_note_number)
            new_node_number += 1
            note_name = "Note " + str(new_node_number)
        else:
            if name  in self.notes.keys():
                print(f"A note with the name {name} already exists in the "
                      f"project under the project {self.name}")
            note_name = name

        self.notes.update({
            note_name: Note(parent_folder=self.project_path, note_id=note_name)
        })

        return self.notes[note_name]
