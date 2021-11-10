import pandas as pd


class TimeSeries:
    def __init__(self, file):
        file = './examples/Dynamic_Data.csv'
        csv_file = pd.read_csv(file, delimiter=';')

        self.data = {}
        for row in csv_file.iterrows():
            self.data[int(row[1]['Hour'])] = {
                'temp': row[1]['Temp'],
                'wind_speed': row[1]['Wind speed'],
                'radiance': row[1]['Rad (W/m^2)'],
                'occupation': row[1]['Occupation'],
                'lighting': row[1]['Lighting (lux)'],
                'total_lamps': row[1]['Total lapms'],
                'percent_area_heating': row[1]['%AreaHeatingCooling'],
                'hot_water': row[1]['Hot Water @ 40 C'],
                'cooking': row[1]['Cooking (MJ)'],
                'electrical_appliances': row[1]['Electrical Applainces (kWh)'],
            }
