import tkinter as tk
from tkinter import Button
from tkinter.filedialog import askopenfile


class OpenFileButton(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent)
        self.open_button_static = Button(
            parent,
            text='Open Static File',
            command=self.__open_static_file
        )

        self.open_button_dynamic = Button(
            parent,
            text='Open Dynamic File',
            command=self.__open_dynamic_file
        )

        self.open_button_static.grid(row=3, column=3, columnspan=3, sticky='NESW')
        self.open_button_dynamic.grid(row=6, column=5)

    def __open_static_file(self):
        file_path = askopenfile(mode='r', filetypes=[('CSV', '*csv')], initialdir='./examples')
        if file_path is not None:
            self.static_file = file_path.name

    def __open_dynamic_file(self):
        file_path = askopenfile(mode='r', filetypes=[('CSV', '*csv')], initialdir='./example')
        if file_path is not None:
            self.dynamic_file = file_path.name
