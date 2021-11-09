import pandas as pd


class Appliances:
    def __init__(self, conversion_file_path, storage_file_path, end_use_file_path):
        xlsx_conversion_file_path = pd.read_excel(conversion_file_path)
        xlsx_storage_file_path = pd.read_excel(storage_file_path)
        xlsx_end_use_file_path = pd.read_excel(end_use_file_path)


