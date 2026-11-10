
import pandas as pd
import numpy as np
from pathlib import Path
from google.cloud import bigquery
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Retrieve the raw dataset directly from BigQuery
PROJECT_ID = "agrimarketanalytics"
TABLE_ID = "agrimarketanalytics.mandi_price_data.tomato_karnataka_2025"

client = bigquery.Client(project=PROJECT_ID)

query = f"""
    SELECT *
    FROM `{TABLE_ID}`
"""

df = client.query(query).result().to_dataframe(create_bqstorage_client=False)

print("Records retrieved from BigQuery:", len(df))

if df.empty:
    raise ValueError("BigQuery returned no records.")

# Prepare dataset
df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"])
df["Modal_Price"] = pd.to_numeric(
    df["Modal_Price"], errors="coerce"
)

# Select Ramanagara market
df = df[df["Market"] == "Ramanagara"].copy()
df = df.dropna(subset=["Arrival_Date", "Modal_Price"])

if df.empty:
    raise ValueError("No valid Ramanagara records found in BigQuery.")

# Calculate daily average prices
daily = (
    df.groupby("Arrival_Date")["Modal_Price"]
    .mean()
    .sort_index()
)

# Fill missing dates
daily = daily.asfreq("D")
daily = daily.interpolate(method="time")

# Generate features
data = pd.DataFrame({"Price": daily})

data["Lag_1"] = data["Price"].shift(1)
data["Lag_7"] = data["Price"].shift(7)
data["Rolling_Mean_7"] = (
    data["Price"].shift(1).rolling(7).mean()
)
data["Day_Of_Week"] = data.index.dayofweek
data["Day_Of_Year"] = data.index.dayofyear

data = data.dropna()

features = [
    "Lag_1",
    "Lag_7",
    "Rolling_Mean_7",
    "Day_Of_Week",
    "Day_Of_Year"
]

X = data[features]
y = data["Price"]

if len(data) < 10:
    raise ValueError("Insufficient records for model training.")

# Split data chronologically
split = int(len(data) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]
y_train = y.iloc[:split]
y_test = y.iloc[split:]

# Train Random Forest
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print("\n===== MODEL EVALUATION =====")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))

# Save evaluation results
output_folder = Path("FORECASTING")
output_folder.mkdir(exist_ok=True)

results = pd.DataFrame({
    "Date": y_test.index,
    "Actual_Price": y_test.values,
    "Predicted_Price": predictions
})

results.to_csv(
    output_folder / "model_evaluation.csv",
    index=False
)

# Predict next 7 days
history = daily.copy()
future_results = []

for _ in range(7):

    next_date = history.index[-1] + pd.Timedelta(days=1)

    row = pd.DataFrame([{
        "Lag_1": history.iloc[-1],
        "Lag_7": history.iloc[-7],
        "Rolling_Mean_7": history.iloc[-7:].mean(),
        "Day_Of_Week": next_date.dayofweek,
        "Day_Of_Year": next_date.dayofyear
    }])

    predicted_price = model.predict(row[features])[0]

    future_results.append({
        "Date": next_date,
        "Predicted_Modal_Price": round(predicted_price, 2)
    })

    history.loc[next_date] = predicted_price

forecast_df = pd.DataFrame(future_results)

forecast_df.to_csv(
    output_folder / "next_7_days_forecast.csv",
    index=False
)

print("\n===== NEXT 7 DAYS FORECAST =====")
print(forecast_df.to_string(index=False))

print("\nForecast files saved successfully!")

client.close()
