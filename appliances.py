import pandas as pd


class Appliances:
    def __init__(self):
        xlsx_end_use_file = pd.ExcelFile("./examples/End_Use_Technologies_DataBase.xlsx")
        xlsx_conversion_file = pd.ExcelFile("./examples/Conversion_Technologies_Database.xlsx")
        xlsx_storage_file = pd.ExcelFile("./examples/StorageTechnologies_Database.xlsx")

        # heaters
        self.space_heaters = []
        for row in xlsx_end_use_file.parse('SpaceHeating').iterrows():
            if row[1]['Final Energy'] == 'Electricity' or 'Gas':
                self.space_heaters.append({
                    'name': row[1]['Name'],
                    'final_energy': row[1]['Final Energy'],
                    'power': row[1]['Thermal PowerHeating (W)'],
                    'efficiency': row[1]['Efficiency Heating'],
                    'price': row[1]['Price']
                })
        for row in xlsx_end_use_file.parse('SpaceHeatingWater').iterrows():
            if row[1]['Final Energy'] == 'Electricity' or 'Gas':
                self.space_heaters.append({
                    'name': row[1]['Name'],
                    'final_energy': row[1]['Final Energy'],
                    'power': row[1]['Thermal PowerHeating (W)'],
                    'efficiency': row[1]['Efficiency'],
                    'price': row[1]['Price (€)']
                })

        # coolers
        self.space_coolers = []
        for row in xlsx_end_use_file.parse('SpaceHeatingCooling').iterrows():
            self.space_coolers.append({
                'name': row[1]['Name'],
                'final_energy': row[1]['Final Energy'],
                'power_heating': row[1]['Thermal PowerHeating (W)'],
                'power_cooling': row[1]['Thermal PowerCooling (W)'],
                'efficiency_heating': row[1]['Efficiency Heating'],
                'efficiency_cooling': row[1]['Efficiency Cooling'],
                'price': row[1]['Price (€)']
            })

        # hot water
        self.hot_water = []
        for row in xlsx_end_use_file.parse('HotWater').iterrows():
            self.hot_water.append({
                'name': row[1]['Name'],
                'final_energy': row[1]['Final Energy'],
                'power': row[1]['Power (W)'],
                'flow': row[1]['Flow (L/m)'],
                'tank_size': row[1]['Tank size (L)'],
                'efficiency': row[1]['Efficiency'],
                'price': row[1]['Price (€)']
            })

        self.cookers = []
        for row in xlsx_end_use_file.parse('Cooking').iterrows():
            self.cookers.append({
                'name': row[1]['Name'],
                'final_energy': row[1]['Final Energy'],
                'power': row[1]['Power (W)'],
                'efficiency': row[1]['Efficiency'],
                'price': row[1]['Price (€)']
            })

        self.lighting = []
        for row in xlsx_end_use_file.parse('Lighting').iterrows():
            self.lighting.append({
                'name': row[1]['Name'],
                'final_energy': row[1]['Final Energy'],
                'power': row[1]['Power (W)'],
                'lumen': row[1]['Lumens (lm)'],
                'hours': row[1]['Hours'],
                'price': row[1]['Price (€)']})

        self.pv_panels = []
        for row in xlsx_conversion_file.parse('Solar PV').iterrows():
            self.pv_panels.append({
                'name': row[1]['Name'],
                'power': row[1]['Power (W)'],
                'area': row[1]['Area (m2)'],
                'efficiency': row[1]['Efficiency'],
                'price': row[1]['Price (€)']})

        self.batteries = []
        for row in xlsx_storage_file.parse('Batteries').iterrows():
            self.batteries.append({
                'name': row[1]['Name'],
                'voltage': row[1]['Voltage (V)'],
                'ampere': row[1]['Storage (Ah)'],
                'efficiency': row[1]['Efficiency (Charging/discharging)'],
                'max_current': row[1]['Charging/Discharging current (A)'],
                'price': row[1]['Price (€)']})
