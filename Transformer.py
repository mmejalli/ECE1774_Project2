import numpy as np
from Bus import Bus

class Transformer:
    def __init__(self, name: str, bus1: Bus, bus2: Bus, power_rating: float, impedance_percent: float,
                 x_over_r_ratio: float):
        """Initialize a Transformer instance with given parameters."""
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.power_rating = power_rating
        self.impedance_percent = impedance_percent
        self.x_over_r_ratio = x_over_r_ratio

        # Calculate impedance and admittance values
        self.impedance = self.calculate_impedance()
        self.admittance = 1 / self.impedance if self.impedance != 0 else float('inf')
        self.y_prim_mat=None

    def calculate_impedance(self):
        """Calculate the impedance based on power rating and impedance percentage."""
        base_impedance = (self.bus1.base_kv ** 2) / self.power_rating
        z_pu = self.impedance_percent / 100
        return z_pu * base_impedance

    def calculate_admittance(self):
        """Calculate the admittance as the reciprocal of impedance."""
        return 1 / self.impedance if self.impedance != 0 else float('inf')

    def yprim(self):
        """Compute the primitive admittance matrix."""
        y = self.calculate_admittance()
        self.y_prim_mat=np.array([[y, -y], [-y, y]])
        return self.y_prim_mat

    def Rpu_Xpu(self):
        base_impedance = (self.bus1.base_kv ** 2) / self.power_rating
        z_pu = self.impedance_percent / 100
        x_pu = z_pu * self.x_over_r_ratio/np.sqrt(1+self.x_over_r_ratio**2)
        r_pu = z_pu * 1/np.sqrt(1 + self.x_over_r_ratio**2)
        return r_pu, x_pu