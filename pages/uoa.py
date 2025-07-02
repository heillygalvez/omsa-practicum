import streamlit as st
import pandas as pd
import plotly.express as px

st.write("UOAs")


df = pd.read_json('./data/codes/uoa.json')

df['n_cips'] = df.apply(lambda x: len(x['cips']), axis=1)
df['n_socs'] = df.apply(lambda x: len(x['socs']), axis=1)
st.write(df)

count_cluster = px.scatter(df, x='n_cips', y="n_socs", title="# of CIPs vs # of SOCs")#.update_layout(xaxis_title="Hires")
st.plotly_chart(count_cluster, use_container_width=True)
#TODO: Show all codes in UOA with click on a dot