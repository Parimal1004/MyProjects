import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(
    page_title="Demand Forecasting App",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Load model ----------
@st.cache_resource
def load_artifacts():
    with open("xgboost_demand_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("label_encoders.pkl", "rb") as f:
        encoders = pickle.load(f)
    return model, encoders

model, label_encoders = load_artifacts()

# ---------- Light styling ----------
st.markdown("""
    <style>
    /* Page background gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e2530 0%, #0f172a 100%);
    }

    /* Title glow */
    h1 {
        background: linear-gradient(90deg, #4ade80, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glassy card look for the form */
    div[data-testid="stForm"] {
    background: rgba(10, 13, 20, 0.85);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 2em;
     }

    .stButton>button {
        width: 100%;
        height: 3em;
        font-size: 1.1em;
        font-weight: 600;
        border-radius: 10px;
        background: linear-gradient(90deg, #4ade80, #38bdf8);
        color: #0f172a;
        border: none;
    }
    .stButton>button:hover {
        opacity: 0.85;
        color: #0f172a;
    }

    .result-box {
        padding: 1.5em;
        border-radius: 12px;
        background: rgba(30, 37, 48, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(74, 222, 128, 0.3);
        text-align: center;
        margin-top: 1em;
    }
    .result-number {
        font-size: 2.8em;
        font-weight: 700;
        color: #4ade80;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("📦 About")
    st.write(
        "This app predicts product demand using a trained "
        "**XGBoost** regression model based on pricing, "
        "inventory, and market signals."
    )
    st.divider()
    st.caption("Model: XGBoost Regressor")
    st.caption("Inputs: Price, Discount, Inventory, Promotion, Competitor Price, Category")

# ---------- Header ----------
st.title("📦 Demand Forecasting App")
st.caption("Estimate expected product demand from pricing and market conditions.")
st.divider()

# ---------- Input form ----------
st.subheader("Input Features")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        price = st.number_input("💲 Price", min_value=0.0, value=50.0, step=1.0)
        competitor_pricing = st.number_input("🏷️ Competitor Price", min_value=0.0, value=50.0, step=1.0)

    with col2:
        discount = st.number_input("🔻 Discount (%)", min_value=0, max_value=100, value=10)
        promotion = st.selectbox("📣 Promotion Active?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

    with col3:
        inventory_level = st.number_input("🏬 Inventory Level", min_value=0, value=100)
        category = st.selectbox("🗂️ Category", label_encoders["Category"].classes_.tolist())

    submitted = st.form_submit_button("🔮 Predict Demand")

# ---------- Prediction ----------
if submitted:
    input_data = pd.DataFrame({
        "Price": [price],
        "Discount": [discount],
        "Inventory Level": [inventory_level],
        "Promotion": [promotion],
        "Competitor Pricing": [competitor_pricing],
        "Category": [category]
    })

    for col, encoder in label_encoders.items():
        if col in input_data.columns:
            input_data[col] = encoder.transform(input_data[col])

    prediction = model.predict(input_data)[0]

    st.markdown(
        f"""
        <div class="result-box">
            <div>Predicted Demand</div>
            <div class="result-number">{int(prediction)} units</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("🔍 View input summary"):
        st.dataframe(
            pd.DataFrame({
                "Price": [price],
                "Discount (%)": [discount],
                "Inventory Level": [inventory_level],
                "Promotion": ["Yes" if promotion == 1 else "No"],
                "Competitor Price": [competitor_pricing],
                "Category": [category],
            }),
            hide_index=True,
            use_container_width=True,
        )