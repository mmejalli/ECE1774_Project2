from Powerflow import Powerflow
from Settings import Settings
from Circuit import Circuit

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
        self.ybus = circuit.ybus
        self.powerflow = Powerflow(circuit)
        self.powerflow.flat_start()
        p_inj,q_inj =  self.powerflow.calc_PQ()
        self.powerflow.calc_mismatch(q_inj, p_inj)

    def solve(self):
        iteration = 0
        while iteration < self.max_iter:
            mismatch = self.calculate_power_mismatch()
            if np.max(np.abs(mismatch)) < self.tol:
                break
            jacobian = self.compute_jacobian()
            delta_x = np.linalg.solve(jacobian, mismatch)
            self.update_voltages(delta_x)
            iteration += 1
        if iteration == self.max_iter:
            print("Warning: Newton-Raphson method did not converge")

    def update_voltages(self, delta_x):
        self.angles[:-1] += delta_x[:len(self.angles) - 1]
        self.voltages[self.pq_buses] += delta_x[len(self.angles) - 1:]