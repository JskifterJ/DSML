# DSML
Lesgooo 🔥🚀🚀


# Electric Vehicles and Air Quality Analysis

## Project Overview
This project investigates the impact of electric vehicle (EV) adoption on air quality, focusing primarily on Switzerland. Through data analysis and statistical evaluation, we aim to determine whether there is measurable evidence supporting the claim that EVs significantly improve air quality.

## Objectives
- Collect and analyze historical data on EV sales and air quality metrics.
- Perform trend analysis to examine the relationship between EV adoption and air quality indicators (e.g., PM2.5, NO₂, CO₂).
- Use statistical and machine learning techniques to evaluate the significance of observed changes.
- Present findings through a Streamlit app and visualizations.

## Folder Structure
DSML/
├── data/                     # Folder for raw and processed data
│   ├── raw/                  # Raw data files
│   └── processed/            # Processed/cleaned data files
├── notebooks/                # Jupyter notebooks for exploratory data analysis (EDA)
├── src/                      # Source code for the project
│   ├── data_processing.py    # Scripts for data cleaning and preprocessing
│   ├── analysis.py           # Scripts for statistical and machine learning analysis
│   ├── visualization.py      # Scripts for generating visualizations
│   └── app.py                # Streamlit app entry point
├── tests/                    # Unit tests for your code
├── figures/                  # Folder for saving figures/graphs
├── docs/                     # Documentation and references
├── README.md                 # Project overview and instructions
├── requirements.txt          # Python dependencies
├── environment.yml           # Conda environment configuration
└── .gitignore                # Files and folders to ignore in Git

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/JskifterJ/DSML.git
   cd DSML

Create and activate the Conda environment:
conda env create -f environment.yml
conda activate dsml_EV_project

Install additional dependencies (if needed):
pip install -r requirements.txt

Run the Streamlit app:
streamlit run src/app.py