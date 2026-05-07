import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pride Profit Pro", page_icon="🦁", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, #4b1e2f, #2b0f19);
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
h1, h2, h3 {
    color: #f4c542 !important;
    text-align: center;
    font-weight: bold;
}
div, p, label {
    color: white !important;
    font-size: 18px;
}
.stNumberInput input {
    background-color: white;
    color: black;
    border-radius: 10px;
}
.stSuccess {
    background-color: #f4c542;
    color: black;
    padding: 15px;
    border-radius: 12px;
    font-size: 24px;
    font-weight: bold;
}
hr { border-color: #f4c542; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.title("🦁 Pride Profit Pro")

tab1, tab2 = st.tabs(["Commission Calculator", "Leaderboard"])

with tab1:
    st.subheader("Roofing Commission Calculator")

    job_amount = st.number_input("Original Job Amount ($)", min_value=0.0, step=100.0)
    supplement_amount = st.number_input("Supplement Amount ($)", min_value=0.0, step=100.0)
    commission_percent = st.number_input("Commission Percentage (%)", min_value=0.0, step=1.0)

    total_revenue = job_amount + supplement_amount
    commission = total_revenue * (commission_percent / 100)

    st.divider()
    st.subheader("Commission Summary")
    st.write(f"Original Job Amount: ${job_amount:,.2f}")
    st.write(f"Supplement Amount: ${supplement_amount:,.2f}")
    st.write(f"Total Revenue: ${total_revenue:,.2f}")
    st.success(f"💰 Commission Earned: ${commission:,.2f}")

with tab2:
    st.subheader("🏆 Sales Leaderboard")

    if st.button("🔄 Refresh Leaderboard"):
        st.cache_data.clear()
        st.rerun()

    sheet_url = "https://docs.google.com/spreadsheets/d/14iXrynuoHaMO6y17XUw10ujrT-DC0jwcvFN53iIynBE/export?format=csv&gid=0"

    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()

        rep_col = df.columns[0]
        sales_col = df.columns[1]
        deals_col = df.columns[2]

        df[sales_col] = (
            df[sales_col]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        df[deals_col] = (
            df[deals_col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        df[sales_col] = pd.to_numeric(df[sales_col], errors="coerce")
        df[deals_col] = pd.to_numeric(df[deals_col], errors="coerce")

        df = df.dropna(subset=[rep_col, sales_col, deals_col])

        if df.empty:
            st.warning("No leaderboard data found. Check that your Google Sheet has rep names, sales, and contract numbers filled in.")
            st.stop()

        df["Average Contract Value"] = df[sales_col] / df[deals_col]

        df = df.sort_values(by=sales_col, ascending=False).reset_index(drop=True)

        ranks = []
        for i in range(len(df)):
            if i == 0:
                ranks.append("🥇 1")
            elif i == 1:
                ranks.append("🥈 2")
            elif i == 2:
                ranks.append("🥉 3")
            else:
                ranks.append(f"{i + 1}")

        df.insert(0, "Rank", ranks)

        df[sales_col] = df[sales_col].apply(lambda x: f"${x:,.2f}")
        df["Average Contract Value"] = df["Average Contract Value"].apply(lambda x: f"${x:,.2f}")

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()
        top_rep = df.iloc[0]
        st.success(f"👑 Current Leader: {top_rep[rep_col]} — {top_rep[sales_col]}")

    except Exception as e:
        st.error("The leaderboard could not load.")
        st.write(e)

st.divider()
st.caption("Built for Pride Roofing & Construction")
