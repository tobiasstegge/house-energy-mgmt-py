def lux_to_lumen(lux, distance):
    return lux * (distance ** 2)


def get_power(power_kwh, efficiency, max_power_w):
    max_power_kwh = max_power_w / 1000
    if power_kwh > max_power_kwh:
        return max_power_kwh * (1 / efficiency)
    else:
        return power_kwh * (1 / efficiency)
