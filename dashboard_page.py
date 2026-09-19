# app/pages/dashboard_page.py

import streamlit as st
from controllers.data_controller import fetch_ticker_data
from app.components.charts import simple_price_chart


def render():
    st.title('Dashboard')

    ticker = st.selectbox(
        'Ticker',
        ["TSLA", "AMD", "SNPS", "GOOG", "ADBE", "TXN"],
        key='dashboard_ticker'
    )

    load_dash_btn = st.button("Load Dashboard", use_container_width=True)
    # ----------------------------
    # Dashboard Table (under load)
    # ----------------------------
    if load_dash_btn:
        try:
            df = fetch_ticker_data(ticker)
            fig = simple_price_chart(df.index, df['Close'], ticker=ticker)
            st.plotly_chart(fig, use_container_width=True)
            if df is not None and not df.empty:
                st.subheader("📊 Dashboard Historical Data")
                st.dataframe(df.tail(100))
        except Exception as e:
            st.error(f"Data fetch error for {ticker}: {e}")
