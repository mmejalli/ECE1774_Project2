class Bus:

    bus_index = 0

    def __init__(self, name, base_kv):
        """
        Initialize a Bus object.

        :param name: Name of the bus (str).
        :param base_kv: Base KV (float).
        """
        self.name = name
        self.base_kv = base_kv
        self.index = Bus.bus_index
        Bus.bus_index += 1

    def __str__(self):
        """Return a formatted string representing the bus object."""
        return (
            f"Bus Name: {self.name}\n"
            f"Bus Index: {self.index}\n"
            f"Base Voltage: {self.base_kv} kV"
        )

if __name__ == "__main__":
    """
    Bus Validation
    """
    bus1 = Bus("Bus 1", 20)
    bus2 = Bus("Bus 2", 230)

    print(bus1)
    print(bus2)
    print("Bus count: ", Bus.bus_count)