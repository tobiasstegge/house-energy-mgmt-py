import tkinter as tk
from tkinter import Label


class AppliancesLabels(tk.Frame):
    def __init__(self, parent, house, **kw):
        super().__init__(**kw)
        self.parent = parent

        self.label_heater_des = Label(self.parent, text="Space Heater")
        self.label_heater = Label(self.parent, text=house.space_heater['name'])
        self.label_heater_des.grid(sticky="S")
        self.label_heater.grid(sticky="S")

        self.label_cooker_des = Label(self.parent, text="Cooker")
        self.label_cooker = Label(self.parent, text=house.cooker['name'])
        self.label_cooker_des.grid(sticky="S")
        self.label_cooker.grid(sticky="S")

        self.label_w_heater_des = Label(self.parent, text="Name")
        self.label_w_heater = Label(self.parent, text=house.hot_water_heater['name'])
        self.label_w_heater_des.grid(sticky="S")
        self.label_w_heater.grid(sticky="S")

        self.label_cooler_des = Label(self.parent, text="Space Cooler")
        self.label_cooler = Label(self.parent, text=house.space_cooler['name'])
        self.label_cooler_des.grid(sticky="S")
        self.label_cooler.grid(sticky="S")

        self.label_lights_des = Label(self.parent, text="Light")
        self.label_lights = Label(self.parent, text=house.light['name'])
        self.label_lights_des.grid(sticky="S")
        self.label_lights.grid(sticky="S")
