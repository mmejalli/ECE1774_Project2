# This class describes the powerflow modeling of a system
# Includes power mismatch and power injection equations
from contextlib import nullcontext

from Circuit import Circuit
from Bus import Bus
from Geometry import Geometry
from Conductor import Conductor
from Bundle import Bundle
from Settings import Settings

import numpy as np
import pandas as pd

s=Settings()

class Powerflow:
    def __init__(self, circuit: Circuit):
        # Load in data from sample circuit
        self.circuit = circuit

        # Should start from flat start: all bus voltages are 1.0 and 0 angle by default
        self.flat_start()

        '''
        v_bus = [1,0.9369,0.9205,0.9298,0.9267,0.9397,0.9999]
        del_bus = [0, -4.44, -5.46, -4.7, -4.83, -3.95, 2.15]

        # For debugging, use input bus voltage function
        self.input_bus_voltages(v_bus,del_bus)
        '''

        #Calculate Power injection for buses
        p_injected,q_injected = self.calc_PQ()

        #Compute Mismatch
        self.calc_mismatch(p_injected,q_injected)




    def flat_start(self):
        for bus in self.circuit.buses.values():
            bus.delta = 0
            bus.vpu = 1.0

    def input_bus_voltages(self, vpu_array, delta_array):
        """
        Assigns bus voltages and angles to the circuit buses.

        Parameters:
        vpu_array (np.ndarray): Array of per-unit voltage magnitudes.
        delta_array (np.ndarray): Array of voltage angles in radians.
        """



        assert len(vpu_array) == len(self.circuit.buses), "Voltage array length mismatch"
        assert len(delta_array) == len(self.circuit.buses), "Angle array length mismatch"

        bus_names = list(self.circuit.buses.keys())

        for idx, name in enumerate(bus_names):
            bus = self.circuit.buses[name]
            bus.vpu = vpu_array[idx]
            bus.delta = delta_array[idx]

        # Create and print verification DataFrame
        voltage_df = pd.DataFrame({
            "Bus": bus_names,
            "Voltage (pu)": np.round(vpu_array, 4),
            "Angle (rad)": np.round(delta_array, 4)
        }).set_index("Bus")

        print("\nUpdated Bus Voltages and Angles:")
        print(voltage_df)

    def calc_PQ(self):
        # Initialize real and reactive power array and running totals
        p_calc = np.zeros(len(self.circuit.buses), dtype=np.float64)
        p_k = 0

        q_calc = np.zeros(len(self.circuit.buses), dtype=np.float64)
        q_k = 0

        #Create list of bus names
        bus_names = list(self.circuit.buses.keys())

        for k in range(0, len(self.circuit.buses)):
            bus_k = self.circuit.buses[bus_names[k]]
            p_k = 0  # Reset for each bus k
            q_k = 0  # Reset for each bus k
            delta_k_rad = np.radians(bus_k.delta)

            for m in range(0, len(self.circuit.buses)):
                bus_m = self.circuit.buses[bus_names[m]]
                y_bus_km = self.circuit.ybus[k][m]
                y_bus_theta_km = np.angle(y_bus_km)

                delta_m_rad = np.radians(bus_m.delta)
                angle_diff = delta_k_rad - delta_m_rad - y_bus_theta_km

                #Calc real and reactive power for current k and m indexes
                p_k += bus_k.vpu * bus_m.vpu * abs(y_bus_km)*np.cos(angle_diff)
                q_k += bus_k.vpu * bus_m.vpu * abs(y_bus_km)*np.sin(angle_diff)

            #store values for current iteration
            p_calc[k] = p_k
            q_calc[k] = q_k

        #print(p_calc)
        #print(q_calc)

        # Print real values only
        results_df = pd.DataFrame(
            [np.round(p_calc.real, 4), np.round(q_calc.real, 4)],  # Use .real to discard imaginary part
            index=["P (MW)", "Q (MVAR)"],  # Row labels
            columns=bus_names,  # Column labels are bus names
        )
        print(results_df)



        return p_calc, q_calc

    def calc_mismatch(self, p_injected, q_injected):
        p_mismatch = np.zeros(len(self.circuit.buses))
        q_mismatch = np.zeros(len(self.circuit.buses))

        non_slack_indeces = []
        pq_indeces = []

        # Create list of bus names
        bus_names = list(self.circuit.buses.keys())


        for k in range(0, len(self.circuit.buses)):
            bus_k = self.circuit.buses[bus_names[k]]
            if bus_k.bus_type == "Slack_Bus":
                p_mismatch[k] = None
                q_mismatch[k] = None

            elif bus_k.bus_type == "PQ_Bus":
                p_mismatch[k] = -self.circuit.buses[bus_names[k]].load.real_power/s.base_power - p_injected[k]
                q_mismatch[k] = -self.circuit.buses[bus_names[k]].load.reactive_power/s.base_power - q_injected[k]
                non_slack_indeces.append(k)
                pq_indeces.append(k)

            elif bus_k.bus_type == "PV_Bus":
                p_mismatch[k] = self.circuit.buses[bus_names[k]].generator.mw_setpoint/s.base_power - p_injected[k]
                q_mismatch[k] = None
                non_slack_indeces.append(k)

            else:
                print("Not valid bus type")


        ##Print mismatch matrices in a dataframe
        mismatch_df = pd.DataFrame(
            [np.round(p_mismatch, 4), np.round(q_mismatch, 4)],
            index=["P Mismatch (MW)", "Q Mismatch (MVAR)"],
            columns=bus_names,
        )
        #print(mismatch_df,"\n")



        #print ("Non-slack indeces:", non_slack_indeces, "\n")
        #print ("PQ indeces:", pq_indeces, "\n")

        p_mismatch = p_mismatch[non_slack_indeces]
        q_mismatch = q_mismatch[pq_indeces]

        mismatch = np.concatenate((p_mismatch.reshape(-1, 1), q_mismatch.reshape(-1, 1)), axis=0)

        print("Mismatch\n")
        print(mismatch,"\n")

        return mismatch






if __name__ == "__main__":
    """
    Powerflow Validation
    """

    circuit1 = Circuit("Circuit1")

    # Adding buses
    circuit1.add_bus("bus1", 20, 1, 0, "Slack_Bus")
    circuit1.add_bus("bus2", 230)
    circuit1.add_bus("bus3", 230)
    circuit1.add_bus("bus4", 230)
    circuit1.add_bus("bus5", 230)
    circuit1.add_bus("bus6", 230)
    circuit1.add_bus("bus7", 18, 1, 0, "PV_Bus")

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

    # Adding Generators
    circuit1.add_generator("Gen1", 1.0, 100, "bus1")
    circuit1.add_generator("Gen2", 1.0, 200.0, "bus7")

    # Adding Loads
    circuit1.add_load("Load1", 0, 0, "bus2")
    circuit1.add_load("Load2", 110, 50, "bus3")
    circuit1.add_load("Load3", 100, 70, "bus4")
    circuit1.add_load("Load4", 100, 65, "bus5")
    circuit1.add_load("Load5", 0, 0, "bus6")

    circuit1.calc_y_admit()

    powerflow1 = Powerflow(circuit1)