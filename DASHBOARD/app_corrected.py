import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Agricultural Market Price Intelligence",
    page_icon="🌾",
    layout="wide"
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")
MONGODB_URI = os.getenv("MONGODB_URI")


# --------------------------------------------------
# DASHBOARD TITLE
# --------------------------------------------------

st.title("🌾 Agricultural Market Price Intelligence")

st.markdown(
    "### Tomato Market Price Analysis and Intelligence Dashboard"
)

st.markdown(
    "Historical mandi data analysis, market comparison, "
    "price alerts and machine-learning-based forecasting."
)

st.divider()


# --------------------------------------------------
# LOAD DATA FROM MONGODB
# --------------------------------------------------

def load_market_data():
    """Load the complete Karnataka tomato dataset from MongoDB."""

    if not MONGODB_URI:
        raise ValueError(
            "MONGODB_URI was not found in the project-root .env file."
        )

    client = None

    try:
        client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=15000
        )

        client.admin.command("ping")

        database = client["agri_market_intelligence"]
        collection = database["karnataka_tomato_prices"]

        # Load every document. No market or date filter is applied here.
        records = list(collection.find({}, {"_id": 0}))

        if not records:
            raise ValueError(
                "No records were found in the MongoDB collection."
            )

        df = pd.DataFrame(records)

        required_columns = [
            "Arrival_Date",
            "Market",
            "Modal_Price",
            "Min_Price",
            "Max_Price"
        ]

        missing_columns = [
            column for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                "Missing required columns: "
                + ", ".join(missing_columns)
            )

        # MongoDB stores Arrival_Date as a date/datetime value.
        df["Arrival_Date"] = pd.to_datetime(
            df["Arrival_Date"],
            errors="coerce"
        )

        for column in ["Modal_Price", "Min_Price", "Max_Price"]:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        # Remove only rows that cannot be used for date/price analysis.
        df = df.dropna(
            subset=["Arrival_Date", "Modal_Price", "Market"]
        ).copy()

        df["Market"] = df["Market"].astype(str)
        df = df.sort_values("Arrival_Date").reset_index(drop=True)

        if df.empty:
            raise ValueError(
                "No valid market price records are available after data cleaning."
            )

        return df

    finally:
        if client is not None:
            client.close()


# --------------------------------------------------
# FETCH DATA AND HANDLE ERRORS
# --------------------------------------------------

try:
    # Deliberately not cached: each dashboard run reads the current
    # contents of MongoDB, avoiding an old cached count such as 254.
    df = load_market_data()

    st.success(
        f"Connected to MongoDB Atlas. "
        f"Loaded {len(df):,} valid records across "
        f"{df['Market'].nunique()} markets."
    )

except (ValueError, PyMongoError) as error:
    st.error(f"Dashboard connection or data error: {error}")
    st.stop()

except Exception as error:
    st.error(f"Unexpected error: {error}")
    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔎 Dashboard Filters")

available_markets = sorted(
    df["Market"].dropna().unique().tolist()
)

selected_markets = st.sidebar.multiselect(
    "Select Market",
    options=available_markets,
    default=available_markets
)

minimum_date = df["Arrival_Date"].min().date()
maximum_date = df["Arrival_Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date
)


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

if selected_markets:
    filtered_df = filtered_df[
        filtered_df["Market"].isin(selected_markets)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

# Apply the date filter only when Streamlit has returned a complete range.
if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates

    if start_date is not None and end_date is not None:
        filtered_df = filtered_df[
            (filtered_df["Arrival_Date"].dt.date >= start_date)
            & (filtered_df["Arrival_Date"].dt.date <= end_date)
        ]

if filtered_df.empty:
    st.warning(
        "No records are available for the selected filters. "
        "Choose at least one market and a date range containing records."
    )
    st.stop()

filtered_df = filtered_df.copy()


# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.subheader("📊 Market Price Overview")

total_records = len(filtered_df)
average_price = filtered_df["Modal_Price"].mean()
minimum_price = filtered_df["Modal_Price"].min()
maximum_price = filtered_df["Modal_Price"].max()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{total_records:,}")
col2.metric("Average Modal Price", f"₹{average_price:,.2f}")
col3.metric("Minimum Modal Price", f"₹{minimum_price:,.2f}")
col4.metric("Maximum Modal Price", f"₹{maximum_price:,.2f}")

st.caption(
    f"Showing {total_records:,} of {len(df):,} valid MongoDB records "
    "for the selected markets and date range."
)

st.divider()


# --------------------------------------------------
# DAILY MODAL PRICE TREND
# --------------------------------------------------

st.subheader("📈 Daily Tomato Modal Price Trend")

daily_prices = (
    filtered_df.groupby("Arrival_Date", as_index=False)["Modal_Price"]
    .mean()
)

daily_chart = px.line(
    daily_prices,
    x="Arrival_Date",
    y="Modal_Price",
    markers=True,
    title="Daily Average Modal Price",
    labels={
        "Arrival_Date": "Arrival Date",
        "Modal_Price": "Modal Price (₹)"
    }
)

daily_chart.update_layout(
    xaxis_title="Arrival Date",
    yaxis_title="Modal Price (₹)",
    hovermode="x unified"
)

st.plotly_chart(
    daily_chart,
    use_container_width=True
)


# --------------------------------------------------
# MARKET-WISE PRICE COMPARISON
# --------------------------------------------------

st.subheader("🏪 Market-wise Price Comparison")

market_prices = (
    filtered_df.groupby("Market", as_index=False)["Modal_Price"]
    .mean()
    .sort_values("Modal_Price", ascending=False)
)

market_chart = px.bar(
    market_prices,
    x="Market",
    y="Modal_Price",
    color="Modal_Price",
    title="Average Modal Price by Market",
    labels={
        "Market": "Market",
        "Modal_Price": "Average Modal Price (₹)"
    },
    text_auto=".2f"
)

market_chart.update_layout(
    xaxis_title="Market",
    yaxis_title="Average Modal Price (₹)"
)

st.plotly_chart(
    market_chart,
    use_container_width=True
)


# --------------------------------------------------
# HIGH PRICE ALERTS
# --------------------------------------------------

st.subheader("🚨 High Price Alerts")

price_threshold = 2000

high_price_records = filtered_df[
    filtered_df["Modal_Price"] > price_threshold
].copy()

if not high_price_records.empty:
    st.warning(
        f"{len(high_price_records):,} records have a "
        f"modal price above ₹{price_threshold:,}."
    )

    st.dataframe(
        high_price_records[
            [
                "Arrival_Date",
                "Market",
                "Min_Price",
                "Max_Price",
                "Modal_Price"
            ]
        ].sort_values(
            "Modal_Price",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success(
        f"No prices above ₹{price_threshold:,} "
        "were found in the selected data."
    )


# --------------------------------------------------
# MACHINE LEARNING FORECASTING
# --------------------------------------------------

st.divider()
st.header("🤖 Machine Learning Price Forecasting")

st.markdown(
    "Random Forest Regression is used to analyse historical "
    "Ramanagara tomato prices and generate short-term forecasts."
)

st.info(
    "This forecasting model currently covers Ramanagara only. "
    "It is separate from the selected-market dashboard filters."
)

evaluation_path = PROJECT_ROOT / "FORECASTING" / "model_evaluation.csv"
forecast_path = PROJECT_ROOT / "FORECASTING" / "next_7_days_forecast.csv"

if evaluation_path.exists() and forecast_path.exists():
    try:
        evaluation_df = pd.read_csv(evaluation_path)
        forecast_df = pd.read_csv(forecast_path)

        evaluation_required = ["Date", "Actual_Price", "Predicted_Price"]
        forecast_required = ["Date", "Predicted_Modal_Price"]

        missing_evaluation = [
            column for column in evaluation_required
            if column not in evaluation_df.columns
        ]
        missing_forecast = [
            column for column in forecast_required
            if column not in forecast_df.columns
        ]

        if missing_evaluation or missing_forecast:
            raise ValueError(
                "Forecast CSV files are missing required columns. "
                f"Evaluation missing: {missing_evaluation}; "
                f"forecast missing: {missing_forecast}"
            )

        evaluation_df["Date"] = pd.to_datetime(
            evaluation_df["Date"],
            errors="coerce"
        )
        forecast_df["Date"] = pd.to_datetime(
            forecast_df["Date"],
            errors="coerce"
        )

        for column in ["Actual_Price", "Predicted_Price"]:
            evaluation_df[column] = pd.to_numeric(
                evaluation_df[column],
                errors="coerce"
            )

        forecast_df["Predicted_Modal_Price"] = pd.to_numeric(
            forecast_df["Predicted_Modal_Price"],
            errors="coerce"
        )

        evaluation_df = evaluation_df.dropna(
            subset=evaluation_required
        ).copy()
        forecast_df = forecast_df.dropna(
            subset=forecast_required
        ).copy()

        if not evaluation_df.empty and not forecast_df.empty:
            actual = evaluation_df["Actual_Price"].to_numpy(dtype=float)
            predicted = evaluation_df["Predicted_Price"].to_numpy(dtype=float)

            mae = float(np.mean(np.abs(actual - predicted)))
            rmse = float(np.sqrt(np.mean((actual - predicted) ** 2)))

            st.subheader("📊 Model Performance")

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                "Mean Absolute Error (MAE)",
                f"₹{mae:,.2f}"
            )
            metric2.metric(
                "Root Mean Squared Error (RMSE)",
                f"₹{rmse:,.2f}"
            )
            metric3.metric(
                "Testing Records",
                f"{len(evaluation_df):,}"
            )

            st.caption(
                "Lower MAE and RMSE generally indicate smaller prediction errors."
            )

            st.subheader("📈 Actual vs Predicted Prices")

            comparison_df = evaluation_df.melt(
                id_vars=["Date"],
                value_vars=["Actual_Price", "Predicted_Price"],
                var_name="Price_Type",
                value_name="Price"
            )

            comparison_chart = px.line(
                comparison_df,
                x="Date",
                y="Price",
                color="Price_Type",
                markers=True,
                title="Random Forest: Actual vs Predicted Prices",
                labels={
                    "Date": "Date",
                    "Price": "Modal Price (₹)",
                    "Price_Type": "Price Type"
                }
            )

            comparison_chart.update_layout(
                hovermode="x unified"
            )

            st.plotly_chart(
                comparison_chart,
                use_container_width=True
            )

            st.subheader("🔮 Seven-Day Tomato Price Forecast")

            st.warning(
                "Historical forecast: the source dataset ends on "
                "4 November 2025. These predictions are not live "
                "November 2026 market prices."
            )

            forecast_chart = px.line(
                forecast_df,
                x="Date",
                y="Predicted_Modal_Price",
                markers=True,
                title="Predicted Ramanagara Tomato Modal Prices",
                labels={
                    "Date": "Forecast Date",
                    "Predicted_Modal_Price": "Predicted Modal Price (₹)"
                }
            )

            st.plotly_chart(
                forecast_chart,
                use_container_width=True
            )

            st.dataframe(
                forecast_df,
                use_container_width=True,
                hide_index=True
            )

            forecast_download = forecast_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇️ Download Forecast Results",
                data=forecast_download,
                file_name="tomato_price_forecast.csv",
                mime="text/csv"
            )
        else:
            st.warning(
                "Forecast files exist, but they contain no valid records."
            )

    except (OSError, ValueError, KeyError, pd.errors.ParserError) as error:
        st.error(f"Could not display forecasting results: {error}")

else:
    st.warning(
        "Forecast files were not found. Run "
        "FORECASTING/price_forecasting.py first."
    )


# --------------------------------------------------
# COMPLETE MARKET DATA
# --------------------------------------------------

st.divider()
st.subheader("📋 Market Data Records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# DOWNLOAD FILTERED DATA
# --------------------------------------------------

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name="tomato_market_price_analysis.csv",
    mime="text/csv"
)


# --------------------------------------------------
# REFRESH DASHBOARD
# --------------------------------------------------

st.sidebar.divider()

if st.sidebar.button("🔄 Refresh Dashboard"):
    st.rerun()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Agricultural Market Price Intelligence and "
    "Short-Term Crop Price Forecasting Using Big Data Analytics"
)

st.caption(
    "Data source: Historical mandi market price records "
    "| Database: MongoDB Atlas"
)
