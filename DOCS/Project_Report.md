
# AGRICULTURAL MARKET PRICE INTELLIGENCE AND SHORT-TERM CROP PRICE FORECASTING USING BIG DATA ANALYTICS

## 1. INTRODUCTION

Agriculture plays an important role in the Indian economy. Farmers depend on agricultural markets (Mandis) to sell their crops. However, market prices frequently change due to demand, supply, seasonal variations, and other market conditions.

The Agricultural Market Price Intelligence and Short-Term Crop Price Forecasting project aims to analyze historical agricultural market prices and provide useful insights through Big Data technologies.

The project uses daily commodity price data collected from the AGMARKNET platform through data.gov.in. The collected data is processed, cleaned, stored, analyzed, and visualized using different technologies.

The system also uses Apache Kafka and Apache Spark Structured Streaming to demonstrate real-time processing of market price records. Machine Learning techniques are applied to historical price data to generate short-term price forecasts.

The project provides an integrated platform for understanding market price trends, comparing prices across markets, identifying high-price records, and forecasting future prices.

## 2. PROBLEM STATEMENT

Agricultural market prices fluctuate frequently, making it difficult for farmers and other stakeholders to understand price trends and make informed decisions.

Traditional methods of analyzing market prices often involve manual processing and limited historical comparisons. They may not provide efficient large-scale data processing, real-time monitoring, or forecasting capabilities.

Therefore, there is a need for a data-driven system that can collect, process, store, analyze, and visualize agricultural market price information using Big Data technologies and Machine Learning.

## 3. OBJECTIVES

1. To collect agricultural market price data from the AGMARKNET platform.
2. To clean, validate, and preprocess the collected data.
3. To store and analyze large datasets using Google BigQuery.
4. To manage structured market price records using MongoDB.
5. To develop an interactive dashboard using Streamlit.
6. To implement real-time data processing using Apache Kafka and Apache Spark Structured Streaming.
7. To identify market records with modal prices above ₹2,000.
8. To develop a Machine Learning model for short-term crop price forecasting.
9. To provide useful insights into agricultural market price trends.

## 4. DATASET DESCRIPTION

The dataset used in this project was obtained from the AGMARKNET platform through data.gov.in.

**Dataset:** Variety-wise Daily Market Prices Data of Commodity

**Dataset selection:**
- State: Karnataka
- Commodity: Tomato
- Period: 1 January 2025 to 31 December 2025
- Total records: 673
- Number of attributes: 11
- Number of markets: 9

The dataset contains the following attributes:

1. Arrival_Date
2. Commodity
3. Commodity_Code
4. District
5. Grade
6. Market
7. Max_Price
8. Min_Price
9. Modal_Price
10. State
11. Variety

The dataset provides daily minimum, maximum, and modal prices of tomatoes across different agricultural markets.

## 5. METHODOLOGY

The project follows a structured Big Data analytics workflow.

### 5.1 Data Collection

Historical agricultural market price records were collected from data.gov.in using the AGMARKNET dataset.

### 5.2 Data Preprocessing

Python was used to inspect, clean, and validate the dataset. Data types, missing values, duplicate records, and price fields were checked before further processing.

### 5.3 Big Data Storage and Processing

Google BigQuery was used to store and analyze the historical market price dataset. A curated table was created for Ramanagara tomato prices, using date partitioning and grade clustering.

### 5.4 Database Management

MongoDB was used to store agricultural price records in collections for efficient retrieval and analysis.

### 5.5 Data Visualization

A Streamlit dashboard was developed to display market price trends, market comparisons, high-price alerts, historical records, and forecast results.

### 5.6 Machine Learning Forecasting

A Machine Learning forecasting model was trained using historical market price data. The model was evaluated using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

### 5.7 Real-Time Data Streaming

Apache Kafka was used to receive market price records through the `mandi-prices` topic. Apache Spark Structured Streaming processed the incoming records to display raw data, calculate one-minute market price aggregations, and identify high-price alerts.

## 6. TECHNOLOGIES USED

The project integrates several technologies for data collection, processing, storage, visualization, and forecasting.

| Technology | Purpose |
|---|---|
| Python | Data preprocessing and analysis |
| Google BigQuery | Large-scale data storage and SQL analytics |
| MongoDB | NoSQL database storage and retrieval |
| Apache Kafka | Real-time data ingestion |
| Apache Spark Structured Streaming | Real-time stream processing |
| Streamlit | Interactive analytics dashboard |
| Machine Learning | Short-term price forecasting |
| Git and GitHub | Version control and project management |

## 7. IMPLEMENTATION AND RESULTS

### 7.1 Dataset Analysis

A total of 673 tomato market price records from Karnataka were processed.

The overall dataset analysis produced the following results:

- Total records: 673
- Average modal price: ₹1,924.81
- Minimum modal price: ₹500
- Maximum modal price: ₹6,000
- Number of markets: 9

### 7.2 BigQuery Analysis

The historical dataset was stored in Google BigQuery.

A curated Ramanagara tomato dataset containing 284 records was analyzed. The average modal price for these records was approximately ₹1,603.70.

A separate FAQ-grade curated dataset contained 160 records, with an average modal price of approximately ₹1,210.63.

The curated table used date partitioning and grade clustering to organize the data for analytical queries.

### 7.3 MongoDB Analysis

The processed agricultural market price records were stored in MongoDB.

The database contained:
- 673 Karnataka tomato price records.
- 160 Ramanagara FAQ-grade records.
- Records from 9 agricultural markets.

An indexed query examined 29 documents compared with 160 documents in the unindexed comparison, demonstrating reduced document scanning.

### 7.4 Machine Learning Forecasting

A forecasting model was trained and evaluated using historical market price data.

Model evaluation results:

- Training records: 240
- Testing records: 61
- Mean Absolute Error (MAE): ₹413.69
- Root Mean Squared Error (RMSE): ₹462.72

The model also generated a seven-day forecast based on the available historical Ramanagara price data.

**Note:** These forecasts are based on historical data and should not be interpreted as live November 2026 market predictions.

### 7.5 Dashboard Implementation

An interactive Streamlit dashboard was developed to present:
- Historical daily modal price trends.
- Market-wise price comparisons.
- High-price alerts.
- Machine Learning forecasting results.
- Seven-day forecast visualization.
- Historical market price records.

The dashboard identified 205 historical records with modal prices above ₹2,000.

### 7.6 Real-Time Kafka and Spark Implementation

Apache Kafka and Apache Spark Structured Streaming were integrated to demonstrate real-time agricultural market price processing.

A test record for Ramanagara tomato prices was successfully sent through the Kafka topic `mandi-prices`.

The incoming record contained a modal price of ₹3,000.

Spark successfully performed three operations:

1. **Raw Record Processing:** Parsed and displayed all 11 fields of the incoming record.
2. **Window Aggregation:** Calculated an average modal price of ₹3,000 with a record count of 1 in the one-minute window.
3. **High-Price Alert:** Detected the ₹3,000 record because it exceeded the configured ₹2,000 threshold.

This successful test verified the Kafka-to-Spark streaming workflow.

## 8. CONCLUSION

The project, Agricultural Market Price Intelligence and Short-Term Crop Price Forecasting Using Big Data Analytics, successfully demonstrates the use of Big Data technologies and Machine Learning for agricultural market price analysis.

Historical tomato market price data from Karnataka was collected, cleaned, processed, and stored using Python, Google BigQuery, and MongoDB.

An interactive Streamlit dashboard was developed to provide insights into historical price trends, market comparisons, high-price records, and forecast results.

The integration of Apache Kafka and Apache Spark Structured Streaming demonstrated real-time data ingestion, processing, window-based aggregation, and high-price alert generation.

The forecasting model was evaluated using MAE and RMSE to measure its prediction error.

Overall, the project demonstrates how Big Data analytics and Machine Learning can support better understanding of agricultural market price patterns and provide useful information for decision-making.

## 9. LIMITATIONS

1. The historical dataset is limited to Karnataka tomato market prices for the selected period.
2. The forecasting model depends on the availability and quality of historical records.
3. The real-time streaming demonstration uses test records rather than a continuously connected live AGMARKNET feed.
4. Forecast accuracy may be affected by seasonal changes, weather conditions, demand, supply, and other external factors.
5. The forecasting results should be treated as estimates rather than guaranteed future market prices.

## 10. FUTURE ENHANCEMENTS

1. Extend the system to include multiple agricultural commodities and states.
2. Integrate a continuously updated live agricultural market price data source.
3. Improve forecasting accuracy using advanced time-series and Machine Learning models.
4. Incorporate weather, rainfall, demand, and supply information.
5. Develop farmer-friendly mobile and web applications.
6. Add automated notifications for significant market price changes.
7. Deploy the complete system on a cloud platform for wider accessibility.

## 11. REFERENCES

1. AGMARKNET – Agricultural Marketing Information Network.
2. data.gov.in – Open Government Data Platform, India.
3. Google Cloud BigQuery Documentation.
4. MongoDB Documentation.
5. Apache Kafka Documentation.
6. Apache Spark Structured Streaming Documentation.
7. Streamlit Documentation.
8. Python Documentation.
9. Scikit-learn Documentation.

## 12. BIG DATA CHARACTERISTICS

The project demonstrates the three major characteristics of Big Data:

### 12.1 Volume
- The raw dataset contains 673 agricultural market price records.
- Each record contains 11 attributes.
- A curated Ramanagara FAQ-grade dataset contains 160 records.
- The data is stored in Google BigQuery and MongoDB Atlas.

### 12.2 Velocity
- Historical records are replayed through Apache Kafka to simulate incoming market price events.
- Apache Spark Structured Streaming processes incoming records continuously.
- One-minute window aggregation and high-price alerts are generated during streaming.

### 12.3 Variety
The project primarily uses structured agricultural market data containing dates, market names, commodity details, grades, and numerical price values.
JSON-formatted test records are also used for Kafka streaming.

## 13. AUTOMATED ETL PIPELINE

### 13.1 ETL Process

The project implements an ETL pipeline to transfer curated agricultural market price records from Google BigQuery to MongoDB Atlas.

The process consists of:

1. **Extract:** Retrieve curated records from BigQuery.
2. **Transform:** Prepare records for MongoDB storage and maintain the required data structure.
3. **Load:** Insert or update records in the MongoDB collection.

### 13.2 Automation

The ETL process is executed using the following components:

- Python script: `transfer_bigquery_to_mongodb.py`
- Batch file: `run_etl.bat`
- Automation tool: Windows Task Scheduler
- Scheduled task: `AgriMarket_ETL_Automation`
- Configured frequency: Daily at 8:00 AM.

The scheduled task was successfully created and tested.

### 13.3 ETL Verification Results

| Metric | Result |
|---|---:|
| Records fetched from BigQuery | 160 |
| Records processed | 160 |
| New records inserted during verification | 0 |
| Existing records updated during verification | 0 |
| Scheduled task result code | 0 |

The zero insertions and updates during the verification run indicate that the existing records were already present and unchanged.

The successful execution confirms the BigQuery-to-MongoDB ETL workflow.

## 14. BIGQUERY SQL QUERY DOCUMENTATION

Eight analytical SQL queries were executed in Google BigQuery.

### Query 1: Market-Wise Price Analysis

**Business question:** Which markets have the highest average tomato modal prices?

```sql
SELECT
    Market,
    COUNT(*) AS Total_Records,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price,
    MIN(Modal_Price) AS Minimum_Price,
    MAX(Modal_Price) AS Maximum_Price
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
GROUP BY Market
HAVING COUNT(*) >= 10
ORDER BY Average_Modal_Price DESC;

SELECT
    EXTRACT(MONTH FROM Arrival_Date) AS Month_Number,
    FORMAT_DATE('%B', Arrival_Date) AS Month_Name,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price,
    MIN(Modal_Price) AS Minimum_Price,
    MAX(Modal_Price) AS Maximum_Price,
    COUNT(*) AS Total_Records
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
GROUP BY Month_Number, Month_Name
ORDER BY Month_Number;

SELECT
    Grade,
    COUNT(*) AS Total_Records,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price,
    MIN(Modal_Price) AS Minimum_Price,
    MAX(Modal_Price) AS Maximum_Price
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
GROUP BY Grade
ORDER BY Average_Modal_Price DESC;

SELECT
    Market,
    COUNT(*) AS Above_Average_Records,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
WHERE Modal_Price > (
    SELECT AVG(Modal_Price)
    FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
)
GROUP BY Market
ORDER BY Average_Modal_Price DESC;

WITH MarketStats AS (
    SELECT
        Market,
        COUNT(*) AS Total_Records,
        AVG(Modal_Price) AS Average_Price
    FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
    GROUP BY Market
),
OverallStats AS (
    SELECT AVG(Modal_Price) AS Overall_Average
    FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
)
SELECT
    M.Market,
    M.Total_Records,
    ROUND(M.Average_Price, 2) AS Average_Price,
    ROUND(O.Overall_Average, 2) AS Overall_Average,
    CASE
        WHEN M.Average_Price > O.Overall_Average
        THEN 'Above Average'
        ELSE 'Below Average'
    END AS Market_Performance
FROM MarketStats M
CROSS JOIN OverallStats O
ORDER BY M.Average_Price DESC;

SELECT
    Market,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price,
    RANK() OVER (
        ORDER BY AVG(Modal_Price) DESC
    ) AS Market_Rank
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
GROUP BY Market
ORDER BY Market_Rank;

SELECT
    Market,
    Arrival_Date,
    Modal_Price,
    LAG(Modal_Price) OVER (
        PARTITION BY Market
        ORDER BY Arrival_Date
    ) AS Previous_Day_Price,
    Modal_Price - LAG(Modal_Price) OVER (
        PARTITION BY Market
        ORDER BY Arrival_Date
    ) AS Price_Change
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
ORDER BY Market, Arrival_Date;

SELECT
    Arrival_Date,
    Market,
    Modal_Price,
    CASE
        WHEN Modal_Price >= 5000 THEN 'Very High Price'
        WHEN Modal_Price >= 3000 THEN 'High Price'
        ELSE 'Normal Price'
    END AS Price_Category
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
WHERE Modal_Price >= 3000
ORDER BY Modal_Price DESC;

