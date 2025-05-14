import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="EV Impact on Air Quality", layout="wide")

# Load processed data
@st.cache.data
def load_data():
    fleet_data = pd.read_csv("../data/processed/combined_fleet_data.csv")
    return fleet_data

data = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Dashboard", "Introduction", "EDA", "Regression Analysis", "Literature Review", "Conclusions"])

# Dashboard page
if section == "Dashboard":
    st.title("Welcome to the EV Impact Dashboard 🚗🌍")
    st.write("Navigate to different sections of the analysis using the buttons below:")

    # Create a grid layout with buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Introduction"):
            st.session_state.section = "Introduction"
    with col2:
        if st.button("EDA"):
            st.session_state.section = "EDA"
    with col3:
        if st.button("Regression Analysis"):
            st.session_state.section = "Regression Analysis"

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("Literature Review"):
            st.session_state.section = "Literature Review"
    with col5:
        if st.button("Conclusions"):
            st.session_state.section = "Conclusions"

    st.write("Use the sidebar to navigate as well!")

# Conditional logic for other sections
elif section == "Introduction":
    st.title("Electric Vehicles and Air Quality Analysis")
    st.write("""
    This dashboard presents the findings of our investigation into whether the adoption of electric vehicles (EVs) has led to measurable improvements in air quality.
    """)
    st.write("""
    **Objectives:**
    - Analyze trends in EV adoption and air quality metrics.
    - Evaluate the relationship between EV adoption and air quality using statistical methods.
    - Present findings and discuss alternative explanations.
    """)

elif section == "EDA":
    st.title("Exploratory Data Analysis (EDA)")
    st.write("This section explores trends in EV adoption and air quality metrics.")

    # EV Adoption Trends
    st.subheader("EV Adoption Trends")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=data, x="Category", y="BEV", hue="Country", ax=ax)
    ax.set_title("Battery Electric Vehicle (BEV) Trends Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("BEV Proportion")
    st.pyplot(fig)

    # Air Quality Trends (Placeholder for future data)
    st.subheader("Air Quality Trends")
    st.write("Air quality data visualizations will be added here.")

elif section == "Regression Analysis":
    st.title("Regression Analysis")
    st.write("This section presents the results of regression models analyzing the relationship between EV adoption and air quality.")

    # Placeholder for regression results
    st.write("Regression results will be displayed here.")

elif section == "Literature Review":
    st.title("Literature Review")
    st.write("""
    This section explores existing research on the environmental impacts of electric vehicle (EV) adoption and compares their findings with our analysis.
    """)

    # Study 1
    st.subheader("Study 1: Gómez Vilchez et al. (2019)")
    st.write("""
    **Goal:** Quantify key environmental impacts of electric vehicle deployment in the European Union by 2030.
    """)
    st.write("""
    **Findings:**
    - Simulated CO2 emission reductions are modest, with only two countries (Austria and Ireland) reducing CO2 emissions by more than 10%.
    - Positive correlation between higher EV stock deployment and greater CO2 mitigation.
    - Switzerland benefits from lower PM2.5 concentrations due to EV uptake in neighboring countries.
    """)
    st.write("[Read more](https://doi.org/10.1186/s12544-019-0377-1)")

    # Study 2
    st.subheader("Study 2: Weeberb J. Requia et al. (2018)")
    st.write("""
    **Goal:** Comprehensive review of the effects of EV adoption on air quality, greenhouse gas emissions, and human health.
    """)
    st.write("""
    **Findings:**
    - The main bottleneck is that air pollution shifts from roads to power plants.
    - Pollution reduction benefits depend on EV lifecycle emissions and the energy mix used for electricity generation.
    """)
    st.write("[Read more](https://doi.org/10.1016/j.atmosenv.2018.04.040)")

    # Discussion
    st.subheader("Discussion")
    st.write("""
    These studies highlight the complexity of assessing the environmental benefits of EV adoption. While there are clear benefits in reducing road-level emissions, the overall impact depends on factors such as:
    - The energy mix used for electricity generation.
    - Lifecycle emissions of EVs, including manufacturing and disposal.
    - Regional differences in air quality and EV adoption rates.

    Our analysis builds on these findings by focusing on specific countries (e.g., Switzerland, Norway) and examining the relationship between EV adoption and air quality metrics over time.
    """)

elif section == "Conclusions":
    st.title("Conclusions and Alternative Explanations")
    st.write("""
    **Key Findings:**
    - Summarize the main findings from the analysis.
    - Discuss whether EV adoption has significantly impacted air quality.

    **Alternative Explanations:**
    - Consider other factors that may influence air quality (e.g., industrial emissions, weather patterns).
    - Highlight limitations of the analysis.
    """)