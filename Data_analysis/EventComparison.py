import os
import pandas as pd
import numpy as np

# Function to process the DataFrame and create a list of sets of events for each trial
def process_events(df):
    # Group by 'Trial Number' and aggregate events into a list
    grouped = df.groupby('Trial Number')['Event'].apply(list)
    # Convert lists to sets for similarity comparison
    event_sets = grouped.apply(set)
    return event_sets

# Function to calculate Jaccard similarity score for two sets
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# Function to load a CSV file into a DataFrame
def load_csv(file_path):
    return pd.read_csv(file_path)

# Main function to calculate Jaccard scores between a specific CSV and all others in the folder
def compare_with_all(latest_csv_path, directory):
    # Load the specified CSV into a DataFrame
    latest_df = load_csv(latest_csv_path)

    # Process the event data for the specified CSV
    latest_event_sets = process_events(latest_df)

    # Store Jaccard scores
    jaccard_scores = {}

    # Loop through all CSV files in the directory
    for csv_file in os.listdir(directory):
        file_path = os.path.join(directory, csv_file)
        if csv_file.endswith('.csv') and file_path != latest_csv_path:
            # Load the CSV file into a DataFrame
            current_df = load_csv(file_path)

            # Process the event data
            current_event_sets = process_events(current_df)

            # Calculate the minimum common number of trials
            min_trials = min(len(latest_event_sets), len(current_event_sets))

            # Calculate Jaccard similarity score for each trial
            scores = [jaccard_similarity(latest_event_sets[i], current_event_sets[i]) for i in range(min_trials)]

            # Average the Jaccard scores to get an overall similarity score
            average_score = np.mean(scores)

            # Store the average score with the filename
            jaccard_scores[csv_file] = average_score

    return jaccard_scores

# Path to the latest CSV file
directory= 'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/COMPUTER_COMPUTER/event_data_from_trials/'

# Directory containing the other CSV files
latest_csv_path = 'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/MOUSE_COMPUTER/1775/event_data_from_trials/20240123_105302.csv'

# Compare the latest CSV with all others and get the Jaccard scores
scores = compare_with_all(latest_csv_path, directory)

# Output the Jaccard scores
for file, score in scores.items():
    print(f"Average Jaccard similarity score for {file}: {score}")
