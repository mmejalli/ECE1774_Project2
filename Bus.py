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