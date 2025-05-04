# Main file setup
from Powerflow import Powerflow
from Settings import Settings
from Circuit import Circuit
from Jacobian import Jacobian
from Geometry import Geometry
from Conductor import Conductor
from Bundle import Bundle
from Settings import Settings
from Newton_Raphson import Newton_Raphson


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

## Check Newton Raphson
print("running Newton Raphson")
solver = Newton_Raphson(circuit1, 0.1, 5)
solver.solve()
