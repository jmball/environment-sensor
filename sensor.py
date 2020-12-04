#!/usr/bin/env python

import csv
import pathlib
import time

import bme680
import pms5003


SAVE_FILE = pathlib.Path("data.tsv")
HEADER = [
    "timestamp (s)",
    "temperature (C)",
    "pressure (hPa)",
    "rel. humidity (%RH)",
    "gas resistance (counts)",
    "PM > 0.3um (/0.1L air)",
    "PM > 0.5um (/0.1L air)",
    "PM > 1.0um (/0.1L air)",
    "PM > 2.5um (/0.1L air)",
    "PM > 5.0um (/0.1L air)",
    "PM > 10um (/0.1L air)",
]

# configure the PMS5003 particulate sensor
pms = pms5003.PMS5003(
    device='/dev/ttyAMA0',
    baudrate=9600,
    pin_enable=22,
    pin_reset=27
)
pms.setup()

# configure the bme680 temp/humidity/pressure sensor
bme = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

bme.set_humidity_oversample(bme680.OS_2X)
bme.set_pressure_oversample(bme680.OS_4X)
bme.set_temperature_oversample(bme680.OS_8X)
bme.set_temp_offset(-4) # this is a guess at what the offset should be
bme.set_filter(bme680.FILTER_SIZE_3)
bme.set_gas_status(bme680.ENABLE_GAS_MEAS)
bme.set_gas_heater_temperature(320)
bme.set_gas_heater_duration(150)
bme.select_gas_heater_profile(0)

# write header if file doesn't already exist
if SAVE_FILE.exists() is False:
    with open(str(SAVE_FILE), "w+", newline="\n") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(HEADER)

try:
    while True:
        data = []

        # store timestamp
        data.append(int(time.time()))

        # read bme680 sensor data
        if bme.get_sensor_data():
            data.append(bme.data.temperature)
            data.append(bme.data.pressure)
            data.append(bme.data.humidity)

            if bme.data.heat_stable:
                data.append(bme.data.gas_resistance)
            else:
                data.append(0)
        else:
            data += [0, 0, 0, 0]

        # read particulate sensor data
        pms_data = pms.read()
        data.append(pms_data.pm_per_1l_air(0.3))
        data.append(pms_data.pm_per_1l_air(0.5))
        data.append(pms_data.pm_per_1l_air(1.0))
        data.append(pms_data.pm_per_1l_air(2.5))
        data.append(pms_data.pm_per_1l_air(5))
        data.append(pms_data.pm_per_1l_air(10))

        # save append data
        with open(str(SAVE_FILE), "a", newline="\n") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(data)

        # print(data)

        time.sleep(15)

except KeyboardInterrupt:
    pass
