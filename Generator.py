import numpy as np

class Generator:
    def __init__(self, name:str,voltage_setpoint:float, mw_setpoint:float):
        self.name = name
        self.voltage_setpoint = voltage_setpoint
        self.mw_setpoint = mw_setpoint

        #sdgsdgg