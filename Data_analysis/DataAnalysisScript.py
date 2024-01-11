"""""
import pandas as pd

class DataAnalyzer:
    def __init__(self,trial_logger):
        self.trial_logger=trial_logger
        
    def analyze_data(self):
        # Read the CSV file into a DataFrame
        data_file_path = self.trial_logger.csv_file_path

        df = pd.read_csv(data_file_path, delimiter=',')  # Assuming the data is tab-separated

        # Perform analysis
        num_trials = len(df)  # Assuming num_trials is the number of rows in the DataFrame
        additional_reward = num_trials * 0.005

        total_reward = df['Reward'].sum() + additional_reward
        reward_mean = total_reward / num_trials
        total_reward = df['Reward'].sum()
        reward_to_be_delivered = 1.5 - total_reward
        completed_trials_count = df[df['Trial Validity'] == 'Completed Trial'].shape[0]
        mean_reward_by_opponent_choice = df.groupby('Opponent Choice')['Reward'].mean()
        average_time_to_make_decision = df['Time to Make Decision'].mean()
        average_time_to_return_to_center = df['Time to Return to Center'].mean()

        # Return the analysis results as a dictionary
        analysis_results = {
            "Num trials": num_trials,
            "Mean Reward": reward_mean,
            "Total Reward": total_reward,
            "Reward to be Delivered": reward_to_be_delivered,
            "Number of Completed Trials": completed_trials_count,
            #"Mean Reward by Opponent": mean_reward_by_opponent_choice.to_dict(),
            "Average Time to Make Decision": average_time_to_make_decision,
            "Average Time to Return to Center": average_time_to_return_to_center
        }

        return analysis_results
"""""
import pandas as pd

class DataAnalyzer:
    def __init__(self,filepath):
        self.data_file_path = filepath

    def analyze_data(self):
        # Read the CSV file into a DataFrame

        df = pd.read_csv( self.data_file_path, delimiter=',')

        # Perform analysis
        num_trials = df['Trial Number'].max()  # Get the maximum value in 'Trial Number' column
        columns_to_convert = ['Reward', 'Center Reward', 'Opponent Reward', 'Opponent Center Reward']
        for col in columns_to_convert:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Initialize total_reward
        total_reward = 0

        # Iterate through DataFrame and calculate total_reward for valid trials
        for index, row in df.iterrows():
            if row["Trial Validity"] == "Completed Trial":
                total_reward += row["Reward"] + row["Center Reward"]

                # Count the number of 'C' and 'D' in the Mouse Choice column
                num_c_choices = df[df['Mouse Choice'] == 'C'].shape[0]
                num_d_choices = df[df['Mouse Choice'] == 'D'].shape[0]

        # Convert 'Reward' column to numeric and calculate mean reward
        df['Reward'] = pd.to_numeric(df['Reward'], errors='coerce')
        reward_mean = total_reward / num_trials
        reward_to_be_delivered = 1.5 - total_reward

        # Calculate mean reward by opponent choice
        mean_reward_by_opponent_choice = df.groupby('Opponent Choice')['Reward'].mean()

        # Calculate average times
        average_time_to_make_decision = df['Time to Make Decision'].mean()
        average_time_to_return_to_center = df['Time to Return to Center'].mean()

        # Calculate the percentage of 'C' and 'D' choices

        percentage_c = (num_c_choices / num_trials) * 100
        percentage_d = (num_d_choices / num_trials) * 100
        # Return the analysis results as a dictionary
        analysis_results = {
            "Num trials": num_trials,
            "Mean Reward": reward_mean,
            "Total Reward": total_reward,
            "Reward to be Delivered": reward_to_be_delivered,
            "Mean Reward by Opponent": mean_reward_by_opponent_choice.to_dict(),
            "Average Time to Make Decision": average_time_to_make_decision,
            "Average Time to Return to Center": average_time_to_return_to_center,
            "Number of C Choices": num_c_choices,
            "Number of D Choices": num_d_choices,
            "Percentage of C Choices": percentage_c,
            "Percentage of D Choices": percentage_d
        }

        return analysis_results
    def save_results_to_file(self, results):
        result_file_path = self.data_file_path.replace('data_from_trials', 'data_analysis_results').replace(
            '.csv', '.txt')

        with open(result_file_path, 'w') as file:
            for key, value in results.items():
                file.write(f'{key}: {value}\n')

        return result_file_path
