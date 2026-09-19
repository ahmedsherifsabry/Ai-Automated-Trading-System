# app/pages/signals_page.py

import streamlit as st
from controllers.trade_controller import list_pending, approve, reject


# ----------------------------
# Status badge helper
# ----------------------------
def status_badge(status: str) -> str:
    colors = {
        "PENDING": "#f0ad4e",
        "APPROVED": "#5cb85c",
        "REJECTED": "#d9534f"
    }

    return f"""
    <span style="
        padding:6px 14px;
        border-radius:20px;
        background:{colors.get(status, '#777')};
        color:white;
        font-weight:bold;
        font-size:13px;">
        {status}
    </span>
    """


# ----------------------------
# Signals Page
# ----------------------------
def render():
    st.title("Signals")

    # Page description
    st.caption("Review generated trading signals and approve or reject them")

    # Fetch recent signals (pending + history)
    signals = list_pending(limit=50, only_pending=False)

    if not signals:
        st.markdown("""
        <div style='text-align:center; padding:40px; color:#777'>
            <h3>No signals yet</h3>
            <p>Generated signals will appear here</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("<hr>", unsafe_allow_html=True)

    # Table header
    header = st.columns([1.2, 1.2, 0.5, 1.6, 1, 1])
    header[0].markdown("**Ticker**")
    header[1].markdown("**Type**")
    header[3].markdown("**Status**")
    header[4].markdown("**Approve**")
    header[5].markdown("**Reject**")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Signals rows
    for sig in signals:
        sig_id, ticker, sig_type, confidence, status, created_at = sig

        cols = st.columns([1.2, 1.2, 0.5, 1.6, 1, 1])

        cols[0].write(ticker)
        cols[1].write(sig_type)
        cols[3].markdown(status_badge(status), unsafe_allow_html=True)

        # Buttons only for pending signals
        if status == "PENDING":
            approve_btn = cols[4].button(
                "Approve",
                key=f"approve_{sig_id}",
                use_container_width=True
            )
            reject_btn = cols[5].button(
                "Reject",
                key=f"reject_{sig_id}",
                use_container_width=True
            )

            if approve_btn:
                approve(sig_id)
                st.success(f"Signal {sig_id} approved ✅")
                st.rerun()

            if reject_btn:
                reject(sig_id)
                st.warning(f"Signal {sig_id} rejected ❌")
                st.rerun()
        else:
            cols[4].write("—")
            cols[5].write("—")
