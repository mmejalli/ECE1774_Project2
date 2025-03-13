import numpy as np
from bus import bus

class Generator:
    def __init__(self, name:str, bus:bus,voltage_setpoint:float, mw_setpoint:float):
        self.name = name
        self.bus = bus
        self.voltage_setpoint = voltage_setpoint
        self.mw_setpoint = mw_setpoint