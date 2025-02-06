from Bus import Bus
from Geometry import Geometry
from Transformer import Transformer
from Bundle import Bundle
from TransmissionLine import TransmissionLine


class Circuit:
    def __init__(self, name:str):
        self.name = name
        self.transformers={}
        self.buses={}
        self.transmission_lines={}

    def add_bus(self, name:str, base_kv:float):
        self.buses[name]=Bus(name, base_kv)

    def add_transformer(self, name:str, bus1:str, bus2:str, power_rating:float, impedance_percent:float, x_over_r_ratio:float):
        self.transformers[name]=Transformer(name, self.buses[bus1], self.buses[bus2], power_rating,impedance_percent, x_over_r_ratio)

    def add_transmission_lines(self, name:str, bus1:str, bus2:str, bundle:Bundle, geometry:Geometry, length:float):
        self.transmission_lines[name]=TransmissionLine(name, self.buses[bus1], self.buses[bus2], bundle, geometry, length)



if __name__ == "__main__":

    circuit1=Circuit("Test Circuit")

    print(circuit1.name)
    print(type(circuit1.name))
    print(circuit1.buses)
    print(circuit1.transformers)
    print(circuit1.transmission_lines)
    print(type(circuit1.buses))
    print(type(circuit1.transformers))
    print(type(circuit1.transmission_lines))

    circuit1.add_bus("Bus1",230)
    circuit1.add_bus("Bus2",13)
    print(type(circuit1.buses["Bus1"]))
    print(circuit1.buses["Bus1"].name,circuit1.buses["Bus1"].base_kv)

    circuit1.add_transformer("Tx1","Bus1","Bus2",100, 3, .8)

    print(circuit1.transformers["Tx1"].name,type(circuit1.transformers["Tx1"]),circuit1.transformers["Tx1"].bus1.name,type(circuit1.transformers["Tx1"].bus1))