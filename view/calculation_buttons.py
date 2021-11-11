import tkinter as tk
from tkinter import Button, Entry, END
from evaluate import Evaluator
from export_data import ExportExcel


class CalculationButtons(tk.Frame):
    def __init__(self, parent, static_file, dynamic_file, appliances, methods_radio):
        super().__init__(parent)
        self.parent = parent
        self.appliances = appliances
        self.methods_radio = methods_radio
        self.evaluator = Evaluator(static_file, dynamic_file)
        self.start_calculation_button = Button(
            parent,
            text='Start Calculation',
            command=self.__start_calculation
        )
        self.start_calculation_button.grid(row=7, column=5)

    def __start_calculation(self):

        values = ["price", "efficiency", "max_renewables"]

        self.evaluator.calculate_energy_services()
        self.evaluator.choose_appliances(values[self.methods_radio.active_var.get()])
        self.evaluator.calculate_end_use()
        self.evaluator.choose_conversion_technologies(values[self.methods_radio.active_var.get()])
        self.evaluator.optimize_final_energy()

        ExportExcel(evaluator=self.evaluator)


