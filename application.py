import tkinter as tk
from evaluate import Evaluator
from appliances import Appliances
from view.applicance_boxes import AppliancesBoxes
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
        self.appliances = Appliances('./examples/End_Use_Technologies_DataBase.xlsx')
        self.appliance_boxes = AppliancesBoxes(parent, self.appliances)

        self.open_file_button = OpenFileButton(parent)
        self.evaluator = Evaluator(self.static_file, self.dynamic_file)
        self.methods_radio = MethodsRadioButtons(parent, self.__sort_price(), self.__sort_efficiency())
        self.calculation_buttons = CalculationButtons(parent, self.static_file, self.dynamic_file, self.appliance_boxes,
                                                      self.appliances)

    def __sort_efficiency(self):
        self.appliances.cookers = sorted(self.appliances.cookers, key=lambda cooker: cooker['efficiency'], reverse=True)
        self.heaters_sorted = sorted(self.appliances.space_heaters,
                                     key=lambda heater: heater['efficiency'],
                                     reverse=True)
        self.water_heater_sorted = sorted(self.appliances.hot_water, key=lambda heater: heater['efficiency'],
                                          reverse=True)
        self.cooler_sorted = sorted(self.appliances.space_coolers, key=lambda cooler: cooler['efficiency_cooling'],
                                    reverse=True)
        self.appliance_boxes = AppliancesBoxes(self.parent, self.appliances)

    def __sort_price(self):
        self.cookers_sorted = sorted(self.appliances.cookers, key=lambda cooker: cooker['price'])
        self.heaters_sorted = sorted(self.appliances.space_heaters,
                                     key=lambda heater: heater['price'])
        self.water_heater_sorted = sorted(self.appliances.hot_water, key=lambda heater: heater['price'])
        self.cooler_sorted = sorted(self.appliances.space_coolers,
                                    key=lambda cooler: cooler['price'])
        self.appliance_boxes = AppliancesBoxes(self.parent, self.appliances)
