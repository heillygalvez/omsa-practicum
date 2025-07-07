import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown('# Supply and Demand Over Time')
st.markdown("As we focus on a specific Unit of Analysis, we can compare the different supply and demand indicators for the units education programs and industries/occupations.")
         
# Load uoa_todata
uoa_df = pd.read_json('./data/codes/uoa.json')

# Enable selection of one UOA
selected_uoa_index = 0
if 'uoa' in st.session_state:
    selected_uoa_index = st.session_state.uoa
uoa_indices = list(uoa_df['idx'])
uoa_names = [row['socs'][0]['name'] for _,row in uoa_df.iterrows()]
uoa = st.selectbox("Choose a Unit of Analysis", uoa_names, index=selected_uoa_index)
uoa_idx = uoa_names.index(uoa)
years = list(range(2014,2024))

# Load all completions data
@st.cache_data
def load_all_completions_data(path: str):
    data = pd.DataFrame()
    for year in years:
        df = pd.read_csv(path+f"c{year}_a.csv", usecols=['CIPCODE','CTOTALT','UNITID'])
        df['year'] = year
        data = pd.concat([data,df])
    return data
completions = load_all_completions_data("./data/completions/")

# Aggregate total completions and number of institutions
completion_sums = []
institution_counts = []
for year in years:
    cips = [obj['code'] for obj in uoa_df['cips'][uoa_idx]]
    aoi = completions[completions['CIPCODE'].isin([float(code) for code in cips])]
    aoi = aoi[aoi['year']==year]
    completion_sum = aoi['CTOTALT'].sum()
    completion_sums.append(completion_sum)
    institution_count = aoi['UNITID'].count()
    institution_counts.append(institution_count)
agg_completions = zip(years, completion_sums, institution_counts)
agg_completions_df = pd.DataFrame(agg_completions, columns=['year', 'completions', 'institutions'])
# st.dataframe(agg_completions_df)

completions_fig = px.line(agg_completions_df, x='year', y='completions')
institutions_fig = px.line(agg_completions_df, x='year', y='institutions')

st.plotly_chart(completions_fig, use_container_width=True)
st.plotly_chart(institutions_fig, use_container_width=True)

############################################################3

# Load all hire and separations data (JL series)
hires = pd.read_csv("./data/employment/hires.txt", sep="\t")
separations = pd.read_csv("./data/employment/separations.txt", sep="\t")

# Load all wage data (OE series)
@st.cache_data
def load_all_wage_data(path: str):
    data = pd.DataFrame()
    for year in years:
        df = pd.read_excel(path+f"national_M{year}_dl.xlsx", usecols=['OCC_CODE', 'H_MEDIAN', 'A_MEDIAN'])
        df['year'] = year
        data = pd.concat([data,df])
    return data
wages = load_all_wage_data("./data/employment/")
# st.dataframe(wages)

# Impute annual wages with hourly
imputed_wages = wages.copy()
imputed_wages["A_MEDIAN"] = imputed_wages.apply(lambda row: row["A_MEDIAN"] if row["A_MEDIAN"] != "*" else row["H_MEDIAN"] * 2080, axis=1)
imputed_wages = imputed_wages[imputed_wages['A_MEDIAN'] != "#"]
# st.dataframe(imputed_wages)

# Aggregate average median wage
wages_avgs = []
for year in years:
    socs = [obj['code'] for obj in uoa_df['socs'][uoa_idx]]
    aoi = wages[wages['OCC_CODE'].isin(socs)]
    aoi = aoi[aoi['year']==year]
    wages_avg = aoi['A_MEDIAN'].mean()
    wages_avgs.append(wages_avg)
agg_wages = zip(years, wages_avgs)
agg_wages_df = pd.DataFrame(agg_wages, columns=['year', 'average_annual_wage'])
st.dataframe(hires)

# Aggregare hires and separations 
# ?? 1. extract SOC from series_id, 2. group by soc and year and sum over values, 3. repeat same aoi process as with wages

wages_fig = px.line(agg_wages_df, x='year', y='average_annual_wage')

st.plotly_chart(wages_fig, use_container_width=True)

#TODO upload complete wages from website https://www.bls.gov/oes/tables.htm
# OCC_CODE, H_MEDIAN, A_MEDIAN
# Finish 2 line charts for demand. 1 with hires+ separations. One with wages.

