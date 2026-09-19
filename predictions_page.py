import streamlit as st
import pandas as pd
from controllers.prediction_controller import run_prediction

def render():
    st.title("Predictions")

    # ----------------------------
    # Show today date
    # ----------------------------
    st.markdown(f"**Today:** {pd.Timestamp.today().date()}")

    # ----------------------------
    # Settings
    # ----------------------------
    ticker = st.selectbox(
        "Ticker",
        ["TSLA", "AMD", "SNPS", "GOOG", "ADBE", "TXN"]
    )
    future_days = st.slider("Forecast horizon (days)", 1, 30, 7)
    #threshold = st.number_input("Signal threshold (%)", 0.1, 10.0, 0.5)
    # ----------------------------
    # Signal Threshold (Percentage input)
    # ----------------------------
    threshold = st.number_input(
        "Signal Threshold (%)",  # label
        min_value=0.1,  # أقل قيمة
        max_value=10.0,  # أكبر قيمة
        value=0.5,  # القيمة الافتراضية
        step=0.1,  # خطوة increment/decrement
        format="%.2f"  # لتنسيق الرقم بعشرية 2
    )

    # عرض القيمة مع %
    st.markdown(f"**Signal Threshold:** {threshold:.2f}%")

    run_pred_btn = st.button("Run Prediction", use_container_width=True)

    # ----------------------------
    # Prediction
    # ----------------------------
    if run_pred_btn:
        with st.spinner("Running models..."):
            out = run_prediction(ticker, future_days, threshold)
            if not out:
                return

            st.divider()
            st.subheader("📈 Prediction Results")

            # ----------------------------
            # Metrics with $ and % change
            # ----------------------------
            current = out['current_price']
            predicted = out['predicted_close']

            # حساب النسبة
            pct_change = (predicted - current) / current * 100
            pct_display = f"{pct_change:.2f}%"

            # تحديد اللون
            color = "green" if pct_change > 0 else "red" if pct_change < 0 else "gray"

            col1, col2 = st.columns(2)
            col1.metric("Current Price", f"${current:.2f}")
            col1.metric("Predicted Close (Final Day)", f"${predicted:.2f}")
            col2.metric("Signal", out['signal'])
            col2.markdown(f"**Change:** <span style='color:{color}'>{pct_display}</span>", unsafe_allow_html=True)

            # ----------------------------
            # Plotly chart
            # ----------------------------
            fig = out['figure']

            fig.update_layout(
                yaxis=dict(
                    tick0=0,
                    dtick=100
                ),
                xaxis_title="Date",
                yaxis_title="Price ($)",
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)

            # ----------------------------
            # Future Prices Table
            # ----------------------------
            st.subheader("📅 Forecasted Prices Table")
            forecast_df = pd.DataFrame({
                "Date": out['future_dates'],
                "Predicted Close": out['future_prices']
            })
            forecast_df['Date'] = pd.to_datetime(forecast_df['Date']).dt.date
            # Format Predicted Close with $ sign
            forecast_df['Predicted Close'] = forecast_df['Predicted Close'].apply(lambda x: f"${x:.2f}")
            st.dataframe(forecast_df)
