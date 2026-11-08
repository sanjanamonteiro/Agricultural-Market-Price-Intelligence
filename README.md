# Agricultural Market Price Intelligence and Short-Term Crop Price Forecasting Using Big Data Analytics

## 1. Project Overview

This project develops a Big Data analytics system for analysing agricultural market prices, understanding historical tomato price trends, comparing prices across markets, detecting high-price records, and generating short-term price forecasts.

The project uses Karnataka tomato market-price data and combines cloud data warehousing, NoSQL storage, stream processing, data visualisation, and machine learning.

## 2. Objectives

- Collect and analyse agricultural market-price data.
- Store and process structured data using Google BigQuery.
- Transfer and analyse data using MongoDB Atlas.
- Implement real-time data streaming using Apache Kafka and Spark Structured Streaming.
- Build an interactive dashboard using Streamlit.
- Apply machine learning to forecast short-term tomato prices.
- Evaluate model performance using MAE and RMSE.

## 3. Technologies Used

| Category | Technology |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Cloud Data Warehouse | Google BigQuery |
| NoSQL Database | MongoDB Atlas |
| Stream Processing | Apache Kafka, Apache Spark |
| Dashboard | Streamlit |
| Machine Learning | Random Forest Regression |
| Data Visualisation | Streamlit charts |
| Development Environment | Visual Studio Code |

## 4. Dataset

**Source:** Data.gov.in / AGMARKNET

**Dataset:** Variety-wise Daily Market Prices Data of Commodity

**Selected data:**
- Commodity: Tomato
- State: Karnataka
- Period: 1 January 2025 – 31 December 2025
- Total records: 673
- Number of markets: 9

The dataset contains fields such as Arrival_Date, Commodity, District, Grade, Market, Max_Price, Min_Price, Modal_Price, State, and Variety.

The original dataset is stored in `DATA/RAW/`.

## 5. Project Structure

```text
Agricultural_Market_Price_Intelligence/
│
├── DASHBOARD/
│   └── app_corrected.py
│
├── DATA/
│   └── RAW/
│       ├── original_mandi_dataset.csv
│       └── tomato_karnataka_2025.csv
│
├── FORECASTING/
│   ├── price_forecasting.py
│   ├── model_evaluation.csv
│   └── next_7_days_forecast.csv
│
├── MONGODB/
│   ├── index_performance.py
│   ├── mongodb_queries.py
│   └── mongodb_results.txt
│
├── STREAMING/
│   ├── kafka_price_producer.py
│   └── spark_kafka_stream.py
│
├── DOCS/
├── NOTEBOOKS/
├── SCRIPTS/
│
├── app.py
├── load_full_dataset.py
├── mongodb_performance.py
├── test_bigquery.py
├── test_mongodb.py
├── transfer_bigquery_to_mongodb.py
├── atlas-credentials.env
└── .gitignore
```

Generated Spark checkpoint files and the Python virtual environment are excluded from this structure.

## 6. Project Implementation

### A. Data Collection and Preparation
- Collected Karnataka tomato market-price records from the AGMARKNET dataset.
- Stored the source CSV files in the project data directory.
- Validated records and converted arrival dates into the correct date format.

### B. Google BigQuery
- Created the Google Cloud project and BigQuery dataset.
- Uploaded the raw tomato market-price data.
- Created a curated Ramanagara tomato-price table.
- Partitioned the curated table by arrival date and clustered it by grade.

### C. MongoDB Atlas
- Connected Python applications to MongoDB Atlas.
- Transferred curated data from BigQuery.
- Loaded the complete 673-record dataset into MongoDB.
- Created indexes on arrival date and market.
- Performed aggregation and analytical queries.
- Compared indexed and unindexed query execution.

### D. Kafka and Spark Streaming
- Configured Apache Kafka.
- Created the `mandi-prices` topic.
- Implemented a Python Kafka producer.
- Implemented Spark Structured Streaming to consume and process incoming records.
- Tested raw record processing, one-minute average aggregation, and high-price alerts.

**Note:** Full processing of all 673 producer records should be verified before claiming complete batch-streaming execution.

### E. Interactive Dashboard
Developed a Streamlit dashboard connected to MongoDB Atlas.

The dashboard includes:
1. Daily Tomato Modal Price Trend
2. Market-wise Price Comparison
3. High Price Alerts
4. ML Price Forecasting
5. Seven-Day Tomato Price Forecast
6. Market Data Records

The dashboard successfully loaded all 673 valid records across 9 markets.

### F. Machine Learning Forecasting
- Implemented Random Forest Regression.
- Evaluated model performance using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).
- Generated a seven-day forecast using the historical Ramanagara data.

## 7. Results

### Dataset and Dashboard

| Metric | Result |
|---|---:|
| Total records | 673 |
| Number of markets | 9 |
| Average modal price | ₹1,924.81 |
| Minimum modal price | ₹500 |
| Maximum modal price | ₹6,000 |
| High-price alert records | 205 |

### Forecasting Model

| Metric | Result |
|---|---:|
| Algorithm | Random Forest Regression |
| Training records | 240 |
| Testing records | 61 |
| MAE | ₹413.69 |
| RMSE | ₹462.72 |

The model generated a seven-day forecast based on the available historical Ramanagara data.

### MongoDB Index Performance

The indexed query examined 29 documents, compared with 160 documents for the unindexed query. This represents approximately 82% fewer documents examined.

## 8. Running the Dashboard

Activate the project's Python virtual environment from the project root:

```powershell
.venv\Scripts\Activate.ps1
```

Run the dashboard:

```powershell
python -m streamlit run DASHBOARD/app_corrected.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

## 9. Running the Forecasting Script

From the project root:

```powershell
python FORECASTING/price_forecasting.py
```

The forecasting folder contains the model evaluation results and seven-day forecast output.

## 10. Important Notes and Limitations

- The historical source dataset covers 2025; it does not represent live market prices for November 2026.
- The seven-day forecast is based on historical Ramanagara records and should not be interpreted as a live market forecast.
- Model performance metrics describe the tested historical dataset and do not guarantee future prediction accuracy.
- Complete Kafka producer processing of all 673 records requires final verification.
- Database credentials and API keys must be kept private and must not be committed to GitHub.

## 11. Conclusion

The project demonstrates an integrated Big Data analytics workflow for agricultural market-price intelligence. It combines data collection, cloud data warehousing, NoSQL database analytics, stream processing, interactive visualisation, and machine learning forecasting.

The system provides a foundation for understanding historical agricultural price movements and supporting data-driven market analysis.