import os
import pandas as pd

# Define the path to your CSV file
csv_file_path = os.path.join('./reddit_sentiment/neutrogena.csv')

# Check if the file exists
if os.path.exists(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    # Display the DataFrame
    print(df)
else:
    print(f"The file at {csv_file_path} does not exist.")
