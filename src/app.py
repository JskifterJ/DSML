import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pathlib
import numpy as np
from PIL import Image
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor

# Set page configuration
st.set_page_config(page_title="EV Impact on Air Quality", layout="centered")


# Inject audio player and JS into the page
st.markdown("""
<audio id="nav-sound" src="https://www.soundjay.com/button/beep-07.mp3" preload="auto"></audio>
<script>
window.playNavSound = function() {
    const audio = document.getElementById('nav-sound');
    if (audio) {
        audio.pause();
        audio.currentTime = 0;
        audio.play().catch(e => console.log("Autoplay failed:", e));
    }
}
</script>
""", unsafe_allow_html=True)

# Wrapper to play sound
def play_sound():
    st.markdown("<script>window.playNavSound()</script>", unsafe_allow_html=True)

def switch_section(new_section):
    st.session_state["section"] = new_section

import pathlib

# Load processed data
@st.cache_data
def load_data():
    # Use pathlib to construct the file path
    data_dir = pathlib.Path(__file__).parent.parent / "data" / "processed"
    aq_data_path = data_dir / "AQ_annual_averages.csv"
    vehicle_data_path = data_dir / "combined_vehicle_data.csv" # Using the same vehicle data as Custom Regression Builder

    # Check if the files exist
    if not aq_data_path.exists():
        st.error(f"Air quality data file not found: {aq_data_path}")
        # st.stop() # Consider returning an empty DataFrame or None for more graceful handling if needed elsewhere
        return pd.DataFrame() 
    if not vehicle_data_path.exists():
        st.error(f"Vehicle data file not found: {vehicle_data_path}")
        # st.stop()
        return pd.DataFrame()

    # Load the CSV files
    aq_df = pd.read_csv(aq_data_path)
    vehicle_df = pd.read_csv(vehicle_data_path)

    # Perform the merge on 'Country' and 'Year'
    # This ensures 'Pollutant' from aq_df and fleet data from vehicle_df are combined
    merged_data = pd.merge(aq_df, vehicle_df, on=['Country', 'Year'], how='left')
    return merged_data

data = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
# Initialize session state
if "section" not in st.session_state:
    st.session_state["section"] = "Dashboard"

# Sidebar controls
section_names = [
    "Dashboard", "Introduction", "EDA", "Analysis",
    "Air Quality Predictor", "Custom Regression Builder",
    "Literature Review", "Discussion", "Conclusions"
]
selected = st.sidebar.radio(
    "Go to",
    section_names,
    index=section_names.index(st.session_state["section"]) if "section" in st.session_state else 0,
    key="sidebar_section"
)

# Update session state based on sidebar
if selected != st.session_state["section"]:
    play_sound()  # <-- Play sound before rerun
    st.session_state["section"] = selected
    st.rerun()


# Use section for routing
section = st.session_state["section"]

if "section" not in st.session_state:
    st.session_state.section = "Dashboard"

if section == "Dashboard":
    st.title("Welcome to the EV Impact Dashboard 🚗🌍")
    st.write("Navigate to different sections using the buttons below:")

    col = st.columns(1)[0]
    with col:
        if st.button("📘 Introduction"):
            play_sound()
            st.session_state["section"] = "Introduction"
            st.rerun()
        if st.button("📊 EDA"):
            play_sound()
            st.session_state["section"] = "EDA"
            st.rerun()
        if st.button("📈 Analysis"):
            play_sound()
            st.session_state["section"] = "Analysis"
            st.rerun()
        if st.button("🧪 Air Quality Predictor"):
            play_sound()
            st.session_state["section"] = "Air Quality Predictor"
            st.rerun()
        if st.button("💻 Custom Regression Builder"):
            play_sound()
            st.session_state["section"] = "Custom Regression Builder"
            st.rerun()
        if st.button("📚 Literature Review"):
            play_sound()
            st.session_state["section"] = "Literature Review"
            st.rerun()
        if st.button("🗣️ Discussion"):
            play_sound()
            st.session_state["section"] = "Discussion"
            st.rerun()
        if st.button("🔚 Conclusions"):
            play_sound()
            st.session_state["section"] = "Conclusions"
            st.rerun()

    # add a small text asking whether the user is ready!
    st.write("Are you ready to explore the impact of electric vehicles on air quality? 🚀")

    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWplZjlvYzUzNG5vNmsxcnQwb3AzNW5ycm44dTl5NzRpdjUxcGZ2aiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/AoHEeIi9AzzwLlEmfb/giphy.gif", caption="The road to cleaner air is a journey worth taking!", use_container_width =True)


elif section == "Introduction":
    st.title("Electric Vehicles and Air Quality Analysis 🚗🌍")
    
    # Add a fun introductory GIF or image
    st.image("https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif", caption="Driving into a cleaner future!", use_container_width =True)

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

    st.subheader("⚖️ Regional vs. Global Impact of EV Adoption")

    st.markdown("""
    To fully understand the environmental effects of shifting to electric and alternative fuel vehicles (AFVs), we must distinguish between **regional** and **global** impacts.

    While EVs remove local tailpipe emissions, their lifecycle still includes **upstream emissions** from energy and material sourcing.
    """)

    with st.expander("🔁 Regional Impact (Local Air Pollution)"):
        st.latex(r"""
        \text{Regional Impact} =
        E^{\text{ICE}}_{\text{tailpipe}} +
        E^{\text{non-exhaust}}_{\text{ICE}} -
        \Delta E^{\text{EV}}_{\text{tailpipe}} -
        \Delta E^{\text{EV}}_{\text{brake}} +
        \Delta E^{\text{EV}}_{\text{tire}}
        """)
        st.markdown("""
        - $E^{\\text{ICE}}_{\\text{tailpipe}}$: Local pollutants from ICE cars (CO₂, NO₂, PM)
        - $E^{\\text{non-exhaust}}_{\\text{ICE}}$: Particulate matter from brake and tire wear
        - $\\Delta E^{\\text{EV}}_{\\text{tailpipe}}$: Zero local emissions from EV tailpipes
        - $\\Delta E^{\\text{EV}}_{\\text{brake}}$: Regenerative braking reduces brake dust
        - $\\Delta E^{\\text{EV}}_{\\text{tire}}$: Heavier EVs increase tire and road dust

        📍 **Why this matters**: Not all benefits are linear. EVs clean the air we breathe, but tire-related PM may rise—especially in cities.
        """)

    with st.expander("🌍 Global Impact (Life-Cycle Emissions)"):
        st.latex(r"""
        \text{Global Impact} =
        E^{\text{fossil}}_{\text{extraction}} +
        E^{\text{EV}}_{\text{battery}} +
        E^{\text{grid}}_{\text{operation}} -
        \Delta E^{\text{ICE}}_{\text{tailpipe, lifetime}}
        """)
        st.markdown("""
        - $E^{\\text{fossil}}_{\\text{extraction}}$: Emissions from oil production, transport, and refining
        - $E^{\\text{EV}}_{\\text{battery}}$: Mining and manufacturing of EV batteries
        - $E^{\\text{grid}}_{\\text{operation}}$: Electricity generation for EV charging (energy mix critical)
        - $\\Delta E^{\\text{ICE}}_{\\text{tailpipe, lifetime}}$: Avoided lifetime emissions from displaced ICE mileage

        🌐 **Why this matters**: EVs are only as clean as the power and materials that support them. A coal-powered EV isn’t green by default.
        """)

    st.markdown("> These formulas help guide our interpretation of data across Denmark, Sweden, Norway, Netherlands, Austria, and Switzerland.")


    st.subheader("🌍 Why These Countries?")

    st.write("""
    Understanding the local impact of EV adoption requires comparing countries that are both *diverse enough to show contrast* and *similar enough for meaningful analysis*.

    We focused on six European countries that offer this balance:

    - *Norway* (🇳🇴), *Sweden* (🇸🇪), and *Denmark* (🇩🇰) are EV front-runners with supportive policies and relatively *isolated air basins*, reducing cross-border pollution noise.
    - *Switzerland* (🇨🇭) and *Austria* (🇦🇹) share *mountainous topographies* where smog and air stagnation amplify pollution patterns.
    - *The Netherlands* (🇳🇱) adds contrast with its *urban density*, flat terrain, and advanced EV infrastructure.

    All six countries are part of the *EU or EEA*, aligning on environmental regulation and data availability—while exhibiting distinct adoption rates and geography-driven pollution behaviors.

    """)

    st.markdown("#### Country Comparison Overview")
    st.write("To support this rationale, we compiled key attributes across the selected countries:")

    # Display the CSV file as a table
    import pandas as pd

    csv_path = "figures/EDA/ev_country_comparison.csv"

    if os.path.exists(csv_path):
        ev_comparison_df = pd.read_csv(csv_path)
        st.write("### EV Adoption, Geography, Policy, and Air Quality Regulation in Selected Countries")
        st.dataframe(ev_comparison_df, use_container_width=True)
    else:
        st.warning(f"CSV file not found: {csv_path}")
    

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
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2NuaTdsZXA3OHpnNmZkdzFibTlud2hxMmlxNXd0dzB3YXNpdmN4aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/VIfE4DE7vY49i/giphy.gif", caption="Together, we can drive change!", use_container_width =True)

    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        if st.button("⬅️ Previous"):
            play_sound()
            st.session_state["section"] = "Dashboard"
            st.rerun()
    with col3:
        if st.button("Next ➡️"):
            play_sound()
            st.session_state["section"] = "EDA"
            st.rerun()


elif section == "EDA":
    st.title("Exploratory Data Analysis (EDA)")
    st.write("This section explores trends in EV adoption and air quality metrics.")

    with st.expander("ℹ️ What do the AnnualAvg_ columns mean?"):
        st.markdown("""
        To help us discover patterns according to time of day and week, we created several new columns in the dataset. These columns represent annual average pollutant levels during different time periods.
        **AnnualAvg_ Column Descriptions:**
        - **AnnualAvg_fullweek_Daytime**: Average pollutant value during daytime hours (9:00–18:00), all days of the week.
        - **AnnualAvg_fullweek_RushHour**: Average pollutant value during rush hours (8:00–10:00 & 15:00–18:00), all days of the week.
        - **AnnualAvg_weekday_Daytime**: Average pollutant value during daytime hours, weekdays only (Mon–Fri).
        - **AnnualAvg_weekday_RushHour**: Average pollutant value during rush hours, weekdays only.
        - **AnnualAvg_weekend_Daytime**: Average pollutant value during daytime hours, weekends only (Sat–Sun).
        - **AnnualAvg_weekend_RushHour**: Average pollutant value during rush hours, weekends only.
        """)


    with st.expander("🧪 Pollutant Descriptions"):
        st.markdown("""
        #### Understanding the Key Air Pollutants

        Air quality is influenced by various pollutants, each with unique sources and health impacts. Here's what we're tracking:

        - 🟢 **CO₂ (Carbon Dioxide)**  
        - **Source**: Internal combustion engine (ICE) fuel combustion.  
        - **Notes**: Not directly toxic at ambient levels, but a key greenhouse gas driving climate change.  
        - **Confounders**: Also produced by industry and heating systems. Cannot be reduced by EVs unless power generation is clean.

        - 🟠 **NO₂ (Nitrogen Dioxide)**  
        - **Source**: High-temperature combustion in ICE vehicles (especially diesel engines).  
        - **Health Risk**: Irritates lungs, exacerbates asthma, especially dangerous for children and elderly.  
        - **Confounders**: Also emitted by industrial processes and heating.

        - 🔵 **NO (Nitric Oxide)**  
        - **Source**: Immediate product of combustion, especially in traffic-heavy areas.  
        - **Reaction**: Converts rapidly to NO₂ in the atmosphere.  
        - **Notes**: Monitored as a proxy for recent vehicle emissions.

        - 🟣 **NOₓ (Nitrogen Oxides)**  
        - **Definition**: Combined NO + NO₂, often reported as “NOₓ as NO₂”.  
        - **Source**: Mostly traffic emissions, especially diesel vehicles.  
        - **Importance**: A regulatory metric for urban air quality assessments.

        - ⚫ **PM2.5 (Fine Particulate Matter <2.5µm)**  
        - **Source**: Combustion in ICE vehicles, but also **non-exhaust** sources like **brake dust, tire wear, and road abrasion**.  
        - **Health Risk**: Penetrates deep into lungs and bloodstream; linked to respiratory and cardiovascular diseases.  
        - **EV Factor**: Regenerative braking reduces brake dust, but battery weight may increase tire and road wear PM.

        - ⚪ **PM10 (Coarse Particulate Matter <10µm)**  
        - **Source**: Larger particles from **tire wear, road dust, and mechanical abrasion**.  
        - **EV Factor**: Heavier vehicles (like BEVs) tend to increase PM10 from tire-road interactions.  
        - **Confounders**: Also influenced by construction, agriculture, and weather (wind re-suspension).

        
        ---
        **Note**: Non-tailpipe (non-exhaust) emissions like tire and brake wear are increasingly relevant with the rise of EVs. These sources do not benefit from the "zero emissions" of EV drivetrains and may even increase in some cases.

        To interpret trends responsibly, both **vehicle type** and **driving patterns** must be considered in context of these emissions.
        """)


    # ensure the EDA directory is loaded
    BASE_DIR = pathlib.Path(__file__).parent.parent  # DSML/
    EDA_DIR = BASE_DIR / "figures" / "EDA"


    # --- IMPROVED: Show static EDA figures from ../figures/EDA with descriptions ---
    st.subheader("Air Quality & Fleet EDA Visualizations")
    st.write("Explore the following visualizations to understand the relationship between EV adoption and air quality metrics.")
    st.write("Click on the images to view them in full size.")
    st.write("Note: Only figures present in the folder will be shown.")

    BASE_DIR = pathlib.Path(__file__).parent.parent  # DSML/
    EDA_DIR = BASE_DIR / "figures" / "EDA"

    st.subheader("📈 Fleet Composition and Adoption Trends")
    st.write("This section analyzes trends in fleet composition across six European countries, focusing on BEV, PHEV, and AF vehicle penetration and registration dynamics.")

    eda_figures = [
        ("Distribution of Plug-in Hybrid Electric Vehicles (PHEV) Across Countries", "figures/EDA/AF_distribution_per_country.png", 
        "🔹 Norway and Sweden have the highest spread and median share of PHEVs, while Switzerland and Luxembourg show lower variability and median levels. This highlights more mature hybrid markets in Nordic regions."),

        ("Trends in Battery Electric Vehicles (BEV) Over Time", "figures/EDA/AF_fleet_per_country_timeseries.png", 
        "🔹 Norway leads the BEV transition with exponential growth post-2016. Other countries show steady but slower uptake, likely tied to infrastructure and incentives."),

        ("Market Share of Alternative Fuel Vehicles by Country", "figures/EDA/market_share_by_country.png", 
        "🔹 Norway stands out with high interquartile range (IQR), indicating a broad and growing adoption. The rest show tighter distributions, with Austria, Switzerland, and Denmark trailing."),

        ("Distribution of New Registrations by Country", "figures/EDA/new_registrations_by_country.png", 
        "🔹 Norway and the Netherlands show high variability and volume in alternative fuel vehicle registrations, suggesting rapid market change and policy responsiveness."),

        ("Development of Alternative Fuel New Registrations Over Time", "figures/EDA/new_registrations_over_time.png", 
        "🔹 All countries exhibit accelerating registration trends post-2018, with especially steep climbs in the Netherlands, Sweden, and Norway. This aligns with EU and national decarbonization targets.")
    ]

    for caption, path, insight in eda_figures:
        if os.path.exists(path):
            st.image(path, caption=caption, use_container_width =True)
            st.markdown(f"**Insight:** {insight}")
        else:
            st.warning(f"Figure not found: {path}")

    st.markdown("---")
    st.subheader("🧠 Fleet Composition Takeaways")
    st.markdown("""
    - **Norway** consistently leads across BEV and PHEV metrics, reflecting its aggressive incentive structure and clean grid.
    - **Nordic countries (NO, SE)** show higher PHEV diversity, while **CH, AT, DK** follow with lagging adoption and more modest trends.
    - **Recent acceleration in AF new registrations** across all countries signals a potential inflection point driven by policy or infrastructure readiness.
    - These fleet dynamics set the foundation for analyzing their relationship to air quality metrics in subsequent sections.
    """)


    st.subheader("🌫️ Air Quality Trends and Patterns")
    st.write("This section explores trends in pollutant levels across time and space, using data from national monitoring stations. Patterns in key metrics (CO₂, NO₂, PM) provide insight into evolving air quality amid the shift toward alternative fuel vehicles.")

    aq_figures = [
        ("CO2 Levels (Full Week Daytime) Over Years by Country", "figures/EDA/aq_avg_annual_co2_per_country.png",
        "🔹 CO₂ levels are generally increasing in AT, DK, and CH, while NO and SE show flatter or even declining trends. Norway’s persistently low CO₂ supports the impact of its clean grid."),

        ("Average Annual Pollutant Levels Over Time (All Countries)", "figures/EDA/aq_avg_annual_pollutant_over_time.png",
        "🔹 NO₂, PM2.5, and PM10 show a clear declining trend over the past decade, suggesting overall air quality improvement. However, CO₂ has been rising slightly, likely reflecting energy mix and mobility demand."),

        ("Annual Pollutant Trends by Country", "figures/EDA/aq_avg_annual_pollutant_over_time_per_country.png",
        "🔹 The decline in NO₂ and NOₓ is widespread across countries. PM trends are more erratic, likely due to local non-exhaust sources. CO₂ remains higher in Austria and Denmark."),

        ("Hourly Pattern by Pollutant (Average Across Countries)", "figures/EDA/aq_hourly_pattern_per_pollutant.png",
        "🔹 Most pollutants show strong peaks during rush hours (around 8–9 AM and 4–6 PM), aligning with commuter traffic. CO₂ and NO₂ are especially tied to these patterns."),

        ("Hourly Pattern by Pollutant and Country", "figures/EDA/aq_hourly_pattern_per_pollutant_per_country.png",
        "🔹 Across countries, Norway and Sweden generally show lower hourly concentrations. Peaks in CO₂ and NO₂ confirm vehicular traffic’s central role in local pollution."),

        ("Number of Unique Air Quality Stations per Country", "figures/EDA/station_density_map.png",
        "🔹 Austria and Sweden have the most dense monitoring networks. Switzerland has fewer stations, which may introduce spatial sampling bias in national aggregates.")
    ]

    aq_figures.extend([
        
        ("Average Weekday Daytime Pollution Levels by Country and Pollutant", "figures/EDA/aq_heatmap_weekdaydaytime.png",
        "🔹 Daytime pollution levels are highest for CO₂ and PM2.5 in Austria, Denmark and Norway."),

        ("Average Weekday Daytime Pollution Levels (Rush Hour)", "figures/EDA/aq_heatmap_weekdayrushhour.png",
        "🔹 Rush Hour pollution levels display subtle shifts with NO2 and PM2.5 levels slightly increasing in nost countries."),

        ("Average Difference Between Weekday Daytime and Rush Hour Levels", "figures/EDA/aq_difference_heatmaps.png",
        "🔹 Rush hour peaks are most pronounced in Austria and Norway, highlighting the impact of commuter traffic. Switzerland shows a slight decline during rush hours."),

        ("Correlation Heatmaps by Country", "figures/EDA/aq_correlation_heatmaps.png",
        "🔹 Correlation heatmaps reveal strong relationships between NO₂, NOₓ, and PM pollutants across countries. CO₂ shows weaker correlations, reflecting its broader energy-related sources."),

        ("Seasonal Patterns in Pollutant Levels by Country", "figures/EDA/aq_seasonal_patterns_per_country.png",
        "🔹 Pollutant levels vary seasonally, with winter showing higher concentrations for most pollutants. This reflects seasonal heating and meteorological effects."),

    ])


    for caption, path, insight in aq_figures:
        if os.path.exists(path):
            st.image(path, caption=caption, use_container_width=True)
            st.markdown(f"**Insight:** {insight}")
        else:
            st.warning(f"Figure not found: {path}")

    st.markdown("---")
    st.subheader("🧠 Air Quality Takeaways")
    st.markdown("""
    - **Pollutants from combustion (NO, NO₂, NOₓ)** are decreasing steadily, reflecting improved vehicle standards and rising EV penetration.
    - **Particulate matter (PM2.5, PM10)** shows more variation, as it is also influenced by **non-exhaust sources** like tires and brakes—less responsive to EV trends.
    - **Hourly patterns** strongly align with traffic cycles, supporting transportation as a dominant emission source in urban areas.
    - **Country differences** reflect both technological shifts and structural factors (energy mix, urban planning, industrial activity).
    """)

    st.info("More detailed EDA and interactive plots can be found in the project notebooks.")

    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        if st.button("⬅️ Previous"):
            play_sound()            
            st.session_state["section"] = "Introduction"
            st.rerun()
    with col3:
        if st.button("Next ➡️"):
            play_sound()
            st.session_state["section"] = "Analysis"
            st.rerun()


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
    import pathlib
    best_results_path = pathlib.Path(__file__).parent.parent / "results" / "best_model_per_pollutant_target.csv"
    if not best_results_path.exists():
        st.error(f"File not found: {best_results_path}")
        st.stop()
    best_results = pd.read_csv(best_results_path)    

    worst_results_path = pathlib.Path(__file__).parent.parent / "results" / "worst_model_per_pollutant_target.csv"
    if not worst_results_path.exists():
        st.error(f"File not found: {worst_results_path}")
        st.stop()
    worst_results = pd.read_csv(worst_results_path)  
    

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

    # --- Section: Model Results per Pollutant ---
    st.subheader("📊 Model Results per Pollutant")
    st.markdown("To interpret model performance across pollutants and countries, we focus on the *full week rush-hour* timescale. This view maximizes clarity, captures consistent time windows most impacted by traffic, and highlights inter-country variation in model fit.")
    st.markdown("*Note*: Country fixed effects applied to OLS, Ridge, and Lasso models to account for country-specific factors. Austria (AT) is used as the reference country hence it doesn't show in the plots.")

    # Helper function to display image and bullet points
    def show_model_analysis(pollutant_name, bullet_points):
        import pathlib
        BASE_DIR = pathlib.Path(__file__).parent.parent  # DSML/
        analysis_dir = BASE_DIR / "figures" / "analysis"
        image_path = analysis_dir / f"{pollutant_name}_AnnualAvg_fullweek_RushHour_regression_country_fixed_effects_model_colored.png"
        if image_path.exists():
            st.image(str(image_path), caption=f"Regression results for {pollutant_name}")
        else:
            st.warning(f"Figure not found for {pollutant_name}")
        st.markdown("\n".join([f"- {pt}" for pt in bullet_points]))


    st.subheader("CO2")
    # --- 🟢 CO2 ---
    show_model_analysis("CO2", [
        "The Netherlands and Sweden show a high model fit across all methods, suggesting strong internal consistency in how fleet composition aligns with CO₂ levels.",
        "Switzerland and Norway display low predictive performance, hinting at potential missing variables or measurement discrepancies in their CO₂ reporting.",
        "Random Forest performs best overall, capturing more of the nonlinear variance, especially in countries like Austria (R² = 0.71)."
    ])

    st.subheader("NO")
    # ---🟠 NO2 ---
    show_model_analysis("NO2", [
        "Model fits are consistently strong in Austria, Switzerland, and the Netherlands, suggesting stable relationships in NO₂ emissions and fleet data.",
        "Random Forest shows the strongest generalization, particularly for SE and CH where test R² approaches 1.0.",
        "DK again appears as a difficult case for modeling, though NO₂ performs better than other pollutants."
    ])

    st.subheader("NOX as NO2")
    # ---🟣 NOX as NO2 ---
    show_model_analysis("NOX as NO2", [
        "The Netherlands is again a standout, with high test R² across all models.",
        "Norway and Austria show moderate predictive power with test R² around 0.3 to 0.6, indicating partial but not robust signal capture.",
        "For Sweden, even non-linear models struggle to predict NOx levels, which could point to external factors beyond EV share."
    ])

    st.subheader("PM10")
    # ---⚪ PM10 ---
    show_model_analysis("PM10", [
        "Strongest fits appear in the Netherlands and Switzerland, suggesting a clear structural link between alternative fuel uptake and PM10 levels in these regions.",
        "Austria shows moderate test scores, while countries like DK and NO present greater difficulty in capturing patterns, possibly due to data variability or local factors."
    ])

    st.subheader("PM2.5")
    # ---⚫ PM2.5 ---
    show_model_analysis("PM2.5", [
        "The highest test scores across pollutants are seen here, especially for Switzerland and Sweden, where Random Forest reaches near-perfect R².",
        "Austria and Norway also show reliable performance, suggesting PM2.5 may be the most consistently modelled pollutant in relation to fleet share.",
        "This consistency across countries may reflect the relatively uniform impact of vehicle emissions on fine particulate matter.",
    ])


    st.markdown("---")
    st.subheader("🤔 Alternative Explanations & Limitations")
    st.write("""
    - **Correlation ≠ Causation:** While some models fit well, remember that many factors affect air quality—weather, industry, policy, and more.
    - **Country Effects:** Some countries show strong relationships, others don't. This could be due to differences in data quality, policy, or other local factors.
    - **Pollutant Mysteries:** Some pollutants (like PM2.5) are harder to predict—maybe because they're influenced by more than just vehicles.
    - **Data Gaps:** Missing or sparse data can make even the best models stumble.
    """)
    st.info("Want to explore more? Try the Air Quality Predictor tab to see how changing EV adoption could impact air quality in your country!")


    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        if st.button("⬅️ Previous"):
            play_sound()
            st.session_state["section"] = "EDA"
            st.rerun()
    with col3:
        if st.button("Next ➡️"):
            play_sound()
            st.session_state["section"] = "Literature Review"
            st.rerun()


elif section == "Air Quality Predictor":
    @st.cache_resource
    def train_model(df_train, feature_col, target_col, model_name_to_train, country_dummy_cols):
        models = {
            "LinearRegression": LinearRegression(), # OLS
            "Ridge": Ridge(alpha=1.0),
            "Lasso": Lasso(alpha=0.1),
            "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        # Ensure feature_col is a list, even if it's a single feature
        if isinstance(feature_col, str):
            feature_col = [feature_col]
            
        X_df = df_train[feature_col + country_dummy_cols]
        y_series = df_train[target_col]
        
        # Create mask for valid data
        mask_train = (~X_df.isnull().any(axis=1)) & (~y_series.isnull())
        
        X_train_np = X_df[mask_train].values
        y_train_np = y_series[mask_train].values
        
        if X_train_np.shape[0] == 0: # No data to train on
            st.warning("No valid data available for training with the current selections.")
            # Return a dummy model or handle appropriately
            return models[model_name_to_train], X_train_np, y_train_np, mask_train 

        model_instance = models[model_name_to_train]
        model_instance.fit(X_train_np, y_train_np)
        return model_instance, X_train_np, y_train_np, mask_train

    st.title("🔬 Air Quality Predictor")
    st.markdown("""
    Experiment with different models to predict pollutant levels based on Alternative Fuel (AF) vehicle fleet percentage. 
    You can view predictions for individual countries or use a model trained on all countries with fixed effects (Austria as baseline).
    """)

    data = load_data() # Assuming this loads your base dataset
    # Assuming best_results is loaded globally or passed appropriately
    # For this example, let's ensure it's available. If it's loaded in main(), pass it or load here.
    # if 'best_results' not in globals(): # Simplified check
    results_path = pathlib.Path(__file__).parent.parent / "results"
    best_results = pd.read_csv(results_path / "best_model_per_pollutant_target.csv")

    # --- User Selections ---
    pollutants_available = sorted(best_results['Pollutant'].unique())
    pollutant = st.selectbox("1. Select Pollutant", pollutants_available, key="predictor_pollutant")

    targets_available = sorted(best_results[best_results['Pollutant'] == pollutant]['Target'].unique())
    if not targets_available: # Fallback if no targets for pollutant
        st.warning(f"No target variables found for pollutant {pollutant} in best_results.csv. Please check data.")
        st.stop()
    target = st.selectbox("2. Select Target Variable (e.g., Annual Average)", targets_available, key="predictor_target")

    use_all_countries = st.checkbox("🌍 Use model trained on all countries' data (with fixed effects, AT as baseline)", key="predictor_use_all")

    model_options = ["LinearRegression", "Ridge", "Lasso", "RandomForest"]
    default_model_idx = model_options.index("LinearRegression") # Default to OLS
    
    selected_model_by_user = st.selectbox("3. Select Model Type", model_options, index=default_model_idx, key="predictor_model_select")

    actual_model_to_run = ""
    
    if use_all_countries:
        st.info("ℹ️ Model trained on all countries. 'LinearRegression' (OLS with fixed effects) will be used. Individual country selection below is for plotting context only.")
        actual_model_to_run = "LinearRegression"
    else:
        actual_model_to_run = selected_model_by_user
        try:
            # Display info about the pre-calculated best model for context
            best_row = best_results[
                (best_results['Pollutant'] == pollutant) &
                (best_results['Target'] == target)
            ].iloc[0]
            st.info(f"ℹ️ For {pollutant} ({target.split('_')[-1]}), the pre-calculated best model in analyses was **{best_row['Model']}** (Training R² = {best_row['R2_train']:.2f}). You are currently experimenting with **{actual_model_to_run}**.")
        except IndexError:
            st.info(f"ℹ️ No pre-calculated 'best model' info for {pollutant} ({target.split('_')[-1]}). You are experimenting with **{actual_model_to_run}**.")

    # --- Data Preparation ---
    df_filtered_pollutant = data[data['Pollutant'] == pollutant].copy()
    df_filtered_pollutant['_CountryOrig'] = df_filtered_pollutant['Country']
    
    # Create country dummies, using Austria (AT) as baseline if present
    # Ensure 'AT' is treated as baseline by not creating a dummy for it if drop_first is smart
    # Or explicitly handle AT if it's not automatically the baseline from get_dummies
    if 'AT' in df_filtered_pollutant['Country'].unique():
        df_prepared = pd.get_dummies(df_filtered_pollutant, columns=['Country'], prefix='Country', prefix_sep='_', drop_first=True)
    else: # If AT is not in data for this pollutant, drop the first alphabetically
        df_prepared = pd.get_dummies(df_filtered_pollutant, columns=['Country'], prefix='Country', prefix_sep='_', drop_first=True)
        st.warning("Austria (AT) not found in the data for the selected pollutant; another country was used as baseline for dummies.")

    country_cols = [col for col in df_prepared.columns if col.startswith('Country_')]

    # --- Country selection for individual view (if not use_all_countries) or plot context ---
    selected_country_for_view = None
    selected_country_dummy_for_input = None # For constructing prediction input vector

    # Always show country dropdown for plot context, but its role in model input changes
    available_countries_for_pollutant = sorted(df_filtered_pollutant['_CountryOrig'].unique())
    if available_countries_for_pollutant:
        country_for_plot_context = st.selectbox("4. Select Country for Plot Context / Individual Prediction", available_countries_for_pollutant, key="predictor_country_select")
        selected_country_for_view = country_for_plot_context
        if f"Country_{country_for_plot_context}" in country_cols:
             selected_country_dummy_for_input = f"Country_{country_for_plot_context}"
        # If country_for_plot_context is the baseline (e.g., AT), selected_country_dummy_for_input will be None
    else:
        st.warning("No countries available for the selected pollutant.")
        st.stop()

    # --- AF Fleet Slider ---
    af_fleet_min = 0.0
    af_fleet_max = 100.0
    # Use mean of the specific pollutant's data if available, else a general default
    default_af_fleet = df_prepared['AF_fleet'].mean() if not df_prepared['AF_fleet'].empty else 20.0
    af_fleet_percentage = st.slider("5. Select Alternative Fuel (AF) Fleet Percentage (%) for Prediction", af_fleet_min, af_fleet_max, default_af_fleet, key="predictor_af_slider")

    # --- Model Training & Evaluation ---
    trained_model, X_trained_np, y_trained_np, training_mask = train_model(df_prepared, "AF_fleet", target, actual_model_to_run, country_cols)

    if X_trained_np.shape[0] > 0:
        current_model_r2 = trained_model.score(X_trained_np, y_trained_np)
        st.markdown(f"##### Performance of **{actual_model_to_run}** (Your Current Selection):")
        st.metric(label="Training R² on current data subset", value=f"{current_model_r2:.3f}")
    else:
        st.warning("Model could not be trained due to lack of valid data for current selections.")
        st.stop()

    # --- Prediction ---
    # X_trained_np columns: AF_fleet, then country dummies in order of country_cols
    num_features_model_expects = 1 + len(country_cols) 
    input_vec = np.zeros((1, num_features_model_expects))
    input_vec[0, 0] = af_fleet_percentage  # AF_fleet is the first feature

    if not use_all_countries: # Prediction for a specific country
        if selected_country_dummy_for_input: # A non-baseline country is selected
            try:
                dummy_idx = country_cols.index(selected_country_dummy_for_input)
                input_vec[0, 1 + dummy_idx] = 1 # +1 because AF_fleet is at index 0
            except ValueError:
                 st.error(f"Error: Dummy column {selected_country_dummy_for_input} not found. This should not happen.")
        # Else (baseline country like AT is selected for view), all dummies remain 0, which is correct.
    # Else (use_all_countries is True):
    #   The prediction will be for the baseline country (AT) by default, as all dummies are 0.
    #   If user selected a different country in "country_for_plot_context", we can set its dummy for the point prediction.
    elif use_all_countries and selected_country_dummy_for_input: # if a specific country context is chosen even with all_countries model
        try:
            dummy_idx = country_cols.index(selected_country_dummy_for_input)
            input_vec[0, 1 + dummy_idx] = 1
        except ValueError:
            pass # Keep as baseline if dummy not found

    predicted_value = trained_model.predict(input_vec)[0]
    predicted_value = max(predicted_value, 0) # Clip at 0

    st.success(f"Predicted **{target}** for **{selected_country_for_view if selected_country_for_view else 'Baseline Country (e.g. AT)'}** at {af_fleet_percentage:.1f}% AF Fleet: **{predicted_value:.2f}**")

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Prediction line (trend for the selected country context)
    af_fleet_range_plot = np.linspace(df_prepared['AF_fleet'].min(), df_prepared['AF_fleet'].max(), 100)
    X_plot_trend = np.zeros((100, num_features_model_expects))
    X_plot_trend[:, 0] = af_fleet_range_plot
    
    # Set country dummy for the trend line based on selected_country_dummy_for_input
    # This makes the trend line specific to the country selected in "country_for_plot_context"
    if selected_country_dummy_for_input:
        try:
            dummy_idx_plot = country_cols.index(selected_country_dummy_for_input)
            X_plot_trend[:, 1 + dummy_idx_plot] = 1
        except ValueError:
            pass # Plot baseline trend if dummy not found
            
    y_pred_plot_trend = trained_model.predict(X_plot_trend)
    y_pred_plot_trend = np.clip(y_pred_plot_trend, 0, None)
    ax.plot(af_fleet_range_plot, y_pred_plot_trend, label=f"Predicted Trend ({selected_country_for_view if selected_country_for_view else 'Baseline'})", color='blue', linestyle='--')

    # Scatter actual data points
    df_plot_actuals = df_prepared[training_mask] # Use only data points that were valid for training

    if not use_all_countries: # Show data only for the selected country
        if selected_country_dummy_for_input: # Non-baseline country
            country_actual_mask = df_plot_actuals[selected_country_dummy_for_input] == 1
        else: # Baseline country (e.g., AT)
            country_actual_mask = df_plot_actuals[country_cols].sum(axis=1) == 0
        ax.scatter(df_plot_actuals.loc[country_actual_mask, "AF_fleet"], df_plot_actuals.loc[country_actual_mask, target], color='orange', alpha=0.6, label=f"Actual Data ({selected_country_for_view})")
    else: # Show all data points (from all countries included in training)
        ax.scatter(df_plot_actuals["AF_fleet"], df_plot_actuals[target], color='gray', alpha=0.4, label="Actual Data (All Countries in Model)")
        # Optionally, highlight data for the country selected for context
        if selected_country_for_view:
            if selected_country_dummy_for_input: # Non-baseline
                 country_context_mask = df_plot_actuals[selected_country_dummy_for_input] == 1
            else: # Baseline
                 country_context_mask = df_plot_actuals[country_cols].sum(axis=1) == 0
            ax.scatter(df_plot_actuals.loc[country_context_mask, "AF_fleet"], df_plot_actuals.loc[country_context_mask, target], color='red', alpha=0.7, label=f"Actual Data ({selected_country_for_view})", s=50)


    # Highlight the specific prediction point
    ax.scatter([af_fleet_percentage], [predicted_value], color='red', s=100, edgecolor='black', zorder=5, label=f"Prediction for {selected_country_for_view if selected_country_for_view else 'Baseline'}")
    ax.annotate(f"{predicted_value:.2f}", (af_fleet_percentage, predicted_value), textcoords="offset points", xytext=(0,10), ha='center', color='red', fontsize=9, fontweight='bold')

    ax.set_xlabel("Alternative Fuel (AF) Fleet Percentage (%)")
    ax.set_ylabel(f"{pollutant} - {target}")
    ax.set_title(f"Prediction: {actual_model_to_run} Model")
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.7)
    st.pyplot(fig)



    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        if st.button("⬅️ Previous"):
            st.session_state["section"] = "Literature Review"
            st.rerun()
    with col3:
        if st.button("Next ➡️"):
            play_sound()
            st.session_state["section"] = "Custom Regression Builder"
            st.rerun()


elif section == "Custom Regression Builder":
    st.title("🔬 Custom Regression Builder")
    st.markdown(
        "This regression includes **country fixed effects** (dummy variables for each country, with Austria (AT) as the baseline). "
        "This approach helps control for unobserved country-level differences and improves the reliability of OLS, Ridge, and Lasso models."
    )

    import pathlib
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.ensemble import RandomForestRegressor

    # Robust data import (relative to project root)
    DATA_DIR = pathlib.Path(__file__).parent.parent / "data" / "processed"
    aq = pd.read_csv(DATA_DIR / "AQ_annual_averages.csv")
    vehicle = pd.read_csv(DATA_DIR / "combined_vehicle_data.csv")
    data = aq.merge(vehicle, on=['Country', 'Year'], how='left')

    # --- User selects pollutant and which AnnualAvg_ column to use ---
    pollutants = sorted(data['Pollutant'].dropna().unique())
    pollutant = st.selectbox("Select pollutant (dependent variable)", pollutants)

    # Find all AnnualAvg_ columns available for this pollutant
    annualavg_cols = [col for col in data.columns if col.startswith("AnnualAvg_")]
    default_col = annualavg_cols[0] if annualavg_cols else None
    y_col = st.selectbox("Select annual average column", annualavg_cols, index=annualavg_cols.index(default_col) if default_col else 0)

    # Filter data for selected pollutant
    df = data[data['Pollutant'] == pollutant].copy()

    # Country filter
    countries = sorted(df['Country'].unique())
    selected_countries = st.multiselect("Select countries", countries, default=countries)

    # X variable selection (exclude non-numeric/object columns and country dummies)
    x_vars = st.multiselect(
        "Select independent variables (X)",
        [col for col in df.columns if col not in ["Country", "Year", "Pollutant", y_col] and df[col].dtype != "object"],
        default=["AF_fleet"]
    )

    # Model selection
    model_type = st.selectbox("Select model type", ["Linear Regression", "Ridge", "Lasso", "Random Forest"])
    if model_type == "Ridge":
        alpha = st.slider("Ridge alpha", 0.01, 10.0, 1.0)
    if model_type == "Lasso":
        alpha = st.slider("Lasso alpha", 0.01, 10.0, 0.1)
    if model_type == "Random Forest":
        n_estimators = st.slider("Number of trees", 10, 200, 100, step=10)

    # Filter data
    df = df[df['Country'].isin(selected_countries)].dropna(subset=[y_col] + x_vars + ["Country"])

    # Add country fixed effects (AT as baseline)
    if "AT" in df['Country'].unique():
        df = pd.get_dummies(df, columns=['Country'], drop_first=True)
        country_dummies = [col for col in df.columns if col.startswith("Country_")]
    else:
        # If AT not present, use first country alphabetically as baseline
        df = pd.get_dummies(df, columns=['Country'], drop_first=True)
        country_dummies = [col for col in df.columns if col.startswith("Country_")]

    # Only add country dummies for OLS, Ridge, Lasso
    if model_type in ["Linear Regression", "Ridge", "Lasso"]:
        X = df[x_vars + country_dummies]
    else:
        X = df[x_vars]
    y = df[y_col]

    if len(df) > 5 and x_vars:
        # Model fitting
        if model_type == "Linear Regression":
            model = LinearRegression()
        elif model_type == "Ridge":
            model = Ridge(alpha=alpha)
        elif model_type == "Lasso":
            model = Lasso(alpha=alpha)
        elif model_type == "Random Forest":
            model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
        model.fit(X, y)
        y_pred = model.predict(X)
        r2 = model.score(X, y)
        st.write(f"**R²:** {r2:.3f}")
        if hasattr(model, "coef_"):
            st.write("**Coefficients:**")
            coef_dict = dict(zip(X.columns, model.coef_))
            st.json(coef_dict)
        if hasattr(model, "intercept_"):
            st.write("**Intercept:**", model.intercept_)
        # Plot actual vs predicted
        fig, ax = plt.subplots()
        ax.scatter(y, y_pred, alpha=0.7)
        ax.plot([y.min(), y.max()], [y.min(), y.max()], "r--")
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        ax.set_title(f"Actual vs Predicted for {pollutant} ({y_col})")
        st.pyplot(fig)
    else:
        st.info("Select at least one X variable and enough data.")

    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        if st.button("⬅️ Previous"):
            play_sound()
            st.session_state["section"] = "Air Quality Predictor"
            st.rerun()
    with col3:
        if st.button("Next ➡️"):
            play_sound()
            st.session_state["section"] = "Discussion"
            st.rerun()

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


    # Study 3
    st.subheader("Study 3: Borge et al. (2016)")
    st.write("""
    **Goal:** Assess the impact of electric vehicle (EV) adoption on air pollution levels along a major highway in Madrid, Spain.
    """)
    st.write("""
    **Findings:**
    - Replacing 50% of light-duty vehicles with EVs could reduce nitrogen dioxide (NO₂) and nitrogen oxides (NOₓ) concentrations by approximately 5.5% in areas adjacent to the highway.
    - The study emphasizes that while EVs can contribute to air quality improvements, the overall impact is modest and depends on the extent of EV adoption and other local factors.
    - No significant CO₂ reductions are reported, as the focus is primarily on local pollutants.
    """)
    st.write("[Read more](https://doi.org/10.1016/j.apenergy.2016.03.027)")

    # Study 4
    st.subheader("Study 4: Requia et al. (2016)")
    st.write("""
    **Goal:** Evaluate the episodic impacts of plug-in electric vehicle (PEV) adoption on air quality and public health in the United States.
    """)
    st.write("""
    **Findings:**
    - PEV adoption leads to notable reductions in ozone (O₃) and fine particulate matter (PM₂.₅) during high pollution episodes, especially in urban areas.
    - Air quality improvements are region-specific, with the largest benefits in densely populated, high-emission zones.
    - Public health gains include reduced respiratory and cardiovascular issues, with potential decreases in mortality rates.
    - The effectiveness of EVs in improving air quality depends heavily on the electricity generation mix—regions with cleaner grids show the strongest benefits.
    """)
    st.write("[Read more](https://doi.org/10.1016/j.atmosenv.2016.07.005)")


    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        if st.button("⬅️ Previous"):
            play_sound()
            st.session_state["section"] = "Analysis"
            st.rerun()
    with col3:
        if st.button("Next ➡️"):
            play_sound()
            st.session_state["section"] = "Air Quality Predictor"
            st.rerun()


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

    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXQxbTBmMTRsOGtxM2ZxbGFoc2dkanY5aWM4YnFrMXNzdGM2djRuMiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/282FVV3gOTojMwgcDm/giphy.gif", caption="Mining for EV batteries: A hidden environmental cost?", use_container_width =True)


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


    # Add a motivational GIF or image
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWloOWNlazZ6eDVzaG91M2F4YTRxaDd4enhlZnBiMXQxaHI2d2M5dCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Vfhj19PusenfO/giphy.gif", caption="The road to cleaner air is a journey worth taking!", use_container_width =True)

    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        if st.button("⬅️ Previous"):
            play_sound()
            st.session_state["section"] = "Custom Regression Builder"
            st.rerun()
    with col3:
        if st.button("Next ➡️"):
            play_sound()
            st.session_state["section"] = "Conclusions"
            st.rerun()


elif section == "Conclusions":
    st.title("Conclusions: The Road Ahead 🚗🌍")
    st.subheader("🧠 Main Takeaways: What Did We Learn?")
    st.markdown("""
    - **EV adoption shows localized but non-uniform links to improved air quality**, especially for pollutants like **NO₂** and **PM2.5**, which are closely tied to traffic emissions.
    
    - **Carbon dioxide (CO₂) trends are harder to explain** with EV data alone, likely due to energy production, industry, and transboundary effects—underscoring the complexity of global emissions accounting.
    
    - **Random Forest models capture complex relationships best**, highlighting the potential of non-linear machine learning for environmental modeling.
   
     - **Country-specific dynamics matter**: Strong relationships were seen in countries like the Netherlands and Sweden, while others (e.g., Norway, Switzerland) had lower predictive performance, likely due to external confounding factors.
    
    - **Correlation ≠ causation**: Our models reveal patterns, but we cannot say definitively that EVs caused these changes—structural and behavioral factors remain critical.
    """)

    st.image("https://media.giphy.com/media/xTiTnHXbRoaZ1B1Mo8/giphy.gif", caption="The road ahead: data-powered and cleaner 🌱", use_container_width=True)

    st.subheader("🚀 Next Actionable Moves")
    st.markdown("""
    - **Deploy Causal Inference Techniques**: Beyond the scope of this project, the obvious next step would be to extend the project by implementing **causal inference models** (e.g., difference-in-differences, instrumental variables, or causal forests) to better isolate the effect of EV adoption from co-occurring factors like policy changes or economic shifts.
   
    - **Integrate Geospatial and High-Resolution Temporal Data**:By incorporating **satellite-based pollution data** and **hourly monitoring station feeds**, we would could better isolate the effects of **short-term spikes** and **urban microclimates**, improving the spatial accuracy of our predictions.
    
    - **Merge with Grid and Energy Mix Data**:To bridge regional and global impacts, we could link EV adoption with **electric grid data and lifecycle emission factors**, evaluating whether “clean” EVs truly displace emissions or simply shift them upstream.
    
    - **Simulate Policy Scenarios**:Equipped with robust econometrics-based models, one would try to **simulate hypothetical policy changes** such as EV subsidies or ICE vehicle bans to evaluate their projected impact on different pollutants.
    """)

    st.subheader("🧠 What we Learned")
    st.markdown("""
    - **Version Control with GitHub:** We became much more comfortable using Git and GitHub for collaboration, including resolving merge conflicts, managing branches, and using pull requests to review and integrate code changes.
    - **Debugging and Troubleshooting:** We learned to systematically debug code, interpret error messages, and use tools like Stack Overflow and official documentation to resolve issues—especially when dealing with tricky file paths and Streamlit reruns.
    - **Repository Management:** We encountered and overcame GitHub storage and file size restrictions, learning to use `.gitignore` and LFS effectively and keep our repository clean by avoiding the upload of large data files and generated figures.
    - **Environment & Dependency Management:** Setting up and maintaining a consistent development environment (using `environment.yml` and `requirements.txt`) was crucial for reproducibility and collaboration throughout the project.
    - **Documentation:** We saw firsthand the value of clear README files, code comments, and structured folder organization for both our own workflow and for future users of our codebase.
    - **Teamwork and Fun!:** Apart from the technical sides, we learned just how important it is to stay aligned on process and codebase structure, and made sure to push the boundaries of what we could do with Streamlit and GitHub Actions, emphasizing having fun and breaking things rather than being too conservative :)!

    These lessons will serve us well in future data science projects, both academic and professional!    
    """)

    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmgwa3RmcDgzbXQ3MTMwNmxxNTF6Z2I0NmZrbzhmMDEya3d4cHp4MCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/5C472t1RGNuq4/giphy.gif", caption="Alas, we move forward!", use_container_width=True)

    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        if st.button("⬅️ Previous"):
            play_sound()
            st.session_state["section"] = "Discussion"
            st.rerun()