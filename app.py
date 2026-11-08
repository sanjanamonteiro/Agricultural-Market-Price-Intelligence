
import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import PyMongoError


# -------------------- PAGE CONFIGURATION --------------------

st.set_page_config(
    page_title="AgriMarket Intelligence",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Agricultural Market Price Intelligence")
st.caption("Karnataka Tomato Market | Ramanagara | FAQ Grade")


# -------------------- LOAD MONGODB SETTINGS --------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


def load_env_file():
    if not ENV_FILE.exists():
        return

    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


load_env_file()

MONGODB_URI = os.getenv("MONGODB_URI")


# -------------------- FETCH DATA --------------------

@st.cache_data(ttl=60)
def load_market_data():
    if not MONGODB_URI:
        raise ValueError(
            "MONGODB_URI was not found in the project's .env file."
        )

    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=10000
    )

    client.admin.command("ping")

    collection = client[
        "agri_market_intelligence"
    ][
        "ramanagara_tomato_prices"
    ]

    records = list(collection.find({}, {"_id": 0}))

    client.close()

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    required_columns = [
        "Arrival_Date",
        "Market",
        "Modal_Price",
        "Min_Price",
        "Max_Price"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required MongoDB fields: {missing}"
        )

    df["Arrival_Date"] = pd.to_datetime(
        df["Arrival_Date"],
        dayfirst=True,
        errors="coerce"
    )

    for column in ["Modal_Price", "Min_Price", "Max_Price"]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.dropna(
        subset=["Arrival_Date", "Modal_Price"]
    )

    df = df.sort_values("Arrival_Date")

    return df


# -------------------- DASHBOARD --------------------

try:
    df = load_market_data()

    if df.empty:
        st.warning("No market records were found in MongoDB.")
        st.stop()

    st.success(
        f"Connected to MongoDB Atlas — {len(df)} records loaded."
    )

    # Sidebar filters
    st.sidebar.header("Dashboard Filters")

    markets = sorted(df["Market"].dropna().unique().tolist())

    selected_markets = st.sidebar.multiselect(
        "Select Market",
        markets,
        default=markets
    )

    start_date = df["Arrival_Date"].min().date()
    end_date = df["Arrival_Date"].max().date()

    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        value=(start_date, end_date),
        min_value=start_date,
        max_value=end_date
    )

    if len(selected_dates) != 2:
        st.info("Please select both a start date and an end date.")
        st.stop()

    filtered_df = df[
        (df["Market"].isin(selected_markets))
        & (
            df["Arrival_Date"].dt.date >= selected_dates[0]
        )
        & (
            df["Arrival_Date"].dt.date <= selected_dates[1]
        )
    ].copy()

    if filtered_df.empty:
        st.warning("No records match the selected filters.")
        st.stop()

    # Key performance indicators
    st.subheader("Market Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Records",
        f"{len(filtered_df):,}"
    )

    col2.metric(
        "Average Modal Price",
        f"₹{filtered_df['Modal_Price'].mean():,.2f}"
    )

    col3.metric(
        "Minimum Price",
        f"₹{filtered_df['Min_Price'].min():,.0f}"
    )

    col4.metric(
        "Maximum Price",
        f"₹{filtered_df['Max_Price'].max():,.0f}"
    )

    st.divider()

    # Price trend
    st.subheader("📈 Tomato Modal Price Trend")

    trend_df = (
        filtered_df
        .groupby("Arrival_Date", as_index=False)
        ["Modal_Price"]
        .mean()
    )

    fig_trend = px.line(
        trend_df,
        x="Arrival_Date",
        y="Modal_Price",
        markers=True,
        title="Daily Average Modal Price",
        labels={
            "Arrival_Date": "Arrival Date",
            "Modal_Price": "Modal Price (₹)"
        }
    )

    fig_trend.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )

    # Market comparison
    st.subheader("🏪 Market-wise Price Comparison")

    market_df = (
        filtered_df
        .groupby("Market", as_index=False)
        ["Modal_Price"]
        .mean()
        .sort_values("Modal_Price", ascending=False)
    )

    fig_market = px.bar(
        market_df,
        x="Market",
        y="Modal_Price",
        color="Modal_Price",
        title="Average Modal Price by Market",
        labels={
            "Market": "Market",
            "Modal_Price": "Average Modal Price (₹)"
        }
    )

    st.plotly_chart(
        fig_market,
        use_container_width=True
    )

    # High-price alerts
    st.subheader("🚨 High-Price Alerts")

    alert_df = filtered_df[
        filtered_df["Modal_Price"] > 2000
    ].copy()

    if alert_df.empty:
        st.info("No prices above ₹2,000 were found.")
    else:
        st.warning(
            f"{len(alert_df)} records have a modal price above ₹2,000."
        )

        st.dataframe(
            alert_df,
            use_container_width=True,
            hide_index=True
        )

    # Raw data
    st.subheader("📋 Market Records")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # Download filtered records
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv_data,
        file_name="ramanagara_tomato_market_data.csv",
        mime="text/csv"
    )

    if st.button("🔄 Refresh Dashboard"):
        st.cache_data.clear()
        st.rerun()

except (ValueError, PyMongoError) as error:
    st.error(f"Dashboard connection or data error: {error}")

except Exception as error:
    st.error(f"Unexpected dashboard error: {error}")
