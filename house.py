import pandas as pd


class House:
    def __init__(self, file):
        file = './examples/Static_Data.csv'
        self.data = pd.read_csv(file, delimiter=';')

        self.length = float(self.data['Length(m)'].values[0])
        self.depth = float(self.data['Depth(m)'].values[0])
        self.height = float(self.data['Height(m)'].values[0])
        self.conductivity_walls = self.data['Uwalls(W/m2K)'].values[0]
        self.conductivity_windows = self.data['Uwindows(W/m2K)'].values[0]
        self.fraction_window = self.data['Awindow/Awall'].values[0]
        self.air_exchange = self.data['Air Changes/hour (h^-1)'].values[0]
        self.temperature_inside = self.data['Tinside(ºC)'].values[0]
        self.temperature_water_in = self.data['Twaterin(ºC)'].values[0]
        self.heat_transfer_people = self.data['Qpeople(W)'].values[0]
        self.window_solar_gain = self.data['Window Solar Gain'].values[0]
        self.percentage_renenwables_grid = self.data['Renewables_grid(%)'].values[0]
        self.primary_final_factor = self.data['Primary_Final_Factor'].values[0]
        self.emissions_grid = self.data['Emissions_grid(kgCO2/kWH)'].values[0]
        self.emissions_gas = self.data['Emissions_Gas(kgCO2/KWh)'].values[0]

        # calculated values
        self.floor_area = self.length * self.depth
        self.window_area = self.depth * self.height * 4 * self.fraction_window
        self.wall_area = self.depth * self.height * 4 * (1 - self.fraction_window)
        self.volume = self.length * self.depth * self.height
        self.heat_loss = self.window_area * self.conductivity_windows + self.wall_area * self.wall_area

        # picked from appliances
        self.space_heater = {}
        self.space_cooler = {}
        self.hot_water_heater = {}
        self.cooker = {}
        self.lights = []