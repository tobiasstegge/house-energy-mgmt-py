import tkinter as tk
from tkinter import Button, Label
from evaluate import Evaluator
from export_data import ExportExcel
import matplotlib.pyplot as plt


class CalculationButtons(tk.Frame):
    def __init__(self, parent, static_file, dynamic_file, appliances, methods_radio, path):
        super().__init__(parent)
        self.parent = parent
        self.plt = None
        self.path = path
        self.show_plots = False
        self.appliances = appliances
        self.methods_radio = methods_radio
        self.evaluator = Evaluator(static_file, dynamic_file)
        self.start_calculation_button = Button(
            parent,
            text='Start Calculation',
            command=self.__start_calculation
        )
        self.start_calculation_button.grid(sticky='NESW')
        self.calculation_finished = False

    def __start_calculation(self):
        values = [None, "price", "efficiency", "max_renewables"]

        self.evaluator.calculate_energy_services()
        self.evaluator.choose_appliances(values[self.methods_radio.active_var.get()])
        self.evaluator.calculate_end_use()
        self.evaluator.choose_conversion_technologies(values[self.methods_radio.active_var.get()])
        self.evaluator.optimize_final_energy()

        ExportExcel(evaluator=self.evaluator, path=self.path)

        self.label_success = Label(
            self.parent,
            text=f'Success! Your data excel sheet is saved here: \n {self.path}',
        )
        self.label_success.grid(sticky='NESW')

        self.button_plots = Button(
            self.parent,
            text="Show plots",
            command=self.plots

        )
        self.button_plots.grid(sticky='NESW')

    def plots(self):
        hours = list(range(0, 24))
        plt.plot(hours, self.evaluator.end_use_total_electricity,
                 hours, self.evaluator.electricity_from_solar,
                 hours, self.evaluator.electricity_from_storage,
                 hours, self.evaluator.electricity_to_storage,
                 hours, self.evaluator.electricity_from_grid,
                 hours, self.evaluator.electricity_to_grid,
                 hours, self.evaluator.soc_battery)
        plt.xlabel('hours')
        plt.ylabel('kWh')
        plt.legend(["Total Electricity", "Energy from Solar", "Electricity from Storage", "Electricity to Storage",
                    "Electricity from Grid", "Electricity to Grid", "State of Charge Battery"])
        plt.show()
