import numpy as np
from bus import bus

class Load:
    def __init__(self, name:str, bus:bus, real_power:float, reactive_power:float):
        self.name = name
        self.bus = bus
        self.real_power = real_power
        self.reactive_power = reactive_power