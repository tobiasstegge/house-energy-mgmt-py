import pandas as pd


class House:
    def __init__(self, file):
        self.data = pd.read_csv(file, delimiter=";", encoding="cp1252")

        self.length = float(self.data['Length(m)'].values[0])
        self.depth = float(self.data['Depth(m)'].values[0])
        self.height = float(self.data['Height(m)'].values[0])
        self.conductivity_walls = self.data['Uwalls(W/m2K)'].values[0]
        self.conductivity_windows = self.data['Uwindows(W/m2K)'].values[0]
        self.air_exchange = self.data['Air Changes/hour (h^-1)'].values[0]
        self.temperature = self.data['Tinside(ºC)'].values[0]
        self.heat_transfer_people = self.data['Qpeople(W)'].values[0]
        self.window_solar_gain = self.data['Window Solar Gain'].values[0]
        self.height_lights = self.data['Height Lights (m)'].values[0]

        self.volume = self.length * self.depth * self.height
