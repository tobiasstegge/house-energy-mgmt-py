from house import House
from time_series import TimeSeries


class Evaluator:
    def __init__(self, static_file, dynamic_file):
        self.house = House(static_file)
        self.dynamic_data = TimeSeries(dynamic_file)

    def calculate_demand(self):
        pass

    def calculate_end_use(self):
        pass

    def final_energy_conversion(self):
        pass

