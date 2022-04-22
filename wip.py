import tkinter as tk
from tkinter import ttk


class MyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('850x450')
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        self.frames = []
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Frame1")
        self.frames.append(frame)

        self.new_frame_button = tk.Button(self.notebook, command=self.command_add_frame)
        self.notebook.add(self.new_frame_button, text="+")

        self.root.mainloop()

    def command_add_frame(self):
        frame_new = tk.Frame(self.notebook)
        self.frames.append(frame_new)
        self.notebook.add(frame_new, text=f"Frame{len(self.frames)}")


app = MyApp()