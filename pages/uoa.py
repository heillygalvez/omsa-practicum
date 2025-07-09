import streamlit as st
import pandas as pd
import plotly.express as px
from itertools import zip_longest


####################################################################3

top = st.container()
middle = st.container()
bottom = st.container()

top_left, top_right = top.columns(2, vertical_alignment="bottom")
middle_left, middle_right = middle.columns(2)
top_left.markdown("# Units of Analysis")
top_left.markdown("We grouped educational programs and occupations (by their CIP and SOC codes, respectively) into Units of Analysis to facilitate interaction with their supply and demand indicators.")
top_left.markdown("Interact with the table bellow by clicking on the 'UOA', 'n_cips', or 'n_socs' column headers to sort the unit sof analysis "\
                  "alphabetically, by the count of CIP codes, or by the count of SOC codes, respectively.")
top_left.markdown("When you're ready, select a unit to analyze further by chekcing the box to its left.")
####################################################################

# Load data
df = pd.read_json('./data/codes/uoa.json')

# Prep columns
df.loc[:, 'n_cips'] = df.apply(lambda x: len(x.loc['cips']), axis=1)
df.loc[:, 'n_socs'] = df.apply(lambda x: len(x.loc['socs']), axis=1)
df.loc[:, 'UOA'] = df.apply(lambda x: x.loc['socs'][0]['name'], axis=1)

# Render scatterplot of UOAs
selection = top_left.dataframe(df[['UOA', 'n_cips', 'n_socs']], selection_mode="single-row", on_select="rerun",hide_index=True)
count_scatter = px.scatter(df, x='n_cips', y="n_socs", title="CIP-to-SOC Ratios")#.update_layout(xaxis_title="Hires")
if selection.selection.rows:
    count_scatter.add_traces(
        px.scatter([df.iloc[selection.selection.rows[0], :]],  x='n_cips', y="n_socs").update_traces(marker_color="red").data
    )
top_right.plotly_chart(count_scatter, use_container_width=True)
top_right.markdown("Because we used network analysis to detect communities (in this case, units of analysis) "\
                   "that formed organically though the connection of academic programs (CIP) and occupations (SOC) "\
                    "there is a wide range of distributions for these units in terms of their ratio of CIP-to-SOC count.")
top_right.markdown("Use this relationship as another factor to consider in your data exploration by unit of analysis (UOA). "\
                   "Once you select a UOA, see it highligted in the CIP-vs-SOC plane, and see its codes in the table below.")
top_right.badge("Click on 'See UOA over Time' to learn more about historical and forecasted supply and demand indicators for the unit.")

################################################################################

# Render selection table
if selection.selection.rows:
    arr1 = [f'{cip['code']}: {cip['name']}' for cip in df.iloc[selection.selection.rows[0]]['cips']]
    arr2 = [f'{soc['code']}: {soc['name']}' for soc in df.iloc[selection.selection.rows[0]]['socs']]
    data = zip_longest(arr1, arr2)
    selection_idx = selection.selection.rows[0]
    title = df.iloc[selection_idx, :]['UOA']
    table = pd.DataFrame(data, columns=['CIP codes', 'SOC codes'])
    middle_left.markdown(f'#### {title}')
    def set_uoa():
        st.session_state.uoa = selection_idx
    if middle_right.button("See UOA over Time", on_click=set_uoa):
        st.switch_page("./pages/series.py")
    bottom.dataframe(table, hide_index=True)
