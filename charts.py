# app/components/charts.py

import plotly.graph_objects as go


def simple_price_chart(dates, prices, future_dates=None, future_prices=None, ticker=None):
    if dates is None or prices is None or len(dates) == 0:
        import streamlit as st
        st.warning("Cannot render chart: missing price data")
        return None

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines+markers', name='Actual'))

    if future_dates is not None and future_prices is not None:
        if len(future_dates) != len(future_prices):
            future_dates = future_dates[:len(future_prices)]
        fig.add_trace(go.Scatter(x=future_dates, y=future_prices, mode='lines+markers', name='Forecast'))

    fig.update_layout(
        title=f"{ticker} Price Chart" if ticker else "Price Chart",
        xaxis_title='Date', yaxis_title='Price', template='plotly_white'
    )
    return fig
