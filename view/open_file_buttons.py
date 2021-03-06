import tkinter as tk
from tkinter import Button
from tkinter.filedialog import askopenfile, askdirectory


class OpenFileButton(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent)
        self.dynamic_file = None
        self.static_file = None
        self.file_path_output = None
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

        self.open_output_dynamic = Button(
            parent,
            text='Pick Output Directory for Excel',
            command=self.__open_output_dir
        )

        self.open_button_static.grid(sticky='NESW')
        self.open_button_dynamic.grid(sticky='NESW')
        self.open_output_dynamic.grid(sticky='NESW')

    def __open_static_file(self):
        file_path = askopenfile(mode='r', filetypes=[('CSV', '*csv')])
        if file_path is not None:
            self.static_file = file_path.name

    def __open_dynamic_file(self):
        file_path = askopenfile(mode='r', filetypes=[('CSV', '*csv')])
        if file_path is not None:
            self.dynamic_file = file_path.name

    def __open_output_dir(self):
        file_path = askdirectory()
        if file_path is not None:
            self.file_path_output = file_path
