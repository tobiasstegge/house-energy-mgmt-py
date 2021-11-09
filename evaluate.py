from house import House
from time_series import TimeSeries
from appliances import Appliances

HEAT_CAPACITY_AIR = 0.00121 * 0.000277778 # kwH / m3*K
HEAT_CAPACITY_WATER = 4184 * 0.000277778 / 1000 # kWh⋅kg−1⋅K−1
HEAT_OCCUPANT = 0.11 # kWh


class Evaluator:
    def __init__(self, static_file, dynamic_file):
        conversion_file_path = './examples/Conversion_Technologies_Database.xlsx'

        self.house = House(static_file)
        self.dynamic_data = TimeSeries(dynamic_file)
        self.appliances = Appliances('./examples/End_Use_Technologies_DataBase.xlsx')

        self.heating = []
        self.cooling = []
        self.hot_water = []
        self.cooking = []
        self.electrical_appliances = []
        self.lighting = []

    def calculate_energy_services(self):
        for time_point in self.dynamic_data.data.values():
            heat_loss_air = time_point['temp'] * (time_point['percent_area_heating'] / 100) * self.house.volume * \
                            HEAT_CAPACITY_AIR * self.house.air_exchange / 1000
            heat_loss_walls = self.house.wall_area * self.house.conductivity_walls * (20 - time_point['temp']) / 1000
            heat_loss_windows = self.house.window_area * self.house.conductivity_windows * (20 - time_point['temp']) / 1000
            solar_gain = self.house.window_solar_gain * self.house.window_area * time_point['radiance'] / 1000
            heat_occupants = time_point['occupation'] * HEAT_OCCUPANT
            total_heating = heat_loss_air + heat_loss_walls + heat_loss_windows - solar_gain - heat_occupants

            if total_heating > 0:
                self.heating.append(total_heating)
            else:
                self.heating.append(0)

            if total_heating <= 0:
                self.cooling.append(abs(total_heating))
            else:
                self.cooling.append(0)

        # hot water
        for time_point in self.dynamic_data.data.values():
            self.hot_water.append(time_point['hot_water'] * HEAT_CAPACITY_WATER * self.house.temperature_water_in)

        # cooking
        for time_point in self.dynamic_data.data.values():
            self.cooking.append(time_point['cooking'] * 3.6)

        # electrical_appliances
        for time_point in self.dynamic_data.data.values():
            self.electrical_appliances.append(time_point['electrical_appliances'])

        # lighting
        for time_point in self.dynamic_data.data.values():
            self.lighting.append(time_point['lighting'])

    def calculate_end_use(self):

        pass

    def final_energy_conversion(self):
        pass
