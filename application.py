import tkinter as tk
from evaluate import Evaluator
from appliances import Appliances
from view.applicance_labels import AppliancesLabels
from view.open_file_buttons import OpenFileButton
from view.calculation_buttons import CalculationButtons
from view.methods_radio_buttons import MethodsRadioButtons


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.title = "Test"
        parent.geometry('400x400')

        self.static_file = None
        self.dynamic_file = None

        # components
        self.appliances = Appliances()

        self.open_file_button = OpenFileButton(parent)
        self.evaluator = Evaluator(self.static_file, self.dynamic_file)
        self.methods_radio = MethodsRadioButtons(parent, self.__optimize_price(), self.__optimize_efficiency())
        self.calculation_buttons = CalculationButtons(parent, self.static_file, self.dynamic_file,
                                                      self.appliances, self.methods_radio)
        self.appliance_labels = AppliancesLabels(parent, self.calculation_buttons.evaluator.house)

    def __optimize_efficiency(self):
        pass

    def __optimize_price(self):
        pass
