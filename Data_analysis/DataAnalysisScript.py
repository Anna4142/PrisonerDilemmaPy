
import pandas as pd
import os


class DataAnalyzer:
    def __init__(self, filepath):
        self.data_file_path = filepath

    def analyze_data(self):
        # Read the CSV file into a DataFrame

        df = pd.read_csv(self.data_file_path, delimiter=',')

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

        current_datetime = pd.Timestamp.now()

        current_date =  current_datetime.strftime("%Y%m%d")


        analysis_results = {
            "Date": current_date,
            "Num trials": num_trials,
            "Mean Reward": reward_mean,
            "Total Reward": total_reward,
            "Water to be given": reward_to_be_delivered,
            "Mean Reward by Opponent": mean_reward_by_opponent_choice.to_dict(),
            "Average Time to Make Decision": average_time_to_make_decision,
            "Average Time to Return to Center": average_time_to_return_to_center,
            "Number of C Choices": num_c_choices,
            "Number of D Choices": num_d_choices,
            "Percentage of C Choices": percentage_c,
            "Percentage of D Choices": percentage_d,

        }

        return analysis_results

    def save_results_to_file(self, results):
        current_datetime = pd.Timestamp.now()
        current_date = current_datetime.strftime("%Y%m%d")

        # Add the date to the results
        results_with_date = results.copy()
        results_with_date['Date'] = current_date

        # Extract the directory path from the current data file path and replace subdirectory
        directory_path = os.path.dirname(self.data_file_path)
        analysis_directory_path = directory_path.replace('data_from_trials', 'data_analysis_results')

        # Ensure the analysis directory exists
        os.makedirs(analysis_directory_path, exist_ok=True)

        # Define the file path for results
        result_file_path = os.path.join(analysis_directory_path, 'results.csv')
        #result_file_path=opfile
        # Check if the file exists
        if not os.path.isfile(result_file_path):
            # Create a new DataFrame with the results and write to a new CSV file
            pd.DataFrame([results_with_date]).to_csv(result_file_path, index=False)
        else:
            # If the file exists, append the new results as a new row
            pd.DataFrame([results_with_date]).to_csv(result_file_path, mode='a', header=False, index=False)

        return result_file_path