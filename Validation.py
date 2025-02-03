from Bus import Bus
from Transformer import Transformer
from TransmissionLine import TransmissionLine
from Bundle import Bundle
from Geometry import Geometry
from Conductor import Conductor

"""
Bus Validation
"""
bus1 = Bus("Bus 1", 20)
bus2 = Bus("Bus 2", 230)

print("Bus 1 name: ", bus1.name, "kv: ", bus1.base_kv, "index: ", bus1.index)
print("Bus 1 name: ", bus2.name, "kv: ", bus2.base_kv, "index: ", bus2.index)
print("Bus count: ", Bus.bus_count)

"""
Transformer Validation
"""
transformer1 = Transformer("T1", bus1, bus2, 125,8.5, 10)

print("XFMR name:", transformer1.name, "bus 1: ", transformer1.bus1.name, "bus 2:", transformer1.bus2.name, "power rating: ",transformer1.power_rating)
print("XFMR Impedance: ", transformer1.calculate_impedance(), "XFMR Admittance: ", transformer1.calculate_admittance())
print("XFMR Yprim: ", transformer1.yprim())

"""
TransmissionLine Validation
"""
line1 = TransmissionLine("Line 1", bus1, bus2, bundle1, geometry1, 10)

print("Line name: ", line1.name, "bus 1: ", line1.bus1.name, "bus 2: ", line1.bus2.name, "line length: ", line1.length)