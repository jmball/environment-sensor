#!/usr/bin/env python

import time

from pms5003 import PMS5003

print("""all.py - Continously print all data values.

Press Ctrl+C to exit!

""")


# Configure the PMS5003 for Enviro+
pms5003 = PMS5003(
    device='/dev/ttyAMA0',
    baudrate=9600,
    pin_enable=22,
    pin_reset=27
)

print("Setup...")
pms5003.setup()
print("...done")

try:
    while True:
        data = pms5003.read()
        print(data)
        time.sleep(2)

except KeyboardInterrupt:
    pass
