import tkinter as tk
from appliances import Appliances
from view.open_file_buttons import OpenFileButton
from view.calculation_buttons import CalculationButtons
from view.methods_radio_buttons import MethodsRadioButtons


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.geometry('290x350')

        self.radio_checked = False

        self.static_file = None
        self.dynamic_file = None

        self.appliances = Appliances()
        self.label_info = tk.Label(parent,
                                   text="Hello Dear Tester! :-) \n Pick the Input files and an output directory!")
        self.label_info.grid(sticky="S")
        self.open_file_button = OpenFileButton(parent)
        self.methods_radio = MethodsRadioButtons(parent, function=self.__radio_checked)

    def __radio_checked(self):
        if not self.radio_checked and \
                self.open_file_button.dynamic_file is not None and \
                self.open_file_button.dynamic_file is not None and \
                self.open_file_button.file_path_output is not None:
            self.calculation_buttons = CalculationButtons(self.parent, self.open_file_button.static_file,
                                                          self.open_file_button.dynamic_file,
                                                          self.appliances, self.methods_radio,
                                                          self.open_file_button.file_path_output)
            self.radio_checked = True

