
import streamlit as st
import pandas as pd
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE
st.title("Gaming Survey 📝")
st.write("Fill out the survey to contribute to our gaming dataset.")

# DATA INPUT FORM
with st.form("survey_form"):
    category_input = st.text_input("What game genre do you play?")
    value_input = st.text_input("How many hours do you play per week?")

    submitted = st.form_submit_button("Submit Data")

    if submitted:
        if category_input.strip() != "" and value_input.strip() != "":
            try:
                value = float(value_input)

                new_data = pd.DataFrame({
                    "Category": [category_input.strip()],
                    "Value": [value]
                })

                file_exists = os.path.exists("Lab02/data.csv")
                file_empty = not file_exists or os.path.getsize("Lab02/data.csv") == 0

                new_data.to_csv(
                    "Lab02/data.csv",
                    mode="a",
                    header=file_empty,
                    index=False
                )

                st.success("Your data has been submitted!")
                st.write(
                    f"You entered: **Category:** {category_input}, "
                    f"**Value:** {value}"
                )

            except ValueError:
                st.error("Please enter a valid number for gaming hours.")
        else:
            st.warning("Please fill out both fields.")

# DATA DISPLAY
st.divider()
st.header("Current Data in CSV")

if os.path.exists("Lab02/data.csv") and os.path.getsize("Lab02/data.csv") > 0:
    current_data_df = pd.read_csv("Lab02/data.csv")
    st.dataframe(current_data_df)
else:
    st.warning("The data.csv file is empty or does not exist yet.")
