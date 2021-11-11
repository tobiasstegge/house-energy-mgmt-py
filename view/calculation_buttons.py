import tkinter as tk
from tkinter import Button
from evaluate import Evaluator


class CalculationButtons(tk.Frame):
    def __init__(self, parent, static_file, dynamic_file, appliance_boxes, appliances):
        super().__init__(parent)
        self.appliances = appliances
        self.appliance_boxes = appliance_boxes
        self.evaluator = Evaluator(static_file, dynamic_file)
        self.start_calculation_button = Button(
            parent,
            text='Start Calculation',
            command=self.__start_calculation
        )
        self.start_calculation_button.grid(row=7, column=5)

    def __start_calculation(self):
        self.evaluator.house.cooker = self.appliances.cookers[self.appliance_boxes.box_cooker.current()]
        self.evaluator.house.space_heater = self.appliances.space_heaters[self.appliance_boxes.box_heater.current()]
        self.evaluator.house.hot_water_heater = self.appliances.hot_water[self.appliance_boxes.box_water.current()]
        self.evaluator.house.space_cooler = self.appliances.space_coolers[self.appliance_boxes.box_cooler.current()]
        self.evaluator.house.lights = self.appliances.lighting[self.appliance_boxes.box_lights.current()]

        self.evaluator.calculate_energy_services()
        self.evaluator.choose_appliances('price')
        self.evaluator.calculate_end_use()
        self.evaluator.choose_conversion_technologies('price')
        self.evaluator.optimize_final_energy()
