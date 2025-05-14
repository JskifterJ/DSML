import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="EV Impact on Air Quality", layout="wide")

# Load processed data
@st.cache
def load_data():
    fleet_data = pd.read_csv("../data/processed/combined_fleet_data.csv")
    return fleet_data

data = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Dashboard", "Introduction", "EDA", "Regression Analysis", "Air Quality Predictor", "Literature Review", "Discussion", "Conclusions"])

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
    st.title("Electric Vehicles and Air Quality Analysis 🚗🌍")
    
    # Add a fun introductory GIF or image
    st.image("https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif", caption="Driving into a cleaner future!", use_column_width=True)

    st.write("""
    Welcome to the **Electric Vehicle (EV) Impact Dashboard**! 🌱🚗  
    In recent years, the adoption of electric vehicles has been heralded as a game-changer in the fight against climate change and air pollution. But how much of an impact are EVs actually having on the air we breathe?  
    This dashboard dives into the data to explore whether the promises of cleaner air and reduced emissions are being realized.
    """)

    st.subheader("Why Electric Vehicles?")
    st.write("""
    Electric vehicles (EVs) have been promoted as a sustainable alternative to traditional internal combustion engine (ICE) vehicles. By replacing gasoline and diesel with electricity, EVs aim to:
    - **Reduce greenhouse gas emissions**: EVs produce zero tailpipe emissions, helping to combat climate change.
    - **Improve urban air quality**: Cities plagued by smog and particulate matter stand to benefit from reduced vehicle emissions.
    - **Lower dependency on fossil fuels**: Transitioning to EVs aligns with global efforts to shift toward renewable energy sources.

    However, the environmental benefits of EVs depend on several factors:
    - The **energy mix** used to generate electricity (e.g., coal vs. renewables).
    - The **lifecycle emissions** of EVs, including manufacturing and battery disposal.
    - The **rate of adoption** and replacement of ICE vehicles.
    """)

    st.subheader("The Local Impact: Air Quality")
    st.write("""
    Air pollution is a major public health concern, contributing to respiratory diseases, cardiovascular issues, and premature deaths. Key pollutants include:
    - **PM2.5**: Fine particulate matter that penetrates deep into the lungs.
    - **NO₂**: Nitrogen dioxide, primarily emitted by vehicles and industrial processes.
    - **CO₂**: Carbon dioxide, a major greenhouse gas contributing to global warming.

    The adoption of EVs is expected to reduce these pollutants, especially in urban areas. But is this happening at the scale we hoped for? This dashboard explores:
    - Trends in EV adoption across countries.
    - Changes in air quality metrics over time.
    - The relationship between EV adoption and air quality improvements.
    """)

    st.subheader("What You'll Find in This Dashboard")
    st.write("""
    This dashboard is divided into several sections to guide you through the analysis:
    - **Exploratory Data Analysis (EDA)**: Visualize trends in EV adoption and air quality metrics.
    - **Regression Analysis**: Understand the statistical relationship between EV adoption and air quality.
    - **Air Quality Predictor**: Predict air quality metrics based on EV adoption levels.
    - **Literature Review**: Explore existing research on EVs and their environmental impact.
    - **Conclusions**: Summarize findings and discuss alternative explanations.

    Whether you're a policymaker, researcher, or EV enthusiast, this dashboard provides valuable insights into the real-world impact of EV adoption. Let's dive in! 🚀
    """)

    # Add a motivational GIF or image
    st.image("https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif", caption="Together, we can drive change!", use_column_width=True)


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

# Add a new section for Air Quality Predictor
elif section == "Air Quality Predictor":
    st.title("Air Quality Predictor 🚗🌍")
    st.write("Predict air quality metrics based on EV adoption levels.")

    # User inputs
    st.subheader("Input Parameters")
    country = st.selectbox("Select Country", data["Country"].unique())
    ev_percentage = st.slider("Percentage of EVs in Vehicle Fleet (%)", min_value=0, max_value=100, value=20)

    # Placeholder: Replace with actual regression model predictions
    st.subheader("Predicted Air Quality Metrics")
    st.write("Using regression results to predict air pollutant levels...")

    # Example: Mock predictions (replace with actual regression model logic)
    pollutants = ["PM2.5", "NO₂", "CO₂"]
    predictions = {pollutant: ev_percentage * 0.1 for pollutant in pollutants}  # Mock formula

    # Display predictions in a table
    st.write("Predicted Air Quality Levels:")
    prediction_df = pd.DataFrame.from_dict(predictions, orient="index", columns=["Predicted Level"])
    st.table(prediction_df)

    # Compare with 2024 statistics
    st.subheader("Comparison with 2024 Statistics")
    # Placeholder: Replace with actual 2024 data
    stats_2024 = {pollutant: 50 for pollutant in pollutants}  # Mock data
    comparison_df = pd.DataFrame({
        "Pollutant": pollutants,
        "2024 Level": [stats_2024[p] for p in pollutants],
        "Predicted Level": [predictions[p] for p in pollutants]
    })

    # Plot comparison
    st.write("Comparison Graph:")
    fig, ax = plt.subplots(figsize=(10, 6))
    comparison_df.set_index("Pollutant").plot(kind="bar", ax=ax)
    ax.set_title("Predicted vs 2024 Air Quality Levels")
    ax.set_ylabel("Level")
    st.pyplot(fig)



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


elif section == "Discussion":
    st.title("Discussion: Beyond the Dashboard 🚗📊")
    st.write("""
    While this dashboard provides valuable insights into the relationship between electric vehicle (EV) adoption and air quality, it is important to acknowledge the limitations of the analysis and explore avenues for future research. Let's dive into the nuances of what this analysis does—and does not—capture.
    """)

    st.subheader("Not a Causal Analysis")
    st.write("""
    This analysis does not establish causality between EV adoption and air quality improvements. A causal analysis would require:
    - **Far-reaching data points**: Comprehensive datasets on industrial emissions, weather patterns, and the general trajectory of emission reductions for internal combustion engine (ICE) vehicles and other sectors.
    - **Localized CO₂ propagation models**: CO₂ emissions are not confined to national borders. To isolate the impact of EV adoption within a specific country or region, we would need models that account for the transboundary movement of greenhouse gases.
    - **Temporal granularity**: High-resolution temporal data to capture short-term fluctuations and long-term trends in emissions and air quality.
    """)

    st.write("""
    Without these data points, our analysis focuses on statistical correlations and trends, which, while insightful, cannot definitively attribute changes in air quality to EV adoption alone.
    """)

    st.subheader("Upstream Emissions: The Hidden Costs")
    st.write("""
    One critical aspect not considered in this analysis is the **upstream emissions** associated with both ICE vehicles and EVs:
    - **ICE vehicles**: The extraction, refinement, and transportation of fossil fuels contribute significantly to their lifecycle emissions. These processes often have localized environmental impacts, such as oil spills and habitat destruction.
    - **EVs**: The production of EV batteries requires the extraction of rare earth elements and minerals like lithium, cobalt, and nickel. Mining these materials can lead to deforestation, water contamination, and human rights concerns in mining regions.
    """)

    st.image("https://media.giphy.com/media/3o7TKP9lnyMAk3p2yI/giphy.gif", caption="Mining for EV batteries: A hidden environmental cost?", use_column_width=True)

    st.write("""
    Future analyses could incorporate lifecycle assessments (LCAs) to provide a more holistic view of the environmental impacts of both vehicle types. LCAs would help quantify the trade-offs between tailpipe emissions and upstream emissions.
    """)

    st.subheader("Future Research Directions")
    st.write("""
    From a machine learning and data science perspective, there are several exciting opportunities for future research:
    - **Causal Inference Models**: Leveraging advanced techniques like causal forests or Bayesian networks to disentangle the effects of EV adoption from other factors influencing air quality.
    - **Spatial-Temporal Analysis**: Using geospatial data and time-series models to study localized impacts of EV adoption on air quality metrics.
    - **Integrated Energy Models**: Combining EV adoption data with energy grid models to assess the impact of renewable energy integration on lifecycle emissions.
    - **Policy Simulations**: Developing machine learning models to simulate the impact of different policy scenarios, such as subsidies for EVs or stricter emissions standards for ICE vehicles.
    """)

    st.write("""
    These approaches could provide deeper insights into the complex interplay between EV adoption, energy systems, and environmental outcomes.
    """)

    st.subheader("What We Didn't Measure")
    st.write("""
    Several important factors were beyond the scope of this analysis:
    - **Industrial Emissions**: The contribution of industries to air pollution, which can overshadow the impact of vehicle emissions in some regions.
    - **Natural Variability**: Weather patterns and seasonal changes can significantly influence air quality metrics, independent of human activity.
    - **Behavioral Shifts**: Changes in driving habits, public transportation usage, and urban planning can also affect air quality.
    """)

    st.write("""
    Incorporating these factors into future studies would provide a more comprehensive understanding of the drivers of air quality improvements.
    """)

    st.subheader("Conclusion")
    st.write("""
    While EVs hold great promise for reducing urban air pollution and greenhouse gas emissions, their environmental benefits depend on a complex web of factors, including energy grid composition, lifecycle emissions, and adoption rates. By addressing the limitations outlined above, future research can help policymakers and stakeholders make more informed decisions about the transition to sustainable transportation.
    """)

    # Add a motivational GIF or image
    st.image("https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif", caption="The road to cleaner air is a journey worth taking!", use_column_width=True)


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