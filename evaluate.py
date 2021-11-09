from house import House
from time_series import TimeSeries
from appliances import Appliances

HEAT_CAPACITY_AIR = 0.00121 * 0.000277778 # kwH / m3*K
HEAT_CAPACITY_WATER = 4184 * 0.000277778 / 1000 # kWh⋅kg−1⋅K−1
HEAT_OCCUPANT = 0.11 # kWh


class Evaluator:
    def __init__(self, static_file, dynamic_file):
        conversion_file_path = './examples/Conversion_Technologies_Database.xlsx'
        storage_file_path = './examples/StorageTechnologies_Database.xlsx'
        end_use_file_path = './examples/End-Use_Technologies_DataBase..xlsx'

        self.house = House(static_file)
        self.dynamic_data = TimeSeries(dynamic_file)
        self.appliances = Appliances(conversion_file_path, storage_file_path, end_use_file_path)

        self.heating_demand = []
        self.cooling_demand = []
        self.hot_water_demand = []
        self.electrical_appliances = []

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
                self.heating_demand.append(total_heating)
            else:
                self.heating_demand.append(0)

            if total_heating <= 0:
                self.cooling_demand.append(abs(total_heating))
            else:
                self.cooling_demand.append(0)

        # hot water
        for time_point in self.dynamic_data.data.values():
            self.hot_water_demand.append(time_point['hot_water'] * HEAT_CAPACITY_WATER * self.house.temperature_water_in)

        # electricity
        for time_point in self.dynamic_data.data.values():
            self.electrical_appliances.append(time_point['cooking'] * 3.6 + time_point['electrical_appliances'])

        # lighting

    def calculate_end_use(self):
        pass

    def final_energy_conversion(self):
        pass
