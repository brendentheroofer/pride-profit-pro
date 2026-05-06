import streamlit as st

# PAGE SETTINGS
st.set_page_config(
    page_title="Pride Profit Pro",
    page_icon="🦁",
    layout="centered"
)

# CUSTOM STYLING
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, #4b1e2f, #2b0f19);
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

h1, h2, h3 {
    color: #f4c542 !important;
    text-align: center;
    font-weight: bold;
}

p, label, div {
    color: white !important;
    font-size: 18px;
}

.stNumberInput input {
    background-color: white;
    color: black;
    border-radius: 10px;
    font-size: 18px;
}

.stSuccess {
    background-color: #f4c542;
    color: black;
    padding: 15px;
    border-radius: 12px;
    font-size: 24px;
    font-weight: bold;
}

hr {
    border-color: #f4c542;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.title("🦁 Pride Profit Pro")
st.subheader("Roofing Commission Calculator")

st.divider()

# INPUTS
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

# CALCULATIONS
total_revenue = job_amount + supplement_amount
commission = total_revenue * (commission_percent / 100)

st.divider()

# OUTPUT
st.subheader("Commission Summary")

st.write(f"Original Job Amount: ${job_amount:,.2f}")
st.write(f"Supplement Amount: ${supplement_amount:,.2f}")
st.write(f"Total Revenue: ${total_revenue:,.2f}")

st.success(f"💰 Commission Earned: ${commission:,.2f}")

st.divider()

st.caption("Built for Pride Roofing & Construction")