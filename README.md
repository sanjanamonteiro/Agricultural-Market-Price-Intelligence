# Agricultural Market Price Intelligence and Short-Term Crop Price Forecasting Using Big Data Analytics

## 1. Project Overview

This project develops an end-to-end Big Data analytics system for analysing agricultural market prices, identifying historical tomato price trends, comparing prices across markets, detecting high-price records, and generating short-term price forecasts.

The system integrates cloud data warehousing, NoSQL storage, automated ETL, real-time stream processing, interactive visualisation, and machine learning.

## 2. Objectives

- Collect and analyse agricultural market-price data.
- Store and process structured data using Google BigQuery.
- Transfer curated data into MongoDB Atlas.
- Automate the ETL process.
- Implement real-time data streaming using Apache Kafka and Spark Structured Streaming.
- Develop an interactive dashboard using Streamlit.
- Forecast short-term tomato prices using machine learning.
- Evaluate model performance using MAE and RMSE.

## 3. Technologies Used

| Category | Technology |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Cloud Data Warehouse | Google BigQuery |
| NoSQL Database | MongoDB Atlas |
| ETL | Python, BigQuery, MongoDB |
| Stream Processing | Apache Kafka, Apache Spark |
| Dashboard | Streamlit |
| Machine Learning | Random Forest Regression |
| Version Control | Git and GitHub |
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

The dataset contains arrival date, commodity, district, grade, market, minimum price, maximum price, modal price, state, and variety.

## 5. Project Structure

```text
Agricultural_Market_Price_Intelligence/
│
├── DASHBOARD/
│   └── app_corrected.py
│
├── DATA/
│   └── RAW/
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
│   ├── Project_Report.md
│   ├── architecture_diagram.md
│   └── Screenshots/
│
├── SCRIPTS/
│   └── bigquery_queries.sql
│
├── requirements.txt
├── run_etl.bat
├── transfer_bigquery_to_mongodb.py
└── .gitignore
```

Private credentials, environment files, virtual environments, and generated checkpoint files are excluded from version control.

## 6. Project Implementation

### A. Data Collection and Preparation

- Collected Karnataka tomato market-price records from AGMARKNET.
- Stored source CSV files in the project data directory.
- Validated records and converted arrival dates into the correct date format.
- Performed data-quality checks.

### B. Google BigQuery

- Created a Google Cloud project and BigQuery dataset.
- Uploaded the raw tomato market-price data.
- Created a curated Ramanagara tomato-price table.
- Partitioned the curated table by arrival date and clustered it by grade.
- Executed eight analytical SQL queries.

### C. MongoDB Atlas

- Connected Python applications to MongoDB Atlas.
- Transferred curated data from BigQuery.
- Stored the full dataset and curated Ramanagara records.
- Created indexes on relevant fields.
- Performed analytical and aggregation queries.
- Compared indexed and unindexed query execution.

### D. Automated ETL

- Developed a Python-based BigQuery-to-MongoDB transfer process.
- Created a Windows batch file to execute the ETL script.
- Configured Windows Task Scheduler for automated execution.
- Verified a successful scheduled task execution.

### E. Kafka and Spark Streaming

- Configured Apache Kafka.
- Created the `mandi-prices` topic.
- Implemented a Python Kafka producer.
- Implemented Spark Structured Streaming to consume and process incoming records.
- Tested raw record processing, one-minute window aggregation, and high-price alerts.

The real-time functionality was verified using test events. Complete processing of all historical producer records should not be interpreted as live market-data ingestion.

### F. Interactive Dashboard

Developed a Streamlit dashboard connected to MongoDB Atlas.

Dashboard features:
1. Daily tomato modal-price trend.
2. Market-wise price comparison.
3. High-price records.
4. Machine-learning forecasting.
5. Seven-day price forecast.
6. Market data records.

The dashboard successfully loaded the 673-record dataset across nine markets.

### G. Machine Learning Forecasting

- Implemented Random Forest Regression.
- Evaluated performance using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).
- Generated a seven-day forecast using historical Ramanagara data.

## 7. Results

### Dataset Statistics

| Metric | Result |
|---|---:|
| Total records | 673 |
| Number of markets | 9 |
| Average modal price | ₹1,924.81 |
| Minimum modal price | ₹500 |
| Maximum modal price | ₹6,000 |
| Historical records above ₹2,000 | 205 |

### Forecasting Model

| Metric | Result |
|---|---:|
| Algorithm | Random Forest Regression |
| Training records | 240 |
| Testing records | 61 |
| MAE | ₹413.69 |
| RMSE | ₹462.72 |

The seven-day forecast is based on historical Ramanagara data and is not a live November 2026 market prediction.

### MongoDB Index Performance

The indexed query examined 29 documents, compared with 160 documents for the unindexed query. This represents approximately 82% fewer documents examined.

The indexed query did not demonstrate a faster execution time on this small collection. The comparison demonstrates reduced document scanning rather than a measured speed improvement.

## 8. Installation and Setup

### Prerequisites

- Python
- Git
- Google Cloud / BigQuery access
- MongoDB Atlas account
- Apache Kafka
- Apache Spark
- Java
- Visual Studio Code

### Clone the Repository

```bash
git clone https://github.com/sanjanamonteiro/Agricultural-Market-Price-Intelligence.git
cd Agricultural-Market-Price-Intelligence
```

### Install Python Dependencies

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Configure Credentials

Configure Google Cloud authentication and MongoDB Atlas connection details using the credential configuration expected by the project scripts.

Do not upload passwords, API keys, service-account JSON files, or private environment files to GitHub.

## 9. Running the Dashboard

From the project root:

```powershell
python -m streamlit run DASHBOARD/app_corrected.py
```

Open the local URL displayed in the terminal.

## 10. Running the Forecasting Script

```powershell
python FORECASTING/price_forecasting.py
```

The forecasting directory contains the model evaluation and forecast outputs.

## 11. Running the ETL Process

From the project root, execute:

```powershell
.\run_etl.bat
```

The batch file runs the BigQuery-to-MongoDB transfer script using the project's virtual environment.

The automated execution is configured through Windows Task Scheduler.

## 12. SQL Queries and Documentation

Eight analytical BigQuery SQL queries are available in:

`SCRIPTS/bigquery_queries.sql`

The detailed project report contains the business questions, query descriptions, sample outputs, and execution-time documentation.

Additional implementation details and evidence are available in:

- `DOCS/Project_Report.md`
- `DOCS/architecture_diagram.md`
- `DOCS/Screenshots/`

## 13. Important Notes and Limitations

- The historical source dataset covers 2025 and does not represent live market prices for November 2026.
- The seven-day forecast is based on historical Ramanagara records.
- Model performance metrics describe the tested historical dataset and do not guarantee future prediction accuracy.
- Real-time streaming was verified using test events.
- Database credentials and API keys must remain private.
- The project uses a limited historical dataset and can be extended with larger and continuously updated datasets.

## 14. Conclusion

The project demonstrates an integrated Big Data analytics workflow for agricultural market-price intelligence. It combines data collection, cloud data warehousing, NoSQL database analytics, automated ETL, stream processing, interactive visualisation, and machine learning forecasting.

The system provides a foundation for understanding historical agricultural price movements and supporting data-driven market analysis.

## 15. GitHub Repository

Source code, SQL scripts, documentation, and implementation evidence:

https://github.com/sanjanamonteiro/Agricultural-Market-Price-Intelligence
