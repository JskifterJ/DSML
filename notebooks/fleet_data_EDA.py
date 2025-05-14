import pandas as pd
import os

# Debug: Check the current working directory
print("Current Working Directory:", os.getcwd())

# Set the path to the raw data folder
data_path = "../data/raw/fleet_data"  # Relative path to the raw data folder

# Verify if the path exists
if not os.path.exists(data_path):
    print(f"Relative path '{data_path}' not found. Using absolute path instead.")
    data_path = "c:/Users/jskif/OneDrive - epfl.ch/Documents/SMT/DSML/DSML/data/raw"

# List all CSV files in the raw data folder
csv_files = [file for file in os.listdir(data_path) if file.endswith(".csv")]

# Initialize dictionaries to store DataFrames for each file type
newreg_dataframes = {}
eu_dataframes = {}
registrations_dataframes = {}

# Process files based on their type
for file in csv_files:
    country_name = file.split("_")[0]  # Extract country name from the file name
    file_path = os.path.join(data_path, file)

    if file.endswith("newreg.csv"):
        newreg_dataframes[country_name] = pd.read_csv(file_path)
    elif file.endswith("EU.csv"):
        eu_dataframes[country_name] = pd.read_csv(file_path)
    elif file.endswith("registrations.csv"):
        registrations_dataframes[country_name] = pd.read_csv(file_path)

# Combine datasets for each file type
combined_newreg_df = pd.concat(newreg_dataframes.values(), keys=newreg_dataframes.keys(), names=["Country", "Index"]).reset_index()
combined_eu_df = pd.concat(eu_dataframes.values(), keys=eu_dataframes.keys(), names=["Country", "Index"]).reset_index()
combined_registrations_df = pd.concat(registrations_dataframes.values(), keys=registrations_dataframes.keys(), names=["Country", "Index"]).reset_index()

# Display basic information about the combined datasets
print("Combined New Registrations Dataset Info:")
print(combined_newreg_df.info())

print("\nCombined EU Dataset Info:")
print(combined_eu_df.info())

print("\nCombined Registrations Dataset Info:")
print(combined_registrations_df.info())

# Save the combined datasets to the processed folder
processed_path = "../data/processed"
os.makedirs(processed_path, exist_ok=True)

combined_newreg_df.to_csv(os.path.join(processed_path, "combined_newreg_data.csv"), index=False)
combined_eu_df.to_csv(os.path.join(processed_path, "combined_eu_data.csv"), index=False)
combined_registrations_df.to_csv(os.path.join(processed_path, "combined_registrations_data.csv"), index=False)

print(f"Combined datasets saved to {processed_path}/")