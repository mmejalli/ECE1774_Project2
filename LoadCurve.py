import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from Circuit import Circuit
from Load import Load
from Bus import Bus

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

class LoadCurve:
    """
    Initialization of LoadCurve Object
    Parameters:
        Circuit object (populated with buses, loads, etc.)
        Filepath for .csv file with load curve data
            Pass as a string literal to avoid escape characters when pasting in Windows.
            Format: r"C:\myFilepath\myFile.csv"

    Formatting load curve .csv file
        Must have a column named "Hour" with values 0-23
        Must have at least one column with corresponding multipliers (user chooses these).
        Any subsequent non-zero loads in the system must have a column with corresponding multipliers.
        Load columns will be applied to loads in the circuit in the order they appear in the .csv file.
        Ex:

            circuit.add_load("Load 1")
            circuit.add_load("Load 2")
            circuit.add_load("Load 3")

            The first load column (leftmost) will be applied to load 1, the next column to load 2, and so on.

        Do not leave blank columns between filled data columns in the .csv file.
        If cells are left blank, this will read as NaN, and the Load data for that load will not be plotted.
        Multipliers can be floats or ints greater than or equal to 0.

    Any Value Error when being used is due to incorrect formatting.
    Ensure correct naming conventions of file columns, and equal number of load columns and loads in the circuit object.

    """
    def __init__(self, circuit, csv_path):

        #member variables
        self.usableLoads = []
        self.newLoadData = []
        self.circuit = circuit
        self.load_profile = pd.read_csv(csv_path)
        #self.loadNames = []

        #functions to be called on initialization
        self.validate_csv()
        self.get_all_multipliers()
        self.validate_loads()
        self.apply_all_hours_to_circuit()

    def validate_csv(self):
        """
        Checks that csv is labeled correctly with an Hour Column and at least 1 load column.
        """
        if 'Hour' not in self.load_profile.columns:
            raise ValueError("CSV must contain 'Hour' column")

        # All other columns are assumed to be Load labels
        self.load_columns = [col for col in self.load_profile.columns if col != 'Hour']
        if not self.load_columns:
            raise ValueError("CSV must contain at least one load column (e.g., 'Load 1')")



    def get_all_multipliers(self):
        """Returns a list of load multipliers for all hours. Each row is a list of multipliers per load."""
        return self.load_profile[self.load_columns].values.tolist()

    def validate_loads(self):
        """
        Ensures csv file has same number of usable loads as the circuit object
        Note: A usable load is one with non-zero real or reactive power
        """
        all_multipliers = self.get_all_multipliers()

        for bus_name, bus in self.circuit.buses.items():
            if (bus.bus_type == "PQ_Bus") & (bus.load.real_power != 0 | bus.load.reactive_power != 0):
                self.usableLoads.append(bus.load)

        if len(self.usableLoads) != len(all_multipliers[0]):
            raise ValueError(
                f"Mismatch: Circuit has {len(self.usableLoads)} non-zero loads, "
                f"but CSV contains {len(all_multipliers[0])} load columns."
            )


    def apply_all_hours_to_circuit(self):
        """
        Applies load multipliers from the CSV to the circuit for all 24 hours.
        Returns a list of dictionaries containing hour and updated load values.
        """

        for hour, multipliers in enumerate(self.get_all_multipliers()):
            row = {"Hour": hour}
            for i, (load, multiplier) in enumerate(zip(self.usableLoads, multipliers)):
                original_power = complex(load.real_power, load.reactive_power)
                scaled_power = original_power * multiplier
                #row[f"Load {i + 1} P"] = scaled_power.real
                #row[f"Load {i + 1} Q"] = scaled_power.imag
                row[f"{self.load_columns[i]} S (MVA)"] = abs(scaled_power)
            self.newLoadData.append(row)

        return

    def print_load_dataframe(self):
        """
        Returns a DataFrame showing P and Q for each load over 24 hours.
        Columns: 'Load 1 P', 'Load 1 Q', ..., etc.
        Rows: Hours 0 to 23.
        """

        df = pd.DataFrame(self.newLoadData)
        df.set_index("Hour", inplace=True)
        print(df)
        return df

    def plot_complex_power_vs_time(self):
        # Prepare data for plotting
        df = pd.DataFrame(self.newLoadData)
        hours = df["Hour"] if "Hour" in df.columns else df.index

        # Create the plot
        plt.figure(figsize=(10, 6))
        colors = ['r', 'g', 'b', 'm', 'c', 'y', 'k']  # Add more colors if needed
        num_loads = len(self.usableLoads)

        for i in range(num_loads):
            s_col = f"{self.load_columns[i]} S (MVA)"
            if s_col in df.columns:
                y_values = df[s_col].values
                # Perform interpolation (use cubic or linear interpolation)
                f_interp = interpolate.interp1d(hours, y_values, kind='cubic', fill_value="extrapolate")

                # Generate new hours for smoother curve
                new_hours = np.linspace(hours.min(), hours.max(), 500)  # More points for smoother curve
                smooth_y_values = f_interp(new_hours)

                # Plot the smoothed data
                plt.plot(new_hours, smooth_y_values, label=self.load_columns[i], color=colors[i % len(colors)])

        # Add title and labels
        plt.title('Apparent Power Magnitude |S| vs. Hour')
        plt.xlabel('Hour')
        plt.ylabel('Apparent Power |S| (MVA)')

        # Customize the x-axis ticks to show 4-hour increments
        plt.xticks(np.arange(0, 24, 4))  # Set ticks at 0, 4, 8, 12, 16, 20

        # Add legend
        plt.legend()

        # Show the plot
        plt.grid(True)
        plt.show()