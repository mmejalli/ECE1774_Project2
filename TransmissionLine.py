import numpy as np
import math
from Bus import Bus
from Bundle import Bundle
from Geometry import Geometry

class TransmissionLine:
    def __init__(self, name: str, bus1: Bus, bus2: Bus, bundle: Bundle, geometry: Geometry, length: float):
        """Initialize a TransmissionLine instance with given parameters."""
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.geometry = geometry
        self.length = length

        # Calculate series impedance and shunt admittance
        self.series_impedance = self.calculate_series_impedance()
        self.shunt_admittance = self.calculate_shunt_admittance()
        self.yprim = self.calc_yprim()

    def calculate_series_impedance(self):
        """Calculate the series impedance of the transmission line."""
        Ra = self.bundle.conductor.resistance / self.bundle.num_conductors * 1609 * self.length
        Xa = 377 * 2e-7 * math.log(self.geometry.DEQ / self.bundle.DSL) * 1609 * self.length  # ohm
        return complex(Ra, Xa)

    def calculate_shunt_admittance(self):
        """Calculate the shunt admittance of the transmission line."""
        y = 377 * 1609 * 2 * math.pi * 8.854e-12 / math.log(self.geometry.DEQ / self.bundle.DSC) * self.length
        return complex(0, y)

    def get_zbase(self):
        """return Zbase value"""
        return self.bus1.base_kv**2/100

    def calc_yprim(self):
        """Compute the primitive admittance matrix."""
        y_series = 1 / self.series_impedance if self.series_impedance != 0 else float('inf')
        y_shunt = self.shunt_admittance
        return np.array([[y_series + y_shunt, -y_series], [-y_series, y_series + y_shunt]])

    def __str__(self):
        """Return a formatted string representing the transmission line object."""
        return (
            f"Transmission Line: {self.name}\n"
            f"Connected Buses: {self.bus1.name} <--> {self.bus2.name}\n"
            f"Bundle: {self.bundle.name}\n"
            f"Geometry: {self.geometry.name}\n"
            f"Length: {self.length} km\n"
            f"Series Impedance: {self.series_impedance/self.get_zbase()} pu\n"
            f"Shunt Admittance: {self.shunt_admittance/self.get_zbase()} pu\n"
            f"Y-Primitive Matrix: {self.yprim}"
        )

if __name__ == "__main__":
    """
    TransmissionLine Validation
    """
    #line1 = TransmissionLine("Line 1", bus1, bus2, bundle1, geometry1, 10)

    #print(line1)

    #print(line1.get_base_values(20,100))
