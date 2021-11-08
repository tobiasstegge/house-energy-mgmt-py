import tkinter as tk
from tkinter import Button, Label, Entry, END
from tkinter.filedialog import askopenfile
from evaluate import Evaluator


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title = "Test"
        self.parent.geometry('300x200')
        self.static_file = None
        self.dynamic_file = None

        self.open_button_static = Button(
            self.parent,
            text='Open Static File',
            command=self.__open_static_file
        )
        self.open_button_dynamic = Button(
            self.parent,
            text='Open Dynamic File',
            command=self.__open_dynamic_file
        )

        self.start_calculation_button = Button(
            self.parent,
            text='Start Calculation',
            command=self.__start_calculation
        )

        self.open_button_static.grid(row=3, column=3, columnspan=3, sticky='NESW')
        self.open_button_dynamic.grid(row=6, column=5)
        self.start_calculation_button.grid(row=7, column=5)

    def __open_static_file(self):
        file_path = askopenfile(mode='r', filetypes=[('CSV', '*csv')], initialdir='./examples')
        if file_path is not None:
            self.static_file = file_path.name

    def __open_dynamic_file(self):
        file_path = askopenfile(mode='r', filetypes=[('CSV', '*csv')], initialdir='./example')
        if file_path is not None:
            self.dynamic_file = file_path.name

    def __start_calculation(self):
        evaluator = Evaluator(self.static_file, self.dynamic_file)
        demand = evaluator.calculate_demand()
