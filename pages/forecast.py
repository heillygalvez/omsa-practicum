import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown('# Predicting Future Indicators')
st.markdown("Using the data for supply and demand indicators over the last 10 years, we can make reasonable predictions of where these metrics are headed in the next few years.")
st.markdown("Academic program directors can use this interactive tool to customize predictions for hires, separations, wages, completions, and program-offering institutions.")


df = pd.read_excel("./data/employment/national_M2023_dl.xlsx", usecols=['OCC_CODE', 'H_MEDIAN', 'A_MEDIAN'])
# df[df['A_MEDIAN'] == "*"]['A_MEDIAN'] = df['H_MEDIAN'].astype("string")

df["A_MEDIAN"] = df.apply(lambda row: row["A_MEDIAN"] if row["A_MEDIAN"] != "*" else row["H_MEDIAN"] * 2080, axis=1)
df = df[df['A_MEDIAN'] != "#"]

st.dataframe(df)