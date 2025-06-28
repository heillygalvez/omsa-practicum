import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Raw Data")


st.markdown("Completions")
st.markdown("## Distribution of CIP codes")
cip_year = st.selectbox("Year", list(range(2014,2024)))
def load_completions_data(path: str, year = 2023):
    data = pd.read_csv(path+f"c{year}_a.csv")
    data = data[['CIPCODE','CTOTALT','UNITID']]
    return data
completions = load_completions_data("./data/completions/", cip_year)

cip_agg = st.radio(
    "Choose metric to aggregate",
    ["total completion count", "number of institutions with program"]
)
cip_hist_fig = None
#1.1 Histogram of all CIP completions
if cip_agg == "total completion count":
    code_completions = completions.groupby(['CIPCODE'], as_index=False)['CTOTALT'].sum()
    code_completions = code_completions[code_completions['CTOTALT'] < 30000] 
    cip_hist_fig = px.histogram(code_completions, x='CTOTALT', nbins=25, title="Count of CIP codes by total completion count").update_layout(xaxis_title="")

#1.2 CIP # of institutions offering program
if cip_agg == "number of institutions with program":
    code_institutions = completions.groupby(['CIPCODE'], as_index=False)['UNITID'].count()
    code_institutions = code_institutions[code_institutions['UNITID'] < 2000]
    cip_hist_fig = px.histogram(code_institutions, x='UNITID', nbins=15, title="Count of CIP codes by # of Institutions").update_layout(xaxis_title="")
st.plotly_chart(cip_hist_fig, use_container_width=True)