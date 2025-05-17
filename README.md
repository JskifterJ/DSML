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

Notes: 
<<<<<<< HEAD
- while one could run the models based on transport-specific data, this data is merely a proxy for the average fuel consumption per kilometer of the transport fleet. With increasing adoption of Alternative Fuels (AF) vehicles in the fleet, this number will obviously be directled correlated with the change in emission factors such as CO2 and NO. Further, this would neglect the emissions of electricity production mix which BEV and PHEV vehicles require, thus severely graying the true picture of regional emission-data corresponding to passenger car emissions. 
- we chose to include PM factors due to the how most BEV and PHEV vehicles brake exclusively with regenerative braking which thus produces less brake dust. On the other hand, the heavy nature of especially BEV's due to battery weight may cause increased dispersion of tire particulate matter. It is important to realize these considerations when interpreting results.
- 

2. Handling Negative and Outlier Values in Air Quality Data
Air quality measurement devices, especially those used for pollutants like PM2.5, PM10, NO2, NO, and CO2, are inherently noisy—particularly at low concentrations. This noise, combined with instrument calibration drift, baseline corrections, and data averaging, can result in negative values or extreme outliers in the recorded data. Negative concentrations are not physically meaningful and are artifacts of the measurement process.

To ensure robust analysis:

Negative values are set to zero, as they do not represent real-world pollutant concentrations.
Outliers are detected using the Interquartile Range (IQR) method and are replaced with NaN values. This helps prevent extreme, likely erroneous values from skewing statistical analyses and visualizations.
This cleaning step is essential for producing reliable insights from environmental monitoring data and is a standard practice in air quality data science.
=======
- while one could run the models based on transport-specific data, this data is merely a proxy for the average fuel consumption per kilometer of the transport fleet. With increasing adoption of Alternative Fuels (AF) vehicles in the fleet, this number will obviously be directled correlated with the change in emission factors such as CO2 and NO.
- we chose to include PM factors due to the how most BEV and PHEV vehicles brake exclusively with regenerative braking which thus produces less brake dust. On the other hand, the heavy nature of especially BEV's due to battery weight may cause increased dispersion of tire particulate matter. It is important to realize these considerations when interpreting results.
- 
>>>>>>> 7b944fe99b6af9b4e568af4f01df7a9e7c1cc3d2
