import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Debug: Check the current working directory
print("Current Working Directory:", os.getcwd())

# Set the path to the raw data folder
data_path = "../data/raw"

# Verify if the path exists
if not os.path.exists(data_path):
    print(f"Relative path '{data_path}' not found. Using absolute path instead.")
    data_path = "c:/Users/jskif/OneDrive - epfl.ch/Documents/SMT/DSML/DSML/data/raw"

# List all CSV files in the raw data folder
csv_files = [file for file in os.listdir(data_path) if file.endswith(".csv")]

# Load all CSV files into a dictionary of DataFrames
dataframes = {}
for file in csv_files:
    country_name = file.split("_")[0]  # Extract country name from the file name
    file_path = os.path.join(data_path, file)
    dataframes[country_name] = pd.read_csv(file_path)

# Display the first few rows of each dataset
for country, df in dataframes.items():
    print(f"Dataset for {country}:")
    print(df.head(), "\n")

# Combine all datasets into a single DataFrame for easier analysis
combined_df = pd.concat(dataframes.values(), keys=dataframes.keys(), names=["Country", "Index"]).reset_index()

# Display basic information about the combined dataset
print("Combined Dataset Info:")
print(combined_df.info())

# Display summary statistics
print("\nSummary Statistics:")
print(combined_df.describe())

# Check for missing values
print("\nMissing Values:")
print(combined_df.isnull().sum())

# Save the combined dataset to the processed folder
processed_path = "../data/processed"
os.makedirs(processed_path, exist_ok=True)
combined_df.to_csv(os.path.join(processed_path, "combined_fleet_data.csv"), index=False)
print(f"Combined dataset saved to {processed_path}/combined_fleet_data.csv")