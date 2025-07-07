import streamlit as st

summary_page = st.Page("./pages/summary.py", title="EPEDS Home", icon= "📊")
uoa_page = st.Page("./pages/uoa.py", title="UOA Overview", icon="🔍")
series_page = st.Page("./pages/series.py", title="Supply and Demand", icon="📈")
forecast_page = st.Page("./pages/forecast.py", title="Forecast", icon="🔮")

pg = st.navigation(
        {
            "Home": [summary_page],
            "Units of Analysis": [uoa_page, series_page, forecast_page],
        }
    )
pg.run()


# FUTURE:
# '''
#  Manually organize "no-match" between crosswalk
#  Use LLM to name UOA's more intuitively
#  Use additional data to train forecast (requirements, job dynamics, demographics)
# '''

# TODO: Make layout more grid-like
# TODO: Sort UOA alphabetically