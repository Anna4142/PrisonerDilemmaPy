
import pandas as pd

class DataAnalyzer:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def analyze_data(self):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(self.data_file_path, delimiter=',')  # Assuming the data is comma-separated

        # Perform analysis
        reward_mean = df['Reward'].mean()
        total_reward = df['Reward'].sum()
        reward_to_be_delivered = 1.5 - total_reward
        completed_trials_count = df[df['Trial Validity'] == 'Completed Trial'].shape[0]
        mean_reward_by_opponent_choice = df.groupby('Opponent Choice')['Reward'].mean()

        # Return the analysis results as a dictionary
        analysis_results = {
            "Mean Reward": reward_mean,
            "Total Reward": total_reward,
            "Reward to be Delivered": reward_to_be_delivered,
            "Number of Completed Trials": completed_trials_count,
            "Mean Reward by Opponent": mean_reward_by_opponent_choice.to_dict()
        }

        return analysis_results