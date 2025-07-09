import streamlit as st
import pandas as pd
import plotly.express as px

c1 = st.container()
l1, r1 = c1.columns([0.8,0.2], vertical_alignment="center")
c2 = st.container()
c2.markdown("## Supply Indicators in Time")

l2, m2, r2 = c2.columns([0.35, 0.35, 0.3], vertical_alignment="center")
c3 = st.container()
c3.markdown("## Demand Indicators in Time")

l3, m3, r3 = c3.columns([0.35, 0.35,0.3], vertical_alignment="center")

l1.markdown('# Supply and Demand Over the Years')
l1.markdown("As we focus on a specific Unit of Analysis, "\
            "we can compare the different supply (total number of completions and number of institutions offering programs) and demand (total employment levels and average mean wages across the unit) indicators for the selected "\
            "unit of analysis' education programs and industries/occupations.")

##############################################################################33         
# Load uoa_todata
uoa_df = pd.read_json('./data/codes/uoa.json')

# Enable selection of one UOA
selected_uoa_index = 0
if 'uoa' in st.session_state:
    selected_uoa_index = st.session_state.uoa
uoa_indices = list(uoa_df['idx'])
uoa_names = [row['socs'][0]['name'] for _,row in uoa_df.iterrows()]
uoa = r1.selectbox("Choose a Unit of Analysis", uoa_names, index=selected_uoa_index)
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

completions_fig = px.line(agg_completions_df, x='year', y='completions')
institutions_fig = px.line(agg_completions_df, x='year', y='institutions')

############################################################3

# Load all wage data (OE series)
@st.cache_data
def load_all_wage_data(path: str):
    data = pd.DataFrame()
    for year in years:
        df = pd.read_excel(path+f"national_M{year}_dl.xlsx", usecols=['OCC_CODE', 'H_MEDIAN', 'A_MEDIAN', 'TOT_EMP'])
        df['year'] = year
        data = pd.concat([data,df])
    return data
wages = load_all_wage_data("./data/employment/")

# Impute annual wages with hourly
imputed_wages = wages.copy()
imputed_wages["A_MEDIAN"] = imputed_wages.apply(lambda row: row["A_MEDIAN"] if row["A_MEDIAN"] != "*" else row["H_MEDIAN"] * 2080, axis=1)
imputed_wages = imputed_wages[imputed_wages['A_MEDIAN'] != "#"]

# Aggregate average median wage
wages_avgs = []
tot_emp_sums = []
for year in years:
    socs = [obj['code'] for obj in uoa_df['socs'][uoa_idx]]
    aoi = wages[wages['OCC_CODE'].isin(socs)]
    aoi = aoi[aoi['year']==year]
    wages_avg = aoi['A_MEDIAN'].mean()
    wages_avgs.append(wages_avg)
    tot_emp_sum = aoi['TOT_EMP'].sum()
    tot_emp_sums.append(tot_emp_sum)
agg_emps = zip(years, wages_avgs, tot_emp_sums)
agg_emps_df = pd.DataFrame(agg_emps, columns=['year', 'average_annual_wage', 'total_national_employment'])

##############################################################################

# Moving average forecasts
window = r1.slider("Choose a window (# of years):", min_value=2, max_value=5, value=3)

def get_predictions(df, columns):
    predictions = []
    for col in columns:
        y =df[col]
        last_year = list(df['year'])[-1]
        future_xs = list(range(last_year,last_year+window+1)) 
        future_ys = [list(y)[-1]]
        for _ in range(window):
            y_pred = list(y.rolling(window=window).mean())
            y = list(y)
            future_ys.append(y_pred[-1])
            y.append(y_pred[-1])
            y = pd.Series(y)
        predictions.append(future_ys)
    new_rows = zip(future_xs, *predictions)
    return pd.DataFrame(new_rows, columns=df.columns)

###########################################################################

# Make predictions
completions_preds_df = get_predictions(agg_completions_df, ['completions', 'institutions'])
completions_preds_df.loc[:,'obs_pred'] = 'pred'
agg_completions_df.loc[:,'obs_pred'] = 'obs'
supply_series = pd.concat([completions_preds_df, agg_completions_df])

wages_preds_df = get_predictions(agg_emps_df, ['average_annual_wage', 'total_national_employment'])
wages_preds_df.loc[:,'obs_pred'] = 'pred'
agg_emps_df.loc[:,'obs_pred'] = 'obs'
demand_series = pd.concat([wages_preds_df, agg_emps_df])

###########################################################################3

# Plot charts

completions_fig = px.line(supply_series, x='year', y='completions', color='obs_pred', markers=True)
institutions_fig = px.line(supply_series, x='year', y='institutions', color='obs_pred', markers=True)
l2.plotly_chart(completions_fig, use_container_width=True)
m2.plotly_chart(institutions_fig, use_container_width=True)
r2.markdown("" \
f"For {uoa}, using a {window}-year moving average, our supply projections for 2026 are")
r2_left_metric, r2_right_metric = r2.columns(2)
rounded_completions = round(list(supply_series.loc[supply_series['year'] == 2026, 'completions'])[0])
r2_left_metric.metric("Completions", value='{:,}'.format(rounded_completions), border=True)
rounded_institutions = round(list(supply_series.loc[supply_series['year'] == 2026,'institutions'])[0])
r2_right_metric.metric("Institutions", value='{:,}'.format(rounded_institutions), border=True)



wages_fig = px.line(demand_series, x='year', y='average_annual_wage', color='obs_pred', markers=True)
emps_fig = px.line(demand_series, x='year', y='total_national_employment', color='obs_pred', markers=True)
l3.plotly_chart(wages_fig, use_container_width=True)
m3.plotly_chart(emps_fig, use_container_width=True)

r3.markdown("" \
f"For {uoa}, using a {window}-year moving average, our demand projections for 2026 are")
r3_left_metric, r3_right_metric = r3.columns(2)
rounded_wages = round(list(demand_series.loc[demand_series['year'] == 2026, 'average_annual_wage'])[0])
r3_left_metric.metric("Avg. Median Wage", value=f"$ {'{:,}'.format(rounded_wages)}", border=True)
rounded_employments = round(list(demand_series.loc[demand_series['year'] == 2026,'total_national_employment'])[0])
r3_right_metric.metric("Total Employment Level", value='{:,}'.format(rounded_employments), border=True)

# STRETCH: Comparisons (against other UOAs and other industries (area?))