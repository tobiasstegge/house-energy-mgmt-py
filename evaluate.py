from house import House
from time_series import TimeSeries
from appliances import Appliances
from utils import lux_to_lumen, get_power

HEAT_CAPACITY_AIR = 0.00121 * 0.000277778  # kwH / m3*K
HEAT_CAPACITY_WATER = 4184 * 0.000277778 / 1000  # kWh⋅kg−1⋅K−1
HEAT_OCCUPANT = 0.11  # kWh


class Evaluator:
    def __init__(self, static_file, dynamic_file):
        self.house = House(static_file)
        self.time_series = TimeSeries(dynamic_file)
        self.appliances = Appliances('./examples/End_Use_Technologies_DataBase.xlsx')

        self.heating = []
        self.cooling = []
        self.hot_water = []
        self.cooking = []
        self.electrical_appliances = []
        self.lighting = []

        self.end_use_electricity_heating = 24 * [0]
        self.end_use_electricity_cooling = 24 * [0]
        self.end_use_electricity_hot_water = 24 * [0]
        self.end_use_electricity_cooking = 24 * [0]
        self.end_use_electricity_lighting = 24 * [0]
        self.end_use_electricity_appliances = 24 * [0]

        self.end_use_gas_heating = 24 * [0]
        self.end_use_gas_cooling = 24 * [0]
        self.end_use_gas_hot_water = 24 * [0]
        self.end_use_gas_cooking = 24 * [0]

    def calculate_energy_services(self):
        # heating or cooling
        for time_point in self.time_series.data.values():
            heat_loss_air = time_point['temp'] * (time_point['percent_area_heating'] / 100) * self.house.volume * \
                            HEAT_CAPACITY_AIR * self.house.air_exchange / 1000
            heat_loss_walls = self.house.wall_area * self.house.conductivity_walls * (20 - time_point['temp']) / 1000
            heat_loss_windows = self.house.window_area * self.house.conductivity_windows * (
                    20 - time_point['temp']) / 1000
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
        for time_point in self.time_series.data.values():
            self.hot_water.append(time_point['hot_water'] * HEAT_CAPACITY_WATER * self.house.temperature_water_in)

        # cooking
        for time_point in self.time_series.data.values():
            self.cooking.append(time_point['cooking'] * 3.6)  # kWh

        # electrical_appliances
        for time_point in self.time_series.data.values():
            self.electrical_appliances.append(time_point['electrical_appliances'])  # kWh

        # lighting
        for time_point in self.time_series.data.values():
            self.lighting.append(lux_to_lumen(time_point['lighting'], self.house.height))  # lumen

    def calculate_end_use(self):
        # heating
        for idx, time_point in enumerate(self.heating):
            if self.house.space_heater['final_energy'] == 'Electricity':
                if time_point > (self.house.space_heater['power'] / 1000):
                    self.end_use_electricity_heating[idx] += self.house.space_heater['power'] / 1000 * (
                            1 / self.house.space_heater['efficiency'])
                else:
                    self.end_use_electricity_heating[idx] += time_point * (1 / self.house.space_heater['efficiency'])
            if self.house.space_heater['final_energy'] == 'Gas':
                if time_point > (self.house.space_heater['power'] / 1000):
                    self.end_use_gas_heating[idx] += (self.house.space_heater['power'] / 1000) * (
                            1 / self.house.space_heater['efficiency'])
                else:
                    self.end_use_gas_heating[idx] += time_point * (1 / self.house.space_heater['efficiency'])

        # cooling
        for idx, time_point in enumerate(self.cooling):
            if time_point > (self.house.space_cooler['power_cooling'] / 1000):
                self.end_use_electricity_cooling[idx] += self.house.space_cooler['power_cooling'] / 1000 * (
                        1 / self.house.space_cooler['efficiency_cooling'])
            else:
                self.end_use_electricity_cooling[idx] += time_point * (
                        1 / self.house.space_cooler['efficiency_cooling'])

        # hot water
        for idx, time_point in enumerate(self.hot_water):
            if self.house.space_heater['final_energy'] == 'Electricity':
                self.end_use_electricity_hot_water[idx] += get_power(power_kwh=time_point,
                                                                     efficiency=self.house.hot_water_heater[
                                                                         'efficiency'], max_power_w=
                                                                     self.house.hot_water_heater['power'])
            if self.house.space_heater['final_energy'] == 'Gas':
                if self.house.space_heater['final_energy'] == 'Gas':
                    self.end_use_gas_hot_water[idx] += get_power(power_kwh=time_point,
                                                                 efficiency=self.house.hot_water_heater[
                                                                     'efficiency'], max_power_w=
                                                                 self.house.hot_water_heater['power'])

        # cooking
        for idx, time_point in enumerate(self.cooking):
            if self.house.cooker['final_energy'] == 'Electricity':
                self.end_use_electricity_cooking[idx] += get_power(power_kwh=time_point, efficiency=self.house.cooker[
                    'efficiency'], max_power_w=self.house.cooker['power'])
            if self.house.cooker['final_energy'] == 'Gas':
                if self.house.cooker['final_energy'] == 'Gas':
                    self.end_use_gas_cooking[idx] += get_power(power_kwh=time_point, efficiency=self.house.cooker[
                        'efficiency'], max_power_w=self.house.cooker['power'])

        # lighting
        for idx, time_point in enumerate(self.lighting): # lux
            n_lights = round(time_point / self.house.lights['lumen'])
            self.end_use_electricity_lighting[idx] += n_lights * (self.house.lights['power'] / 1000)

        print('EL Heating')
        print(self.end_use_electricity_heating)
        print('EL Cooling')
        print(self.end_use_electricity_cooling)
        print('EL Hot Water')
        print(self.end_use_electricity_hot_water)
        print('EL Cooking')
        print(self.end_use_electricity_cooking)
        print('EL Lights')
        print(self.end_use_electricity_lighting)

        print('\n')
        print('GAS Heating')
        print(self.end_use_gas_heating)
        print('GAS Cooling')
        print(self.end_use_gas_cooling)
        print('GAS Hot Water')
        print(self.end_use_gas_hot_water)
        print('GAS Cooking')
        print(self.end_use_gas_cooking)


def final_energy_conversion(self):
    pass
