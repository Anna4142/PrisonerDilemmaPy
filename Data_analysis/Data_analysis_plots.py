import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('Agg')


class DataPlotter:
    def __init__(self, filepath, save_directory=None):
        self.data_file_path = filepath
        self.save_directory = save_directory  # Path to the directory where plots will be saved
        self.data = None

    def load_data(self):
        """Load data from the CSV file."""
        self.data = pd.read_csv(self.data_file_path, delimiter=',')
        print("Data loaded successfully.")

    def filter_completed_trials(self):
        """Filter the data to include only completed trials."""
        if self.data is not None:
            self.data = self.data[self.data['Trial Validity'] == 'Completed Trial']
            print("Filtered for completed trials.")
        else:
            print("Data is not loaded yet.")

    def save_plot_to_directory(self, filename):
        """Determine the save path for the plot."""
        if self.save_directory is not None:
            # Use the specified save directory
            plots_directory_path = self.save_directory
        else:
            # Default behavior: replace part of the data file path
            directory_path = os.path.dirname(self.data_file_path)
            plots_directory_path = directory_path.replace('data_from_trials', 'data_plots')

        # Ensure the plots directory exists
        os.makedirs(plots_directory_path, exist_ok=True)

        # Define the full file path for the plot
        plot_file_path = os.path.join(plots_directory_path, filename)

        return plot_file_path

    def plot_decision_time(self):
        """Plot the time to make decisions."""
        self.plot_data('Time to Make Decision', 'Time to Make Decision for Each Completed Trial',
                       'Time to Make Decision (seconds)', 'time_to_make_decision_plot.png')

    def plot_return_time(self):
        """Plot the time to return to center."""
        self.plot_data('Time to Return to Center', 'Time to Return to Center for Each Completed Trial',
                       'Time to Return to Center (seconds)', 'time_to_return_to_center_plot.png')

    def plot_data(self, column_name, title, ylabel, filename):
        """Generic method to plot data and save to a specific directory."""
        if self.data is not None:
            plt.figure(figsize=(10, 6))
            plt.plot(self.data['Trial Number'], self.data[column_name], marker='o', linestyle='-', color='blue')
            plt.title(title)
            plt.xlabel('Trial Number')
            plt.ylabel(ylabel)
            plt.grid(True)

            # Save the plot to the specified directory
            save_path = self.save_plot_to_directory(filename)
            plt.savefig(save_path)
            plt.close()  # Close the plot to avoid displaying it in non-interactive environments
            print(f"Plot saved to {save_path}")
        else:
            print("Data is not filtered or loaded yet.")