import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title= "EPEDS Home")

#####################################################################

header = st.container()
header.markdown("# Economic Development and Employer Planning System (EDEPS) Interactive Dashboard")
header.markdown("This EPEDS dashboard helps you understand available educational program (supply) and employment (demand) "\
                "data available (in this case, yearly values from 2014 to 2023 for both supply and demand), and explore values that indicate changes over time that are relevant to academic and market planing.")
body = st.container()
left_side, right_side = body.columns(2)

#####################################################################

left_side.markdown("## Supply Data")
left_side.markdown("The data summarized below comes from the Integrated Postsecondary Education Data System (IPEDS) completions data "\
                   "which reports the number of postsecondary awards (completions) according to the field of study, designated by a "\
                    "variety of demographic and institutional characteristics. For our purposes we are interested in the completions' "\
                    "Classification of Instructional Programs (CIP) code and the ID's of the institutions offering programs in such fields of study.")

right_side.markdown("## Demand Data")
right_side.markdown("???")

#####################################################################

#Load supply data
cip_year = left_side.slider("Year", min_value=2014, max_value=2023, value=2023, key="cip_year")

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
lm1.metric(label="Total CIP codes", value='{:,}'.format(code_completions['CIPCODE'].nunique()), border=True)
lm2.metric(label="Completions Median", value='{:,}'.format(code_completions['CTOTALT'].median()), border=True)
lm3.metric(label="Institutions Count Median", value='{:,}'.format(code_institutions['UNITID'].median()), border=True)

left_charts = left_side.container()
lc1, lc2 = left_charts.columns(2)
lc1.plotly_chart(cip_hist_fig1, use_container_width=True)
lc2.plotly_chart(cip_hist_fig2, use_container_width=True)

#####################################################################

industry_year = right_side.slider("Year", min_value=2014, max_value=2023, value=2023, key="industry_year")

#Load demand data

def load_employment_data(path: str, year):
    data = pd.read_excel(path+f"national_M{year}_dl.xlsx", usecols=['OCC_CODE', 'H_MEDIAN', 'A_MEDIAN', 'TOT_EMP'])
    return data
employments = load_employment_data("./data/employment/", industry_year)

# Impute annual wages with hourly
imputed_employments = employments.copy()
imputed_employments["A_MEDIAN"] = imputed_employments.apply(lambda row: row["A_MEDIAN"] if row["A_MEDIAN"] != "*" else row["H_MEDIAN"] * 2080, axis=1)
imputed_employments = imputed_employments[imputed_employments['A_MEDIAN'] != "#"]


# Total completions by CIP code
code_wages = imputed_employments.groupby(['OCC_CODE'], as_index=False)['A_MEDIAN'].mean()
soc_hist_fig1 = px.histogram(code_wages, x='A_MEDIAN', nbins=25, title="Count of SOC codes by mean wages").update_layout(xaxis_title="")

#CIP # of institutions offering program
code_employments = imputed_employments.groupby(['OCC_CODE'], as_index=False)['TOT_EMP'].sum()
soc_hist_fig2 = px.histogram(code_employments, x='TOT_EMP', nbins=15, title="Count of SOC codes by Employment Level").update_layout(xaxis_title="")


######################################################################3

right_metrics = right_side.container()
rm1, rm2, rm3 = right_metrics.columns(3)
rm1.metric(label="Total SOC codes", value="???")
rm2.metric(label="Employment Median", value="???")
rm3.metric(label="Median Wage", value="???")

right_charts = right_side.container()
rc1, rc2 = right_charts.columns(2)
rc1.plotly_chart(soc_hist_fig1, use_container_width=True)
rc2.plotly_chart(soc_hist_fig2, use_container_width=True)


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