# This class describes the powerflow modeling of a system
# Includes power mismatch and power injection equations

from Circuit import Circuit
from Bus import Bus
from Geometry import Geometry
from Conductor import Conductor
from Bundle import Bundle

import numpy as np
import pandas as pd

class Powerflow:
    def __init__(self, circuit: Circuit):
        # Load in data from sample circuit
        self.circuit = circuit

        # Should start from flat start: all bus voltages are 1.0 and 0 angle by default
        self.flat_start()

        #Calculate Power injection for buses
        p_injected,q_injected = self.calc_PQ()

        #Compute Mismatch
        self.mismatch(p_injected,q_injected)



    def flat_start(self):
        for bus in self.circuit.buses.values():
            bus.delta = 0
            bus.vpu = 1.0

    def calc_PQ(self):
        # Initialize real and reactive power array and running totals
        p_calc = np.zeros(len(self.circuit.buses))
        p_k = 0

        q_calc = np.zeros(len(self.circuit.buses))
        q_k = 0

        #Create list of bus names
        bus_names = list(self.circuit.buses.keys())

        for k in range(0, len(self.circuit.buses)):
            bus_k = self.circuit.buses[bus_names[k]]
            p_k = 0  # Reset for each bus k
            q_k = 0  # Reset for each bus k

            for m in range(0, len(self.circuit.buses)):
                bus_m = self.circuit.buses[bus_names[m]]
                y_bus_km = self.circuit.ybus[k][m]
                y_bus_theta_km = np.angle(y_bus_km)

                #Calc real and reactive power for current k and m indexes
                p_k += bus_k.vpu * bus_m.vpu * abs(y_bus_km)*np.cos(bus_k.delta - bus_m.delta - y_bus_theta_km)
                q_k += bus_k.vpu * bus_m.vpu * abs(y_bus_km)*np.sin(bus_k.delta - bus_m.delta - y_bus_theta_km)

            #store values for current iteration
            p_calc[k] = p_k
            q_calc[k] = q_k

        print(p_calc)
        print(q_calc)

        # Print real values only
        results_df = pd.DataFrame(
            [np.round(p_calc.real, 4), np.round(q_calc.real, 4)],  # Use .real to discard imaginary part
            index=["P (MW)", "Q (MVAR)"],  # Row labels
            columns=bus_names,  # Column labels are bus names
        )
        print(results_df)

        return p_calc, q_calc

    def mismatch(self, p_injected, q_injected):
        p_mismatch = np.zeros(len(self.circuit.buses))
        q_mismatch = np.zeros(len(self.circuit.buses))

       # for k in range(0, len(self.circuit.buses)):
           # p_mismatch =


if __name__ == "__main__":
    """
    Powerflow Validation
    """

    circuit1 = Circuit("Circuit1")

    # Adding buses
    circuit1.add_bus("bus1", 20)
    circuit1.add_bus("bus2", 230)
    circuit1.add_bus("bus3", 230)
    circuit1.add_bus("bus4", 230)
    circuit1.add_bus("bus5", 230)
    circuit1.add_bus("bus6", 230)
    circuit1.add_bus("bus7", 18)

    # Transmission Line sub-classes
    conductor1 = Conductor("Partridge", 0.642, 0.0217, 0.385, 460)
    bundle1 = Bundle("Bundle1", 2, 1.5, conductor1)
    geometry1 = Geometry("Geometry1", 0, 0, 9.75 * 2, 0, 9.75 * 4, 0)

    # Adding Transmission Lines
    circuit1.add_transmission_lines("Line1", "bus2", "bus4", bundle1, geometry1, 10)
    circuit1.add_transmission_lines("line2", "bus2", "bus3", bundle1, geometry1, 25)
    circuit1.add_transmission_lines("line3", "bus3", "bus5", bundle1, geometry1, 20)
    circuit1.add_transmission_lines("Line4", "bus4", "bus6", bundle1, geometry1, 20)
    circuit1.add_transmission_lines("Line5", "bus5", "bus6", bundle1, geometry1, 10)
    circuit1.add_transmission_lines("Line6", "bus4", "bus5", bundle1, geometry1, 35)

    # Adding Transformers
    circuit1.add_transformer("Tx1", "bus1", "bus2", 125, 8.5, 10)
    circuit1.add_transformer("Tx2", "bus6", "bus7", 200, 10.5, 12)

    circuit1.calc_y_admit()

    powerflow1 = Powerflow(circuit1)