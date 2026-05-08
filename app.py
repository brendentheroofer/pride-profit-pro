import streamlit as st
import pandas as pd
from datetime import date

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

tab1, tab2 = st.tabs(["Commission Calculator", "Sales Meeting Dashboard"])

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
    st.subheader("🏆 Sales Meeting Dashboard")

    if st.button("🔄 Refresh Dashboard"):
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
            st.warning("No leaderboard data found. Check your Google Sheet.")
            st.stop()

        df["Average Contract Value"] = df[sales_col] / df[deals_col]
        df = df.sort_values(by=sales_col, ascending=False).reset_index(drop=True)

        yearly_goal = 4200000
        current_sales = df[sales_col].sum()
        remaining_sales = yearly_goal - current_sales
        progress = current_sales / yearly_goal

        today = date.today()
        start_of_year = date(today.year, 1, 1)
        end_of_year = date(today.year, 12, 31)

        days_elapsed = max((today - start_of_year).days + 1, 1)
        total_days = (end_of_year - start_of_year).days + 1
        days_remaining = max((end_of_year - today).days, 1)

        expected_sales_by_today = yearly_goal * (days_elapsed / total_days)
        ahead_or_behind = current_sales - expected_sales_by_today
        projected_finish = (current_sales / days_elapsed) * total_days
        weekly_needed = remaining_sales / (days_remaining / 7)

        st.subheader("🎯 2026 Team Sales Goal")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Yearly Goal", f"${yearly_goal:,.2f}")

        with col2:
            st.metric("Current Sales", f"${current_sales:,.2f}")

        with col3:
            st.metric("Remaining", f"${remaining_sales:,.2f}")

        st.progress(min(progress, 1.0))
        st.write(f"Progress to Goal: {progress * 100:.2f}%")

        st.divider()

        st.subheader("🔥 Pace to Goal")

        pace1, pace2, pace3 = st.columns(3)

        with pace1:
            st.metric("Expected Sales By Today", f"${expected_sales_by_today:,.2f}")

        with pace2:
            st.metric("Ahead / Behind Pace", f"${ahead_or_behind:,.2f}")

        with pace3:
            st.metric("Projected Year-End", f"${projected_finish:,.2f}")

        st.write(f"Weekly Sales Needed to Hit Goal: **${weekly_needed:,.2f}**")

        if projected_finish >= yearly_goal:
            st.success("🟢 Team is currently on pace to beat the yearly goal.")
        else:
            st.warning("🔴 Team is currently behind pace. Time to turn up the heat.")

        st.divider()

        top_rep = df.iloc[0]
        most_contracts_rep = df.sort_values(by=deals_col, ascending=False).iloc[0]
        largest_avg_rep = df.sort_values(by="Average Contract Value", ascending=False).iloc[0]

        st.subheader("👑 Rep Recognition")

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric("Current Leader", top_rep[rep_col])

        with r2:
            st.metric("Leader Sales", f"${top_rep[sales_col]:,.2f}")

        with r3:
            st.metric("Contracts", int(top_rep[deals_col]))

        st.success(
            f"🏆 Rep Spotlight: {top_rep[rep_col]} is leading the team with "
            f"${top_rep[sales_col]:,.2f} in contracted sales."
        )

        st.divider()

        st.subheader("🔥 Extra Leader Banners")

        b1, b2 = st.columns(2)

        with b1:
            st.success(
                f"📄 Most Contracts: {most_contracts_rep[rep_col]} — "
                f"{int(most_contracts_rep[deals_col])} contracts"
            )

        with b2:
            st.success(
                f"💎 Largest Average Contract: {largest_avg_rep[rep_col]} — "
                f"${largest_avg_rep['Average Contract Value']:,.2f}"
            )

        st.divider()

        st.subheader("📈 Team Momentum Chart")

        chart_df = df[[rep_col, sales_col]].copy()
        chart_df = chart_df.set_index(rep_col)

        st.bar_chart(chart_df)

        st.divider()

        st.subheader("🏆 Full Leaderboard")

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

    except Exception as e:
        st.error("The dashboard could not load.")
        st.write(e)

st.divider()
st.caption("Built for Pride Roofing & Construction")
