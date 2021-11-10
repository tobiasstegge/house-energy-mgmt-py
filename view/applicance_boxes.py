import tkinter as tk
from tkinter import Label
from tkinter.ttk import Combobox


class AppliancesBoxes(tk.Frame):
    def __init__(self, parent, appliances, **kw):
        super().__init__(**kw)
        self.parent = parent

        self.label_cooker = Label(self.parent, text="Choose Cooker")
        self.label_cooker.grid(row=8, column=5)
        self.box_cooker = Combobox(self.parent, values=[item['name'] for item in appliances.cookers])
        self.box_cooker.grid(row=9, column=5)

        self.label_heater = Label(self.parent, text="Choose Heater")
        self.label_heater.grid(row=10, column=5)
        self.box_heater = Combobox(self.parent, values=[item['name'] for item in appliances.space_heaters])
        self.box_heater.grid(row=11, column=5)

        self.label_heater = Label(self.parent, text="Choose Water Heater")
        self.label_heater.grid(row=12, column=5)
        self.box_water = Combobox(self.parent, values=[item['name'] for item in appliances.hot_water])
        self.box_water.grid(row=13, column=5)

        self.label_cooler = Label(self.parent, text="Choose Space Cooler")
        self.label_cooler.grid(row=14, column=5)
        self.box_cooler = Combobox(self.parent, values=[item['name'] for item in appliances.space_coolers])
        self.box_cooler.grid(row=15, column=5)

        self.label_lights = Label(self.parent, text="Choose Lights")
        self.label_lights.grid(row=16, column=5)
        self.box_lights = Combobox(self.parent, values=[item['name'] for item in appliances.lighting])
        self.box_lights.grid(row=17, column=5)
