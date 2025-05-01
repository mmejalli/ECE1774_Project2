from Powerflow import Powerflow
from Settings import Settings
from Circuit import Circuit
from JacobianTwo import Jacobian

import numpy as np
import pandas as pd

s = Settings()


class Newton_Raphson:
    def __init__(self, circuit: Circuit, tol: float = 0.001, max_iter: int = 50):
        self.circuit = circuit
        self.tol = tol
        self.max_iter = max_iter
        self.buses = circuit.buses
        self.circuit.calc_y_admit()
        self.powerflow = Powerflow(circuit)
        self.powerflow.flat_start()
        self.p_inj,self.q_inj =  self.powerflow.calc_PQ()

    #Function to solve Newton Raphson Method
    def solve(self):

        #Begin from iteration 0 with flat start mismatches
        iteration = 0

        #Continue algorithm until max iterations are reached
        while iteration < self.max_iter:

            print("Running Powerflow Mismatch from NR\n")
            self.p_inj, self.q_inj = self.powerflow.calc_PQ()

            #Start with flat start mismatches, compute using p_inj and q_inj
            mismatch = self.powerflow.calc_mismatch(self.p_inj, self.q_inj)

            #Debug -- Print Mismatches
            print("Mismatch\n", mismatch)



            #if mismatches are within tolerance, algorithm stops
            if np.max(np.abs(mismatch)) < self.tol:
                break

            #Calculate Jacobian Matrix based on mismatches
            Jacobian_obj = Jacobian(self.circuit)
            jacobian_matrix = Jacobian_obj.calc_jacobian()

            #print("Jacobian matrix\n")
            #print(jacobian_matrix)

            #Change in x(mismatches) solved via linear algebra
            delta_x = np.linalg.solve(jacobian_matrix, mismatch)
            print(self.format_delta_x(delta_x))

            print("Change in voltage angles and magnitudes\n", delta_x)

            #Update voltage values
            self.update_voltages(delta_x)

            #Move on to next iteration
            iteration += 1

            mismatch_df = self.format_mismatch_dataframe(mismatch)
            #print(mismatch_df)

            #print("\n", iteration)

        #Once exiting loop, check if max iterations was reached
        if iteration == self.max_iter:
            print("Warning: Newton-Raphson method did not converge")


    def update_voltages(self, delta_x):
        bus_names = list(self.circuit.buses.keys())
        # Step 1: Get non-slack buses (angles to update)
        non_slack_buses = [bus for bus in self.circuit.buses.values() if bus.bus_type != "Slack_Bus"]
        # Step 2: Get PQ buses (magnitudes to update)
        pq_buses = [bus for bus in self.circuit.buses.values() if bus.bus_type == "PQ_Bus"]

        # Step 3: Update voltage angles
        for i, bus in enumerate(non_slack_buses):
            bus.delta += delta_x[i]  # radians

        # Step 4: Update voltage magnitudes (only PQ buses)
        for j, bus in enumerate(pq_buses):
            bus.vpu += delta_x[len(non_slack_buses) + j]

    def format_mismatch_dataframe(self, mismatch_vector):
        # Get bus references
        non_slack_buses = [bus for bus in self.circuit.buses.values() if bus.bus_type != "Slack_Bus"]
        pq_buses = [bus for bus in self.circuit.buses.values() if bus.bus_type == "PQ_Bus"]

        # Build row labels
        labels = []

        # ΔP rows
        for bus in non_slack_buses:
            labels.append(f"ΔP_{bus.name}")

        # ΔQ rows
        for bus in pq_buses:
            labels.append(f"ΔQ_{bus.name}")

        # Create DataFrame
        mismatch_df = pd.DataFrame(mismatch_vector.reshape(-1, 1), index=labels, columns=["Mismatch (p.u.)"])
        return mismatch_df

    def format_delta_x(self, delta_x):
        labels = []

        # Count buses by type
        for bus in self.circuit.buses.values():
            if bus.bus_type != "Slack_Bus":
                labels.append(f"Δδ_{bus.name}")
        for bus in self.circuit.buses.values():
            if bus.bus_type == "PQ_Bus":
                labels.append(f"ΔV_{bus.name}")

        delta_df = pd.DataFrame(delta_x, index=labels, columns=["delta_x"])

        pd.set_option('display.float_format', lambda x: f'{x:.6f}')
        return delta_df