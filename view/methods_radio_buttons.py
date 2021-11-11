from tkinter import Radiobutton, IntVar


class MethodsRadioButtons:
    def __init__(self, parent, function):
        self.active_var = IntVar()
        min_cost = Radiobutton(parent, text='Minimum Cost',
                               variable=self.active_var, value=1, command=function)
        min_final_energy = Radiobutton(parent, text='Minimum Final Energy',
                                       variable=self.active_var, value=2, command=function)
        max_renewables = Radiobutton(parent, text='Maximum Renewables',
                                     variable=self.active_var, value=3, command=function)

        min_cost.grid(sticky="S")
        min_final_energy.grid(sticky="S")
        max_renewables.grid(sticky="S")
