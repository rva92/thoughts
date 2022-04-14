import atexit
import os


class Note:
    def __init__(self, parent_folder: str, note_id: str):
        self.parent_folder = parent_folder
        self.note_id = note_id
        self.note_path = parent_folder + note_id + ".txt"

        # Read the content of the file
        if os.path.isfile(self.note_path):
            file = open(self.note_path, 'r')
            self.text = file.readlines()
            if isinstance(self.text, list):
                self.text = "".join(self.text)
            file.close()
        else:
            self.text = ""

        # Define exit clause
        atexit.register(self.save_file)

    def delete(self):
        os.remove(self.note_path)

    def save_file(self):
        file = open(self.note_path, 'w')
        file.write(self.text)
        file.close()

    def update_text(self, text: str):
        self.text = text
        self.save_file()
