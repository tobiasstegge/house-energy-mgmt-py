import math

from house import House
from time_series import TimeSeries
from appliances import Appliances
from utils import lux_to_lumen, get_power
import numpy as np

HEAT_CAPACITY_AIR = 0.00121 * 0.000277778  # kwH / m3*K
HEAT_CAPACITY_WATER = 4184 * 0.000277778 / 1000  # kWh⋅kg−1⋅K−1
HEAT_OCCUPANT = 0.11  # kWh
FACTOR_REFLECTION_GLASS = 0.87
TEMP_HOT_WATER = 40

GRID_COST_ELECTRICITY_KWH = 0.25  # €
GRID_COST_GAS_KWH = 0.0622  # €


class Evaluator:
    def __init__(self, static_file, dynamic_file):
        self.house = House(static_file)
        self.time_series = TimeSeries(dynamic_file)
        self.appliances = Appliances()

        self.heating = []
        self.cooling = []
        self.hot_water = []
        self.cooking = []
        self.electrical_appliances = []
        self.lighting = []
        self.radiance = []

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

        self.end_use_total_electricity = 24 * [0]
        self.end_use_total_gas = 24 * [0]
        self.electricity_from_solar = 24 * [0]
        self.electricity_from_grid = 24 * [0]
        self.electricity_to_grid = 24 * [0]
        self.electricity_to_storage = 24 * [0]
        self.electricity_from_storage = 24 * [0]

        self.soc_battery = 24 * [0]

        # key indicators
        self.heating_needs = None
        self.cooling_needs = None
        self.hot_water_needs = None
        self.cooking_needs = None
        self.lighting_needs = None
        self.total_final_energy_electricity = None
        self.total_final_energy_gas = None
        self.total_final_energy_biomass = None
        self.total_primary_energy = None
        self.total_cost = None
        self.self_sustainability = None
        self.renewable_penetration = None
        self.local_electricity_generation = None
        self.electricity_bought_from_grid = None
        self.electricity_sold_to_grid = None
        self.emissions = None

    def calculate_energy_services(self):
        # heating or cooling
        for time_point in self.time_series.data.values():
            heat_loss_air = time_point['temp'] * (time_point['percent_area_heating'] / 100) * self.house.volume * \
                            HEAT_CAPACITY_AIR * self.house.air_exchange
            heat_loss_walls = self.house.wall_area * self.house.conductivity_walls * (
                    self.house.temperature_inside - time_point['temp']) / 1000
            heat_loss_windows = self.house.window_area * self.house.conductivity_windows * (
                    self.house.temperature_inside - time_point['temp']) / 1000
            solar_gain = self.house.window_area * time_point['radiance'] * FACTOR_REFLECTION_GLASS / 1000 * math.cos(45)
            heat_occupants = time_point['occupation'] * HEAT_OCCUPANT
            total_heat_loss = heat_loss_air + heat_loss_walls + heat_loss_windows - solar_gain - heat_occupants

            if total_heat_loss > 0:
                self.heating.append(total_heat_loss)
            else:
                self.heating.append(0)
            if total_heat_loss < 0:
                self.cooling.append(abs(total_heat_loss))
            else:
                self.cooling.append(0)

        # hot water
        for time_point in self.time_series.data.values():
            self.hot_water.append(
                time_point['hot_water'] * HEAT_CAPACITY_WATER * (TEMP_HOT_WATER - self.house.temperature_water_in))

        # cooking
        for time_point in self.time_series.data.values():
            self.cooking.append(time_point['cooking'] * 0.27778)  # MJ tp kWh

        # electrical_appliances
        for time_point in self.time_series.data.values():
            self.electrical_appliances.append(time_point['electrical_appliances'])  # kWh

        # lighting
        for time_point in self.time_series.data.values():
            self.lighting.append(lux_to_lumen(time_point['lighting'], self.house.height))  # lumen

        # solar radiance
        self.radiance = [time_point['radiance'] for time_point in
                         self.time_series.data.values()]

    def choose_appliances(self, method):
        # heater
        possible_heaters = []
        for heater in self.appliances.space_heaters:
            if max(self.heating) * 1000 < heater['power']:
                possible_heaters.append(heater)
        if method == 'price':
            self.house.space_heater = min(possible_heaters, key=lambda key: key['price'])
        if method == 'efficiency':
            self.house.space_heater = max(possible_heaters, key=lambda key: key['efficiency'])
        if method == 'max_renewables':
            possible_heaters = [heater for heater in possible_heaters if heater['final_energy'] == 'Electricity']
            self.house.space_heater = max(possible_heaters, key=lambda key: key['efficiency'])

        # cooler
        possible_coolers = []
        for cooler in self.appliances.space_coolers:
            if max(self.cooling) * 1000 < cooler['power_cooling']:
                possible_coolers.append(cooler)
        if method == 'price':
            self.house.space_cooler = min(possible_coolers, key=lambda key: key['price'])
        if method == 'efficiency':
            self.house.space_cooler = max(possible_coolers, key=lambda key: key['efficiency_cooling'])
        if method == 'max_renewables':
            self.house.space_cooler = max(possible_coolers, key=lambda key: key['efficiency_cooling'])

        # cooker
        possible_cookers = []
        for cooker in self.appliances.cookers:
            if max(self.cooking) * 1000 < cooker['power']:
                possible_cookers.append(cooker)
        if method == 'price':
            self.house.cooker = min(possible_cookers, key=lambda key: key['price'])
        if method == 'efficiency':
            self.house.cooker = max(possible_cookers, key=lambda key: key['efficiency'])
        if method == 'max_renewables':
            possible_cookers = [cooker for cooker in possible_cookers if cooker['final_energy'] == "Electricity"]
            self.house.cooker = max(possible_cookers, key=lambda key: key['efficiency'])

        # hot water
        possible_water_heaters = []
        for heater in self.appliances.hot_water:
            if max(self.hot_water) * 1000 < heater['power']:
                possible_water_heaters.append(heater)
        if method == 'price':
            self.house.hot_water_heater = min(possible_water_heaters, key=lambda key: key['price'])
        if method == 'efficiency':
            self.house.hot_water_heater = max(possible_water_heaters, key=lambda key: key['efficiency'])
        if method == 'max_renewables':
            self.house.hot_water_heater = max(possible_water_heaters, key=lambda key: key['efficiency'])

        # lighting
        if method == 'price':
            self.house.light = min(self.appliances.lighting, key=lambda key: (key['price'] / key['lumen']))
        if method == 'efficiency':
            self.house.light = max(self.appliances.lighting, key=lambda key: (key['power'] / key['lumen']))
        if method == 'max_renewables':
            self.house.light = max(self.appliances.lighting, key=lambda key: (key['power'] / key['lumen']))

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
        for idx, time_point in enumerate(self.lighting):  # lux
            n_lights = round(time_point / self.house.light['lumen'])
            self.end_use_electricity_lighting[idx] += n_lights * (self.house.light['power'] / 1000)

        # appliances
        for idx, time_point in enumerate(self.electrical_appliances):
            self.end_use_electricity_appliances[idx] += time_point

        self.end_use_total_electricity = np.sum([self.end_use_electricity_heating, self.end_use_electricity_cooling,
                                                 self.end_use_gas_hot_water, self.end_use_electricity_cooking,
                                                 self.end_use_electricity_lighting,
                                                 self.electrical_appliances], axis=0)

        self.end_use_total_gas = np.sum([self.end_use_gas_heating, self.end_use_gas_cooling,
                                         self.end_use_gas_cooking, self.end_use_gas_hot_water], axis=0)

    def choose_conversion_technologies(self, method):
        # pv panel
        for panel in self.appliances.pv_panels:
            amount_needed = math.ceil(max(self.end_use_total_electricity) / (panel['power'] / 1000))
            amount_possible = self.house.floor_area / panel['area']
            if amount_needed > amount_possible:
                amount = amount_possible
            else:
                amount = amount_needed
            if method == 'price':
                self.house.pv_panel = {'panel': max(self.appliances.pv_panels, key=lambda key: (key['price'] * amount)),
                                       'amount': amount}
            if method == 'efficiency':
                self.house.pv_panel = {
                    'panel': max(self.appliances.pv_panels, key=lambda key: (key['efficiency'] * amount)),
                    'amount': amount}
            if method == 'max_renewables':
                self.house.pv_panel = {
                    'panel': max(self.appliances.pv_panels, key=lambda key: (key['efficiency'] * amount)),
                    'amount': amount}

        # storage
        for battery in self.appliances.batteries:
            amount_for_power = math.ceil(
                max(self.end_use_total_electricity) / battery['max_current'] * battery['voltage'])
            amount_for_capacity = math.ceil(
                (sum(self.end_use_total_electricity) - self.house.pv_panel['panel']['efficiency'] * self.house.pv_panel[
                    'amount'] * np.sum(self.radiance)) / (battery['ampere'] * battery['voltage']))
            amount = max([amount_for_power, amount_for_capacity])
            if method == 'price':
                self.house.battery = {
                    'battery': max(self.appliances.batteries, key=lambda key: (key['price'] * amount)),
                    'amount': amount}
            if method == 'efficiency':
                self.house.battery = {
                    'battery': max(self.appliances.batteries, key=lambda key: (key['efficiency'] * amount)),
                    'amount': amount}
            if method == 'max_renewables':
                self.house.battery = {
                    'battery': max(self.appliances.batteries, key=lambda key: (key['efficiency'] * amount)),
                    'amount': amount}

    def optimize_final_energy(self):
        for idx, time_point in enumerate(self.radiance):
            self.electricity_from_solar[idx] = (
                    time_point * self.house.pv_panel['panel']['area'] * self.house.pv_panel['amount'] *
                    self.house.pv_panel['panel']['efficiency'] / 1000)

        max_capacity_battery = self.house.battery['battery']['ampere'] * self.house.battery['battery']['voltage'] * \
                               self.house.battery['amount'] / 1000

        for idx, value in enumerate(self.end_use_total_electricity):
            demand = self.end_use_total_electricity[idx] - self.electricity_from_solar[idx]
            # charge battery
            if demand < 0:
                if self.soc_battery[idx] + abs(demand) > max_capacity_battery:
                    self.soc_battery[idx] = max_capacity_battery
                    self.electricity_to_grid[idx] = self.soc_battery[idx] + abs(demand) - max_capacity_battery
                    self.electricity_to_storage[idx] = demand - self.electricity_to_grid[idx]
                    demand = 0
                else:
                    self.electricity_to_storage[idx] = abs(demand)
                    self.soc_battery[idx] = self.soc_battery[idx - 1] + abs(demand)
                    demand = 0
            # discharge battery
            if demand > 0:
                if self.soc_battery[idx - 1] > 0:
                    if demand > self.soc_battery[idx - 1]:
                        self.electricity_from_storage[idx] = self.soc_battery[idx - 1]
                        self.electricity_from_grid[idx] = abs(demand - self.soc_battery[idx - 1])
                        self.soc_battery[idx] = 0
                    else:
                        self.soc_battery[idx] = self.soc_battery[idx - 1] - demand
                        self.electricity_from_storage[idx] = demand
                        self.electricity_from_grid[idx] = 0
                # otherwise get from grid
                else:
                    self.electricity_from_grid[idx] = demand

        self.heating_needs = sum(self.heating)
        self.cooling_needs = sum(self.cooling)
        self.hot_water_needs = sum(self.hot_water)
        self.cooking_needs = sum(self.cooking)
        self.lighting_needs = sum(self.lighting)
        self.total_final_energy_electricity = sum(self.end_use_total_electricity)
        self.total_final_energy_gas = sum(self.end_use_total_gas)
        self.total_final_energy_biomass = 0

        renewables_from_grid = self.house.percentage_renewables_grid * sum(self.electricity_from_grid)
        non_renewables_from_grid = (1 - self.house.percentage_renewables_grid) * sum(self.electricity_from_grid)
        total_eletricity_from_solar = sum(self.electricity_from_solar)
        self.total_primary_energy = renewables_from_grid + non_renewables_from_grid * self.house.primary_final_factor + total_eletricity_from_solar

        self.total_cost = GRID_COST_ELECTRICITY_KWH * sum(
            self.electricity_from_grid) + GRID_COST_GAS_KWH * self.total_final_energy_gas
        self.self_sustainability = (sum(self.electricity_from_solar) / (
                self.total_final_energy_electricity + self.total_final_energy_gas)) * 100
        self.renewable_penetration = ((sum(self.electricity_from_solar) + renewables_from_grid) / (
            self.total_primary_energy)) * 100
        self.local_electricity_generation = sum(self.electricity_from_solar)
        self.electricity_bought_from_grid = sum(self.electricity_from_grid)
        self.electricity_sold_to_grid = sum(self.electricity_to_grid)
        self.emissions = self.total_final_energy_gas * self.house.emissions_gas + \
                         self.electricity_bought_from_grid * self.house.emissions_grid


