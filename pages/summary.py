import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title= "EPEDS Home")

#####################################################################

header = st.container()
header.markdown("# Economic Development and Employer Planning System (EDEPS) Interactive Dashboard")
header.markdown("???")
body = st.container()
left_side, right_side = body.columns(2)

#####################################################################

left_side.markdown("## Supply Data")
left_side.markdown("???")

right_side.markdown("## Demand Data")
right_side.markdown("???")

#####################################################################

#Load supply data
cip_year = left_side.selectbox("Year", list(range(2014,2024)))

def load_completions_data(path: str, year = 2023):
    data = pd.read_csv(path+f"c{year}_a.csv", usecols=['CIPCODE','CTOTALT','UNITID'])
    return data
completions = load_completions_data("./data/completions/", cip_year)

# Total completions by CIP code
code_completions = completions.groupby(['CIPCODE'], as_index=False)['CTOTALT'].sum()
code_completions = code_completions[code_completions['CTOTALT'] < 30000] 
cip_hist_fig1 = px.histogram(code_completions, x='CTOTALT', nbins=25, title="Count of CIP codes by total completion count").update_layout(xaxis_title="")

#CIP # of institutions offering program
code_institutions = completions.groupby(['CIPCODE'], as_index=False)['UNITID'].count()
code_institutions = code_institutions[code_institutions['UNITID'] < 2000]
cip_hist_fig2 = px.histogram(code_institutions, x='UNITID', nbins=15, title="Count of CIP codes by # of Institutions").update_layout(xaxis_title="")

######################################################################

left_metrics = left_side.container()
lm1, lm2, lm3 = left_metrics.columns(3)
lm1.metric(label="Total CIP codes", value="???")
lm2.metric(label="Completions Median", value="???")
lm3.metric(label="Institutions Count Median", value="???")

left_charts = left_side.container()
lc1, lc2 = left_charts.columns(2)
lc1.plotly_chart(cip_hist_fig1, use_container_width=True)
lc2.plotly_chart(cip_hist_fig2, use_container_width=True)

#####################################################################

industry_year = right_side.selectbox("Year", list(range(2000,2026)))

#Load demand data
hires = pd.read_csv("./data/employment/hires.txt", sep="\t")

#Total hires by industry
hires_agg = hires[hires['year'] == industry_year]
hires_agg['industry_code'] = hires_agg['series_id'].str[3:9]
hires_agg = hires_agg[hires_agg['series_id'].str[-1] == "L"]
hires_agg = hires_agg.groupby(['industry_code'], as_index=False)['value'].sum()
hires_agg = hires_agg[hires_agg['value'] < 100000]
hires_hist_fig = px.histogram(hires_agg, nbins=20, x='value', title=f"Count of Industries by # of Hires").update_layout(xaxis_title="Hires")

#Total separations by industry
separations = pd.read_csv("./data/employment/separations.txt", sep="\t")
separations_agg = separations[separations['year'] == industry_year]
separations_agg.loc[:,'industry_code'] = separations_agg['series_id'].str[3:9]
separations_agg = separations_agg[separations_agg['series_id'].str[-1] == "L"]
separations_agg = separations_agg.groupby(['industry_code'], as_index=False)['value'].sum()
separations_agg = separations_agg[separations_agg['value']<100000] 
separations_hist_fig = px.histogram(separations_agg, nbins=20, x='value', title=f"Count of Industries by # of Separations").update_layout(xaxis_title="Separations")

######################################################################3

right_metrics = right_side.container()
rm1, rm2, rm3 = right_metrics.columns(3)
rm1.metric(label="Total SOC codes", value="???")
rm2.metric(label="Employment Median", value="???")
rm3.metric(label="Median Wage", value="???")

right_charts = right_side.container()
rc1, rc2 = right_charts.columns(2)
rc1.plotly_chart(hires_hist_fig, use_container_width=True)
rc2.plotly_chart(separations_hist_fig, use_container_width=True)


# TODO: Add lots of metric cards:
#'''
#  Total count of CIP codes
#  Total completions/institutions
#  Average number of completions/institutions per CIP
#  Median
#  Max number of completions and institutions
#  Min number of completions/ institutions

#  Total count of industries
#  Tocal hires/separations
#  Average
#  Median
#  Max
#  Min
# '''