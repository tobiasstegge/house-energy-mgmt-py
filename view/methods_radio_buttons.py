from tkinter import Radiobutton, IntVar


class MethodsRadioButtons:
    def __init__(self, parent, min_cost_function, min_final_energy_function):
        self.active_var = IntVar()
        self.active_var.set(0)
        min_cost = Radiobutton(parent, text='Minimum Cost',
                               variable=self.active_var, value=0, command=min_cost_function)
        min_final_energy = Radiobutton(parent, text='Minimum Final Energy',
                                       variable=self.active_var, value=1, command=min_final_energy_function)
        max_renewables = Radiobutton(parent, text='Maximum Renewables',
                                     variable=self.active_var, value=2)

        min_cost.grid(row=5, column=14)
        min_final_energy.grid(row=6, column=14)
        max_renewables.grid(row=7, column=14)
