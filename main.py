import streamlit as st

summary_page = st.Page("./pages/summary.py", title="CIP and SOC Stats", icon= "📊")
uoa_page = st.Page("./pages/uoa.py", title="Understanding UOAs", icon="🔍")
series_page = st.Page("./pages/series.py", title="UOAs over Time", icon="📈")
supply_page = st.Page("./pages/supply.py", title="Supply Forecast", icon="🎲")
demand_page = st.Page("./pages/demand.py", title="Demand Forecast", icon="🔮")

pg = st.navigation(
        {
            "Summary": [summary_page],
            "Units of Analysis": [uoa_page, series_page],
            "Forecasts": [supply_page, demand_page]
        }
    )
pg.run()




