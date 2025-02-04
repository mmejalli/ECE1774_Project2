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
        return 0.01 * self.length  # PLACEHOLDER, FIX WHEN SUBCLASSES IMPLEMENTED

    def calculate_shunt_admittance(self):
        """Calculate the shunt admittance of the transmission line."""
        return 0.001 * self.length  # PLACEHOLDER, FIX WHEN SUBCLASSES IMPLEMENTED

    def get_base_values(self, vbase, sbase):
        """return Zbase and Ybase values"""
        return vbase**2/sbase, 1/(vbase**2/sbase)

    def calc_yprim(self):
        """Compute the primitive admittance matrix."""
        y_series = 1 / self.series_impedance if self.series_impedance != 0 else float('inf')
        y_shunt = self.shunt_admittance
        return [[y_series + y_shunt, -y_series], [-y_series, y_series + y_shunt]]

    def __str__(self):
        """Return a formatted string representing the transmission line object."""
        return (
            f"Transmission Line: {self.name}\n"
            f"Connected Buses: {self.bus1} <--> {self.bus2}\n"
            f"Bundle: {self.bundle}\n"
            f"Geometry: {self.geometry}\n"
            f"Length: {self.length} km\n"
            f"Series Impedance: {self.series_impedance} Ω\n"
            f"Shunt Admittance: {self.shunt_admittance} S\n"
            f"Y-Primitive Matrix: {self.yprim}"
        )

if __name__ == "__main__":
    """
    TransmissionLine Validation
    """
    line1 = TransmissionLine("Line 1", bus1, bus2, bundle1, geometry1, 10)

    print(line1)

    print(line1.get_base_values(20,100))
