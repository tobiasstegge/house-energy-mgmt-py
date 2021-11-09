import pandas as pd


class Appliances:
    def __init__(self, end_use_file_path):
        xlsx_end_use_file = pd.ExcelFile(end_use_file_path)

        self.space_heaters_electric = {}
        for row in xlsx_end_use_file.parse('SpaceHeating').iterrows():
            if row[1]['Final Energy'] == 'Electricity':
                self.space_heaters_electric[row[1]['Name']] = {
                    'final_energy': row[1]['Final Energy'],
                    'power': row[1]['Thermal PowerHeating (W)'],
                    'efficiency': row[1]['Efficiency Heating'],
                    'price': row[1]['Price']
                }

        self.space_heaters_water = {}
        for row in xlsx_end_use_file.parse('SpaceHeatingWater').iterrows():
            if row[1]['Final Energy'] == 'Gas':
                self.space_heaters_water[row[1]['Name']] = {
                    'final_energy': row[1]['Final Energy'],
                    'power': row[1]['Thermal PowerHeating (W)'],
                    'efficiency': row[1]['Efficiency'],
                    'price': row[1]['Price (€)']
                }

        self.space_coolers = {}
        for row in xlsx_end_use_file.parse('SpaceHeatingCooling').iterrows():
            if row[1]['Final Energy'] == 'Electricity':
                self.space_coolers[row[1]['Name']] = {
                    'final_energy': row[1]['Final Energy'],
                    'power_heating': row[1]['Thermal PowerHeating (W)'],
                    'power_cooling': row[1]['Thermal PowerCooling (W)'],
                    'efficiency_heating': row[1]['Efficiency Heating'],
                    'efficiency_cooling': row[1]['Efficiency Cooling'],
                    'price': row[1]['Price (€)']
                }

        self.hot_water = {}
        for row in xlsx_end_use_file.parse('HotWater').iterrows():
            self.hot_water[row[1]['Name']] = {
                'final_energy': row[1]['Final Energy'],
                'power': row[1]['Power (W)'],
                'flow': row[1]['Flow (L/m)'],
                'tank_size': row[1]['Tank size (L)'],
                'efficiency': row[1]['Efficiency'],
                'price': row[1]['Price (€)']
            }

        self.cookers = {}
        for row in xlsx_end_use_file.parse('Cooking').iterrows():
            self.cookers[row[1]['Name']] = {
                'final_energy': row[1]['Final Energy'],
                'power': row[1]['Power (W)'],
                'efficiency': row[1]['Efficiency'],
                'price': row[1]['Price (€)']
            }

        self.lighting = {}
        for row in xlsx_end_use_file.parse('Lighting').iterrows():
            self.append = self.lighting[row[1]['Name']] = {
                'final_energy': row[1]['Final Energy'],
                'power': row[1]['Power (W)'],
                'lumen': row[1]['Lumens (lm)'],
                'hours': row[1]['Hours'],
                'price': row[1]['Price (€)']}
