import streamlit as st
import pandas as pd
import plotly.express as px
from itertools import cycle, chain

st.markdown('# Units of Analysis over the Years')
st.write("We grouped educational programs and occupations (by their CIP and SOC codes, respectively) into Units of Analysis to facilitate interaction with their supply and demand indicators.")

# Load uoa_todata
uoa_df = pd.read_json('./data/codes/uoa.json')

# Enable selection of one UOA
uoa_indices = list(uoa_df['idx'])
uoa_names = [row['socs'][0]['name'] for _,row in uoa_df.iterrows()]
uoa = st.selectbox("Choose a Unit of Analysis", uoa_names, index=40) #TODO: use navigation parameters
years = list(range(2014,2024))

# Load all completions data
@st.cache_data
def load_all_completions_data(path: str):
    data = pd.DataFrame()
    for year in years:
        df = pd.read_csv(path+f"c{year}_a.csv")
        df = df[['CIPCODE','CTOTALT','UNITID']]
        df['year'] = year
        data = pd.concat([data,df])
    return data
completions = load_all_completions_data("./data/completions/")

# Aggregate total completions and number of institutions
completion_sums = []
institution_counts = []
for year in years:
    uoa_idx = uoa_names.index(uoa)
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

#goal
hires = pd.read_csv("./data/employment/hires.txt", sep="\t")
separations = pd.read_csv("./data/employment/separations.txt", sep="\t")
wages = pd.read_csv("./data/employment/oe_data_1_AllData.txt", sep="\t")
wages = wages[wages['series_id'].str[-2:]=="17"] #Select only Annual median wage values
st.dataframe(wages.tail())

#TODO upload complete wages from website https://www.bls.gov/oes/tables.htm
# Finish 2 line charts for demand. 1 with hires+ separations. One with wages.

