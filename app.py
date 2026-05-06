import streamlit as st
import pandas as pd

# PAGE SETTINGS
st.set_page_config(
    page_title="Pride Profit Pro",
    page_icon="🦁",
    layout="wide"
)

# CUSTOM STYLE
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, #4b1e2f, #2b0f19);
}

h1, h2, h3 {
    color: #f4c542 !important;
    text-align: center;
}

div, p, label {
    color: white !important;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.title("🦁 Pride Profit Pro")

tab1, tab2 = st.tabs(["Commission Calculator", "Leaderboard"])

# ---------------- CALCULATOR TAB ----------------

with tab1:

    st.subheader("Roofing Commission Calculator")

    job_amount = st.number_input(
        "Original Job Amount ($)",
        min_value=0.0,
        step=100.0
    )

    supplement_amount = st.number_input(
        "Supplement Amount ($)",
        min_value=0.0,
        step=100.0
    )

    commission_percent = st.number_input(
        "Commission Percentage (%)",
        min_value=0.0,
        step=1.0
    )

    total_revenue = job_amount + supplement_amount
    commission = total_revenue * (commission_percent / 100)

    st.divider()

    st.subheader("Commission Summary")

    st.write(f"Original Job Amount: ${job_amount:,.2f}")
    st.write(f"Supplement Amount: ${supplement_amount:,.2f}")
    st.write(f"Total Revenue: ${total_revenue:,.2f}")

    st.success(f"💰 Commission Earned: ${commission:,.2f}")

# ---------------- LEADERBOARD TAB ----------------

with tab2:

    st.subheader("🏆 Sales Leaderboard")

    leaderboard_data = {
        "Rep": [
            "Tod",
            "Steele",
            "Ernesto",
            "Stefan",
            "Kevin",
            "Hunter",
            "Jackson"
        ],

        "Contracted Sales": [
            169473.25,
            159796.52,
            156821.03,
            99063.99,
            41450.00,
            11166.54,
            7256.29
        ],

        "Deals": [
            16,
            13,
            13,
            10,
            11,
            1,
            1
        ]
    }

    df = pd.DataFrame(leaderboard_data)

    df["Average Deal Size"] = (
        df["Contracted Sales"] / df["Deals"]
    )

    df = df.sort_values(
        by="Contracted Sales",
        ascending=False
    ).reset_index(drop=True)

    # ADD RANKINGS
    ranks = []

    for i in range(len(df)):

        if i == 0:
            ranks.append("🥇 1")

        elif i == 1:
            ranks.append("🥈 2")

        elif i == 2:
            ranks.append("🥉 3")

        else:
            ranks.append(f"{i+1}")

    df.insert(0, "Rank", ranks)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    top_rep = df.iloc[0]

    st.success(
        f"👑 Current Leader: {top_rep['Rep']} — "
        f"${top_rep['Contracted Sales']:,.2f}"
    )
