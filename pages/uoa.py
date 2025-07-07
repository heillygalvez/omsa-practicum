import streamlit as st
import pandas as pd
import plotly.express as px
from itertools import zip_longest

st.markdown("# Units of Analysis")
st.write("We grouped educational programs and occupations (by their CIP and SOC codes, respectively) into Units of Analysis to facilitate interaction with their supply and demand indicators.")

# Load data
df = pd.read_json('./data/codes/uoa.json')

# Prep columns
df.loc[:, 'n_cips'] = df.apply(lambda x: len(x.loc['cips']), axis=1)
df.loc[:, 'n_socs'] = df.apply(lambda x: len(x.loc['socs']), axis=1)
df.loc[:, 'UOA'] = df.apply(lambda x: x.loc['cips'][0]['name'], axis=1)

# Render scatterplot of UOAs
selection = st.dataframe(df[['UOA', 'n_cips', 'n_socs']], selection_mode="single-row", on_select="rerun",hide_index=True)
count_scatter = px.scatter(df, x='n_cips', y="n_socs", title="# of CIPs vs # of SOCs")#.update_layout(xaxis_title="Hires")
if selection.selection.rows:
    count_scatter.add_traces(
        px.scatter([df.iloc[selection.selection.rows[0], :]],  x='n_cips', y="n_socs").update_traces(marker_color="red").data
    )
st.plotly_chart(count_scatter, use_container_width=True)

# Render selection table
if selection.selection.rows:
    arr1 = [f'{cip['code']}: {cip['name']}' for cip in df.iloc[selection.selection.rows[0]]['cips']]
    arr2 = [f'{soc['code']}: {soc['name']}' for soc in df.iloc[selection.selection.rows[0]]['socs']]
    data = zip_longest(arr1, arr2)
    title = df.iloc[selection.selection.rows[0], :]['UOA']
    table = pd.DataFrame(data, columns=['CIP codes', 'SOC codes'])
    st.markdown(f'#### {title}')
    st.dataframe(table, hide_index=True)

#TODO: Make the first SOC the name of the UOA instead
#TODO: # of Completions vs # of occupations in last year (metrics, scatter, bar charts for shares)