import pandas as pd
from utils import adapt_column_size


class ExportExcel:
    def __init__(self, evaluator, path):
        with pd.ExcelWriter(path + "/DataExportTool.xlsx", engine='xlsxwriter') as writer:
            # Selected Appliances
            df_appliances = pd.DataFrame(columns=['Type', 'Name'])
            rows = [{'Type': "Space Heater",
                     'Name': evaluator.house.space_heater['name'],
                     'Power': evaluator.house.space_heater['power']},
                    {'Type': "Space Cooler", 'Name': evaluator.house.space_cooler['name'],
                     'Power': evaluator.house.space_cooler['power_cooling']},
                    {'Type': "Cooker", 'Name': evaluator.house.cooker['name'],
                     'Power': evaluator.house.cooker['power']},
                    {'Type': "Hot Water Heater", 'Name': evaluator.house.hot_water_heater['name'],
                     'Power': evaluator.house.hot_water_heater['power']},
                    {'Type': "Light", 'Name': evaluator.house.light['name'],
                     'Power': evaluator.house.light['lumen']},
                    ]
            df_appliances = df_appliances.append(rows, ignore_index=True)

            df_appliances.to_excel(writer, sheet_name='Selected Appliances', index=False)
            adapt_column_size(writer.sheets['Selected Appliances'], df_appliances)

            # Energy Use Services
            df_services = pd.DataFrame()
            df_services['Service Heating'] = evaluator.heating
            df_services['Service Cooling'] = evaluator.cooling
            df_services['Service Hot Water'] = evaluator.hot_water
            df_services['Service Cooking'] = evaluator.cooking
            df_services['Service Electrical Appliances'] = evaluator.electrical_appliances
            df_services['Service Lighting'] = evaluator.lighting
            df_services.to_excel(writer, sheet_name='Energy Services', index=False)
            adapt_column_size(writer.sheets['Energy Services'], df_services)

            # Electricty
            df_electricity = pd.DataFrame()
            df_electricity['End Use Heating'] = evaluator.end_use_electricity_heating
            df_electricity['End Use Cooling'] = evaluator.end_use_electricity_cooling
            df_electricity['End Use Hot Water'] = evaluator.end_use_electricity_hot_water
            df_electricity['End Use Cooking'] = evaluator.end_use_electricity_cooking
            df_electricity['End Use Appliances'] = evaluator.end_use_electricity_appliances
            df_electricity['End Use Lighting'] = evaluator.end_use_electricity_lighting
            df_electricity['End Use Total Electricity'] = evaluator.end_use_total_electricity

            df_electricity.to_excel(writer, sheet_name='End Use Electricity', index=False)
            adapt_column_size(writer.sheets['End Use Electricity'], df_electricity)

            # Gas
            df_gas = pd.DataFrame()
            df_gas['End Use Heating'] = evaluator.end_use_gas_heating
            df_gas['End Use Cooling'] = evaluator.end_use_gas_cooling
            df_gas['End Use Hot Water'] = evaluator.end_use_gas_hot_water
            df_gas['End Use Cooking'] = evaluator.end_use_gas_cooking
            df_gas['End Use Total Gas'] = evaluator.end_use_total_gas
            df_gas.to_excel(writer, sheet_name='End Use Gas', index=False)
            adapt_column_size(writer.sheets['End Use Gas'], df_gas)

            # energy conversion
            df_conversion = pd.DataFrame()
            df_conversion['Electricity from Solar (kWh)'] = evaluator.electricity_from_solar
            df_conversion['Electricity from Storage (kWh)'] = evaluator.electricity_from_storage
            df_conversion['Electricity to Storage (kWh)'] = evaluator.electricity_to_storage
            df_conversion['Electricity from Grid (kWh)'] = evaluator.electricity_from_grid
            df_conversion['Electricity to Grid (kWh)'] = evaluator.electricity_to_grid
            df_conversion['State of Charge Battery (kWh)'] = evaluator.soc_battery

            df_conversion.to_excel(writer, sheet_name='Energy Conversion', index=False)
            adapt_column_size(writer.sheets['Energy Conversion'], df_conversion)

            # Energy Totals
            df_energy_totals = pd.DataFrame(columns=['Type', 'Energy (kWh / day)'])
            rows = [{'Type': "Daily Hating Needs",
                     'Energy (kWh / day)': evaluator.heating_needs},
                    {'Type': "Daily Cooling Needs",
                     'Energy (kWh / day)': evaluator.cooling_needs},
                    {'Type': "Daily Hot Water Needs",
                     'Energy (kWh / day)': evaluator.hot_water_needs},
                    {'Type': "Daily Cooking Needs",
                     'Energy (kWh / day)': evaluator.cooking_needs},
                    {'Type': "Daily Lighting Needs",
                     'Energy (kWh / day)': evaluator.lighting_needs},
                    {'Type': "Daily Total Final Energy Electricity",
                     'Energy (kWh / day)': evaluator.total_final_energy_electricity},
                    {'Type': "Daily Total Final Energy Gas",
                     'Energy (kWh / day)': evaluator.total_final_energy_gas},
                    {'Type': "Daily Total Final Energy Biomass",
                     'Energy (kWh / day)': evaluator.total_final_energy_biomass},
                    {'Type': "Daily Total Primary Energy",
                     'Energy (kWh / day)': evaluator.total_primary_energy},
                    ]
            df_energy_totals = df_energy_totals.append(rows, ignore_index=True)
            df_energy_totals.to_excel(writer, sheet_name='Energy Totals', index=False)
            adapt_column_size(writer.sheets['Energy Totals'], df_energy_totals)

            # More Indicators

            df_more_indicators = pd.DataFrame(columns=['Type', 'Value'])
            rows = [{'Type': "Total Cost (€)",
                     'Value': evaluator.total_cost},
                    {'Type': "Self Sustainability (%)",
                     'Value': evaluator.self_sustainability},
                    {'Type': "Renewable Penetration (%)",
                     'Value': evaluator.renewable_penetration},
                    {'Type': "Local Electricity Generation",
                     'Value': evaluator.local_electricity_generation},
                    {'Type': "Electricity bought from Grid (kWh/day)",
                     'Value': evaluator.electricity_bought_from_grid},
                    {'Type': "Electricity sold to grid (kWh/day)",
                     'Value': evaluator.electricity_sold_to_grid},
                    {'Type': "Emissions (gCO2)",
                     'Value': evaluator.emissions},
                    ]
            df_more_indicators = df_more_indicators.append(rows, ignore_index=True)
            df_more_indicators.to_excel(writer, sheet_name='Extra Indicators', index=False)
            adapt_column_size(writer.sheets['Extra Indicators'], df_more_indicators)

