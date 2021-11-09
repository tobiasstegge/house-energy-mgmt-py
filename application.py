import tkinter as tk
from tkinter import Button, Label
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfile
from evaluate import Evaluator
from appliances import Appliances


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title = "Test"
        self.parent.geometry('250x400')
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

        self.label_cooker = Label(self.parent, text="Choose Cooker")
        self.label_cooker.grid(row=8, column=5)
        self.box_cooker = Combobox(self.parent,
                                 values=list(
                                     Appliances('./examples/End_Use_Technologies_DataBase.xlsx').cookers.keys()))
        self.box_cooker.grid(row=9, column=5)

        self.label_heater = Label(self.parent, text="Choose Heater")
        self.label_heater.grid(row=10, column=5)
        self.box_heater = Combobox(self.parent, values=list(
            Appliances('./examples/End_Use_Technologies_DataBase.xlsx').space_heaters_water.keys()) + list(
            Appliances('./examples/End_Use_Technologies_DataBase.xlsx').space_heaters_electric.keys()))
        self.box_heater.grid(row=11, column=5)

        self.label_heater = Label(self.parent, text="Choose Water Heater")
        self.label_heater.grid(row=12, column=5)
        self.box_water = Combobox(self.parent, values=list(
            Appliances('./examples/End_Use_Technologies_DataBase.xlsx').hot_water.keys()))
        self.box_water.grid(row=13, column=5)

        self.label_cooler = Label(self.parent, text="Choose Space Cooler")
        self.label_cooler.grid(row=14, column=5)
        self.box_cooler = Combobox(self.parent, values=list(
            Appliances('./examples/End_Use_Technologies_DataBase.xlsx').space_coolers.keys()))
        self.box_cooler.grid(row=15, column=5)

        self.label_lights = Label(self.parent, text="Choose Lights")
        self.label_lights.grid(row=16, column=5)
        self.box_lights = Combobox(self.parent, values=list(
            Appliances('./examples/End_Use_Technologies_DataBase.xlsx').lighting.keys()))
        self.box_lights.grid(row=17, column=5)

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

        evaluator.house.cooker = self.box_cooker.get()
        evaluator.house.heater = self.box_heater.get()
        evaluator.house.water_heater = self.box_water.get()
        evaluator.house.cooler = self.box_cooler.get()
        evaluator.house.lights = self.label_lights.get()

        evaluator.calculate_energy_services()
