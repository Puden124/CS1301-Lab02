# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---

with open("Lab02/data.json", "r") as file:
    data = json.load(file)

df = pd.DataFrame.from_dict(data, orient="index")

fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(df.index, df["peak_24h"])

ax.set_title("Steam Games by 24-Hour Peak Players")
ax.set_xlabel("Game")
ax.set_ylabel("Concurrent Players")

plt.xticks(rotation=90)

ax.ticklabel_format(style="plain", axis="y")


st.pyplot(fig)

st.subheader("Steam Game Popularity")

if "selection" not in st.session_state:
    st.session_state.selection = "peak_24h"

selection = st.selectbox(
    "Choose a statistic",
    ["peak_24h", "peak_all_time"],
    index=["peak_24h", "peak_all_time"].index(st.session_state.selection)
)

st.session_state.selection = selection

fig2, ax2 = plt.subplots()

ax2.pie(df[selection], labels=df.index)

ax2.set_title("Steam Game Popularity")

st.pyplot(fig2)



# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---

st.header("Gaming Survey Results")

csv_df = pd.read_csv("Lab02/data.csv")

if not csv_df.empty:
    csv_df["Value"] = pd.to_numeric(csv_df["Value"], errors="coerce")
    csv_df = csv_df.dropna(subset=["Value"])

    if not csv_df.empty:
        # Bar Chart

        st.subheader("Average Gaming Hours by Genre")

        averages = csv_df.groupby("Category")["Value"].mean()

        fig3, ax3 = plt.subplots()

        ax3.bar(averages.index, averages.values)
        ax3.set_title("Average Weekly Gaming Hours")
        ax3.set_xlabel("Game Genre")
        ax3.set_ylabel("Hours per Week")

        st.pyplot(fig3)

        # Scatter Plot
        st.subheader("Gaming Hours Survey")

        if "max_hours" not in st.session_state:
            st.session_state.max_hours = int(csv_df["Value"].max())

        maximum = max(1, int(csv_df["Value"].max()))

        limit = st.slider(
            "Maximum weekly gaming hours",
            min_value=0,
            max_value=maximum,
            value=min(st.session_state.max_hours, maximum)
        )

        st.session_state.max_hours = limit

        filtered_df = csv_df[csv_df["Value"] <= limit]

        
        # EXTRA CREDIT: MEAN AND MEDIAN

        # Calculate the mean and median of the filtered data
        if not filtered_df.empty:
            current_mean = filtered_df["Value"].mean()
            current_median = filtered_df["Value"].median()
        else:
            current_mean = 0
            current_median = 0

        # Store previous values using session state
        if "previous_mean" not in st.session_state:
            st.session_state.previous_mean = current_mean

        if "previous_median" not in st.session_state:
            st.session_state.previous_median = current_median

        # Calculate how much the statistics changed
        mean_change = current_mean - st.session_state.previous_mean
        median_change = current_median - st.session_state.previous_median

        # Display metrics side by side
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Average Gaming Hours",
                value=f"{current_mean:.2f}",
                delta=f"{mean_change:+.2f}"
            )

        with col2:
            st.metric(
                label="Median Gaming Hours",
                value=f"{current_median:.2f}",
                delta=f"{median_change:+.2f}"
            )

        # Save current values for the next interaction
        st.session_state.previous_mean = current_mean
        st.session_state.previous_median = current_median


        fig4, ax4 = plt.subplots()

        ax4.scatter(
            filtered_df["Category"],
            filtered_df["Value"]
        )

        ax4.set_title("Gaming Hours by Genre")
        ax4.set_xlabel("Game Genre")
        ax4.set_ylabel("Hours per Week")

        st.pyplot(fig4)
    else:
        st.warning("No valid numeric survey responses yet.")
else:
    st.info("Submit survey responses to see the graphs.")
