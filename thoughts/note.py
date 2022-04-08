import os


class Note:
    def __init__(self, parent_folder: str, note_id: str):
        self.parent_folder = parent_folder
        self.note_id = note_id
        self.note_path = parent_folder + note_id + ".txt"

        # Open or create file it does not exists
        # Notice this opens in append mode
        self.file = open(self.note_path, 'w+')
        self.text = self.file.readlines()

    def __del__(self):
        """
        Ensure to close the note file when the note is deleted
        """
        self.file.close()

    def delete(self):
        os.remove(self.note_path)
