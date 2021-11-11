def lux_to_lumen(lux, distance):
    return lux * (distance ** 2)


def get_power(power_kwh, efficiency, max_power_w):
    max_power_kwh = max_power_w / 1000
    if power_kwh > max_power_kwh:
        return max_power_kwh * (1 / efficiency)
    else:
        return power_kwh * (1 / efficiency)


def adapt_column_size(worksheet, df):
    for i, col in enumerate(df.columns):
        # find length of column i
        column_len = df[col].astype(str).str.len().max()
        # Setting the length if the column header is larger
        # than the max column value length
        column_len = max(column_len, len(col))
        # set the column length
        worksheet.set_column(i, i, column_len)

    return worksheet
