import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="EV Impact on Air Quality", layout="centered")


# Load processed data
@st.cache_data
def load_data():
    fleet_data = pd.read_csv("../data/processed/combined_fleet_data.csv")
    return fleet_data

data = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Dashboard", "Introduction", "EDA", "Analysis", "Air Quality Predictor", "Literature Review", "Discussion", "Conclusions"])

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
        if st.button("Analysis"):
            st.session_state.section = "Analysis"

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
    - **Analysis**: Understand the statistical relationship between EV adoption and air quality.
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


elif section == "Analysis":
    st.title("Analysis")
    st.write("This section presents the results of cross-sectional and regression models analyzing the relationship between EV adoption and air quality.")

    st.write("""
    ## What Did We Learn?
    Our journey through data and models has revealed some fascinating insights into the relationship between electric vehicle (EV) adoption and air quality across Europe. Let's break down the highlights, the surprises, and the stories the data tells!
    """)

    st.write("""
    ## Key Findings
    - Our analysis explored the relationship between electric vehicle (EV) adoption and air quality across Europe using a variety of statistical and machine learning models.
    - We found that in some countries and for some pollutants, EV adoption is associated with measurable improvements in air quality, but the relationship is complex and varies by context.
    - The top-performing models (see tables below) show strong predictive power for certain pollutant-country combinations, while others remain challenging to model.

    ## Methodology: How Did We Find the Best Models?
    - We compared several regression models (Linear, Ridge, Lasso, Random Forest) for each pollutant and air quality metric.
    - Models were evaluated using the R² score, which measures how well the model explains the variance in the data.
    - The "best" model for each pollutant/target combination is the one with the highest R² on the test set.
    - Statistical significance is indicated with stars (*, **, ***), where available, based on conventional p-value thresholds:
        - *p* < 0.05 (*), *p* < 0.01 (**), *p* < 0.001 (***)
    - Note: Not all machine learning models provide p-values; stars are shown only where applicable (typically for linear models).
    """)

    # Load best/worst results
    import pandas as pd
    best_results = pd.read_csv("../results/best_model_per_pollutant_target.csv")
    worst_results = pd.read_csv("../results/worst_model_per_pollutant_target.csv")

    st.subheader("🏆 Top 10 Best Performing Models")
    st.write("These are the model/pollutant/metric combos with the highest R² scores—our 'super predictors'!")
    st.dataframe(best_results.head(10).style.background_gradient(cmap="Greens"))

    st.subheader("🚨 10 Worst Performing Models")
    st.write("And here are the combos where the models struggled—maybe the relationship just isn't there, or the data is too noisy!")
    st.dataframe(worst_results.head(10).style.background_gradient(cmap="Reds"))

    st.markdown("---")
    st.subheader("💡 Did You Know?")

    st.info("""
    **Choosing and Interpreting Air Quality Data is Tricky!**

    - **Negative values in air quality data** are common due to sensor noise, especially at low concentrations. These are not physically meaningful and are set to zero during cleaning. ([EPA Guidance](https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols))
    - **PM2.5 and PM10** are not just from tailpipes! While EVs reduce exhaust, heavier EVs can increase tire and road dust, and regenerative braking reduces brake dust. ([ICCT Report](https://theicct.org/publication/non-exhaust-pm-emissions-from-electric-vehicles-mar2020/))
    - **CO₂ and NO₂** are affected by much more than cars: energy production mix, industrial activity, and even weather patterns play a huge role. For example, Switzerland’s clean grid means EVs are “greener” there than in coal-heavy countries.
    - **Causality is hard:** Even if we see a correlation between EV adoption and cleaner air, it doesn’t prove EVs are the cause. Factors like improved public transport, stricter emissions standards, or economic changes can all confound the results.
    - **Data cleaning matters:** Outliers and negative values are handled carefully to avoid misleading results. See the README for details on our robust cleaning pipeline!
                                
    *“All models are wrong, but some are useful.”* — George Box

    """)

    st.markdown("---")
    st.subheader("🔍 What Did We Find?")
    # Highlight some interesting findings
    st.markdown("### 🌟 Notable Patterns")
    best = best_results.iloc[0]
    st.write(f"- **Best overall:** {best['Model']} for {best['Pollutant']} ({best['Target']}) with R² = {best['R2']:.2f}")
    st.write("- **Countries with consistently high model performance:**")
    for country in ["NO", "CH", "AT", "NL", "DK"]:
        n = best_results[best_results['Target'].str.contains(country, na=False)].shape[0]
        if n > 0:
            st.write(f"  - {country}: {n} top-10 appearances")
    st.write("- **Pollutants best explained by EV adoption:**")
    for pollutant in best_results['Pollutant'].value_counts().index[:3]:
        st.write(f"  - {pollutant}")

    # Show top 3 graphs
    st.subheader("📈 Top 3 Model Fits: See the Magic!")
    import os
    import matplotlib.pyplot as plt

    # Try to find the corresponding figure files for the top 3
    for i, row in best_results.head(3).iterrows():
        pollutant = row['Pollutant']
        target = row['Target']
        fig_path = f"../figures/analysis/{pollutant}_{target}_regression_country_fixed_effects_model_colored.png"
        st.markdown(f"**{i+1}. {pollutant} - {target} ({row['Model']}, R²={row['R2']:.2f})**")
        if os.path.exists(fig_path):
            st.image(fig_path, caption=f"{pollutant} - {target} ({row['Model']})", use_column_width=True)
        else:
            st.warning(f"Figure not found: {fig_path}")

    st.markdown("---")
    st.subheader("🤔 Alternative Explanations & Limitations")
    st.write("""
    - **Correlation ≠ Causation:** While some models fit well, remember that many factors affect air quality—weather, industry, policy, and more.
    - **Country Effects:** Some countries show strong relationships, others don't. This could be due to differences in data quality, policy, or other local factors.
    - **Pollutant Mysteries:** Some pollutants (like PM2.5) are harder to predict—maybe because they're influenced by more than just vehicles.
    - **Data Gaps:** Missing or sparse data can make even the best models stumble.
    """)
    st.info("Want to explore more? Try the Air Quality Predictor tab to see how changing EV adoption could impact air quality in your country!")

    st.markdown("#### 🚀 Thanks for exploring with us! The road to cleaner air is full of twists, turns, and data surprises.")


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


elif section == "Air Quality Predictor":
    st.title("Air Quality Predictor 🚗🌍")
    st.write("Predict air quality metrics based on EV adoption levels.")

    import streamlit as st
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.ensemble import RandomForestRegressor
    import matplotlib.pyplot as plt

    @st.cache_data
    def load_data():
        aq = pd.read_csv("../data/processed/AQ_annual_averages.csv")
        vehicle = pd.read_csv("../data/processed/combined_vehicle_data.csv")
        data = aq.merge(vehicle, on=['Country', 'Year'], how='left')
        return data

    @st.cache_data
    def load_best_results():
        return pd.read_csv("../results/best_model_per_pollutant_target.csv")

    @st.cache_resource
    def train_model(df, feature, target, model_name, country_cols):
        models = {
            "LinearRegression": LinearRegression(),
            "Ridge": Ridge(alpha=1.0),
            "Lasso": Lasso(alpha=0.1),
            "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42)
        }
        X_df = df[[feature] + country_cols]
        y = df[target]
        mask = (~X_df.isnull().any(axis=1)) & (~y.isnull())
        X = X_df[mask].values
        y = y[mask].values
        model = models[model_name]
        model.fit(X, y)
        return model, X, y, mask

    st.title("Pollutant Prediction App")

    data = load_data()
    best_results = load_best_results()

    # User selects pollutant and AnnualAvg_ column
    pollutants = best_results['Pollutant'].unique()
    pollutant = st.selectbox("Select pollutant", pollutants)

    targets = best_results[best_results['Pollutant'] == pollutant]['Target'].unique()
    target = st.selectbox("Select AnnualAvg_ column", targets)

    # Get best model for this combination
    row = best_results[(best_results['Pollutant'] == pollutant) & (best_results['Target'] == target)].iloc[0]
    model_name = row['Model']
    r2 = row['R2']

    st.write(f"Best model: **{model_name}** (R² = {r2:.2f})")

    # Filter data for pollutant and available countries
    df = data[data['Pollutant'] == pollutant].copy()
    countries = sorted(df['Country'].unique())
    country = st.selectbox("Select country", countries)

    # Prepare data for model
    df['_CountryOrig'] = df['Country']
    df = pd.get_dummies(df, columns=['Country'], drop_first=True)
    country_cols = [col for col in df.columns if col.startswith('Country_')]

    # Find the correct dummy column for the selected country
    country_dummy_map = {col.replace('Country_', ''): col for col in country_cols}
    selected_country_dummy = country_dummy_map.get(country, None)

    # User selects AF_fleet percentage
    af_fleet_min = float(df['AF_fleet'].min())
    af_fleet_max = float(df['AF_fleet'].max())
    af_fleet_default = float(df['AF_fleet'].mean())
    af_fleet = st.slider("Select AF_fleet (%)", af_fleet_min, af_fleet_max, af_fleet_default)

    # Train model (cached)
    model, X, y, mask = train_model(df, "AF_fleet", target, model_name, country_cols)

    # Prepare input for prediction
    input_vec = np.zeros((1, X.shape[1]))
    input_vec[0, 0] = af_fleet
    if selected_country_dummy:
        # Set the selected country dummy to 1, others to 0
        idx = country_cols.index(selected_country_dummy)
        input_vec[0, 1:] = 0
        input_vec[0, idx+1] = 1  # +1 because first column is AF_fleet
    else:
        # If country is the reference (first in alphabetical order), all dummies are 0
        input_vec[0, 1:] = 0

    pred = model.predict(input_vec)[0]
    st.success(f"Predicted {target} for {pollutant} in {country} at AF_fleet={af_fleet:.2f}: **{pred:.2f}**")

    # Plot predicted pollutant vs AF_fleet for the selected country
    af_fleet_range = np.linspace(af_fleet_min, af_fleet_max, 100)
    X_plot = np.zeros((100, X.shape[1]))
    X_plot[:, 0] = af_fleet_range
    if selected_country_dummy:
        X_plot[:, 1:] = 0
        X_plot[:, idx+1] = 1
    else:
        X_plot[:, 1:] = 0

    y_pred_plot = model.predict(X_plot)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(af_fleet_range, y_pred_plot, label="Predicted")
    # Scatter actual data for this country
    if selected_country_dummy:
        country_mask = df[selected_country_dummy] == 1
    else:
        # Reference country (all dummies 0)
        country_mask = df[[col for col in country_cols]].sum(axis=1) == 0
    ax.scatter(df.loc[country_mask, "AF_fleet"], df.loc[country_mask, target], color='orange', alpha=0.7, label="Actual data")
    ax.set_xlabel("AF_fleet (%)")
    ax.set_ylabel(target)
    ax.set_title(f"{target} vs AF_fleet for {pollutant} in {country}")
    ax.legend()
    st.pyplot(fig)


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