import streamlit as st
import pandas as pd
import plotly.express as px

# Load JSON data (relative path)
df = pd.read_json("dataset.json")
df.columns = df.columns.str.strip()  # remove extra spaces

# ------------------------------
# PAGE SETUP
# ------------------------------
st.set_page_config(
    page_title="Premier League Player Stats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# SIDEBAR FILTERS
# ------------------------------
st.sidebar.header("Filters")

# Statistic selection
stat_options = {
    "Goals": "Goals",
    "Assists": "Assists",
    "Age": "Age",
    "Appearances": "Appearances",
    "Wins": "Wins",
    "Losses": "Losses",
    "Goals per match": "Goals per match",
    "Shots": "Shots",
    "Shots on target": "Shots on target",
    "Shooting accuracy %": "Shooting accuracy %"
}
stat_friendly = st.sidebar.selectbox("Choose a statistic to visualize:", list(stat_options.keys()))
stat_column = stat_options[stat_friendly]

# ------------------------------
# AGE SLIDER (full dataset range)
# ------------------------------
full_min_age, full_max_age = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider(
    "Select Age Range:",
    min_value=full_min_age,
    max_value=full_max_age,
    value=(full_min_age, full_max_age)
)

# ------------------------------
# NATIONALITY FILTER
# ------------------------------
nationalities = ["All"] + sorted(df["Nationality"].dropna().unique().tolist())
selected_nationality = st.sidebar.selectbox("Filter by Nationality:", nationalities)

# ------------------------------
# APPLY FILTERS
# ------------------------------
filtered_df = df[(df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])]
if selected_nationality != "All":
    filtered_df = filtered_df[filtered_df["Nationality"] == selected_nationality]

# ------------------------------
# HEADER AND KEY METRICS
# ------------------------------
st.title("Premier League Player Stats Dashboard")
st.markdown("Explore player statistics interactively with filters and charts.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Players Displayed", len(filtered_df))
col2.metric("Average Goals", round(filtered_df["Goals"].mean(), 2))
col3.metric("Average Assists", round(filtered_df["Assists"].mean(), 2))
col4.metric("Average Appearances", round(filtered_df["Appearances"].mean(), 2))

# ------------------------------
# TOP 5 PLAYERS
# ------------------------------
st.subheader(f"Top 5 Players by {stat_friendly}")
top5 = filtered_df.nlargest(5, stat_column)[["Name", "Club", "Nationality", stat_column]]
st.dataframe(top5)

# ------------------------------
# TABS FOR VISUALIZATIONS
# ------------------------------
tab1, tab2, tab3 = st.tabs(["Bar Chart", "Scatter Plot", "Data Table"])

with tab1:
    st.subheader(f"{stat_friendly} Visualization")
    fig_bar = px.bar(
        filtered_df,
        x="Name",
        y=stat_column,
        color="Nationality",
        title=f"{stat_friendly} of Players",
        hover_data=["Age", "Club", "Position"],
        height=500
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    fig_scatter = px.scatter(
        filtered_df,
        x="Age",
        y=stat_column,
        color="Nationality",
        size="Appearances",
        hover_data=["Name", "Club", "Position"],
        height=500
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.subheader("Player Data Table")
    st.dataframe(filtered_df.reset_index(drop=True))
