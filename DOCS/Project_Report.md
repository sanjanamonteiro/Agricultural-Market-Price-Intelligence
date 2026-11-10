# AGRICULTURAL MARKET PRICE INTELLIGENCE AND SHORT-TERM CROP PRICE FORECASTING USING BIG DATA ANALYTICS

## PROJECT REPORT

**Project title:** Agricultural Market Price Intelligence and Short-Term Crop Price Forecasting Using Big Data Analytics  
**Course:** Big Data Analytics  
**Course code:** 23BSDA5D54  
**Academic year:** 2026–2027  
**Dataset:** AGMARKNET – Variety-wise Daily Market Prices Data of Commodity  
**Repository:** https://github.com/sanjanamonteiro/Agricultural-Market-Price-Intelligence

### Project team

| Role | Details |
|---|---|
| Team member 1 | Sanjana Monteiro — 24BSR18038 |
| Team member 2 | Tharun Ashok — 24BSR18043 |

*The project team consists of two members.*

---

# 1. INTRODUCTION

Agriculture plays an important role in the Indian economy. Farmers, traders, and other stakeholders depend on agricultural markets (Mandis) to sell and purchase crops. However, agricultural market prices fluctuate due to demand, supply, seasonal variations, transportation, weather conditions, and other market factors.

The project **Agricultural Market Price Intelligence and Short-Term Crop Price Forecasting Using Big Data Analytics** develops an end-to-end analytics system to study agricultural market prices, identify price trends, compare markets, detect high-price records, and generate short-term price forecasts.

The system uses public agricultural market-price data obtained through the AGMARKNET dataset on the Government of India's Open Government Data Platform. Python is used for data preparation and integration, Google BigQuery is used as the cloud data warehouse, and MongoDB Atlas is used as the NoSQL database.

The project also demonstrates automated ETL, Apache Kafka-based data ingestion, Apache Spark Structured Streaming, an interactive Streamlit dashboard, and machine-learning-based price forecasting.

The streaming component replays historical records and uses test events to demonstrate continuous processing. It is a streaming simulation and not a direct live connection to an AGMARKNET market feed.

# 2. PROBLEM STATEMENT

Agricultural market prices change frequently across markets and dates. Understanding these changes using manual methods can be time-consuming and may not provide sufficient analytical insights.

There is a need for a system that can:

- Collect and validate agricultural market-price data.
- Store structured data in a cloud data warehouse.
- Perform analytical queries to identify price patterns.
- Transfer curated data into a NoSQL database.
- Automate data movement between storage systems.
- Process incoming market-price events continuously.
- Identify high-price records and calculate window-based market statistics.
- Present historical trends and forecasts through an interactive dashboard.

This project addresses these requirements by integrating Big Data technologies, cloud storage, NoSQL databases, streaming, analytics, and machine learning into one workflow.

# 3. PROJECT OBJECTIVES

1. Collect agricultural market-price data from AGMARKNET through data.gov.in.
2. Clean, validate, and prepare the dataset for analysis.
3. Store raw and curated agricultural price data in Google BigQuery.
4. Perform analytical SQL queries using aggregation, filtering, subqueries, CTEs, and window functions.
5. Transfer curated records from BigQuery to MongoDB Atlas.
6. Automate the ETL process using Python and Windows Task Scheduler.
7. Implement data ingestion using Apache Kafka.
8. Process streaming records using Apache Spark Structured Streaming.
9. Perform continuous record processing, window aggregation, and high-price alert detection.
10. Develop an interactive dashboard using Streamlit.
11. Build and evaluate a short-term tomato-price forecasting model.
12. Apply data organization and indexing techniques and evaluate their performance.

# 4. DATASET DESCRIPTION

## 4.1 Dataset source

- **Source platform:** Government of India Open Government Data Platform.
- **Data source:** AGMARKNET.
- **Dataset name:** Variety-wise Daily Market Prices Data of Commodity.
- **Commodity selected:** Tomato.
- **State:** Karnataka.
- **Period:** 1 January 2025 to 31 December 2025.

## 4.2 Dataset size

| Attribute | Value |
|---|---:|
| Total records | 673 |
| Number of attributes | 11 |
| Number of markets | 9 |
| Commodity | Tomato |
| State | Karnataka |
| Period | 2025 |

## 4.3 Dataset attributes

| Attribute | Description |
|---|---|
| Arrival_Date | Date of commodity arrival |
| Commodity | Commodity name |
| Commodity_Code | Commodity identification code |
| District | District in which the market is located |
| Grade | Grade or quality classification |
| Market | Agricultural market name |
| Max_Price | Maximum recorded price |
| Min_Price | Minimum recorded price |
| Modal_Price | Modal market price |
| State | State name |
| Variety | Commodity variety |

The dataset contains date, categorical, and numerical fields. The minimum, maximum, and modal prices are used for market-price analysis.

## 4.4 Dataset scope

The project uses the 673-record Karnataka tomato dataset for the overall BigQuery analysis and dashboard. A separate curated dataset containing 160 Ramanagara FAQ-grade records is used for the MongoDB ETL and query demonstrations.

The 160-record collection must not be confused with the full 673-record dataset. They represent different scopes of analysis.

# 5. BIG DATA CHARACTERISTICS

The project demonstrates the three major Big Data characteristics: Volume, Velocity, and Variety.

## 5.1 Volume

- The selected historical dataset contains 673 records.
- Each record contains 11 attributes.
- The full dataset covers nine agricultural markets.
- A separate curated Ramanagara FAQ-grade dataset contains 160 records.
- Google BigQuery stores and analyzes the historical dataset, while MongoDB Atlas stores the curated records used in the NoSQL demonstration.

The current dataset is a modest academic-scale dataset. The architecture demonstrates technologies and processing methods that can be extended to larger datasets.

## 5.2 Velocity

- The Kafka producer sends agricultural market-price records to the `mandi-prices` topic.
- A one-second delay between records simulates an incoming data feed.
- Spark Structured Streaming continuously reads records from Kafka.
- The Spark queries use a ten-second processing trigger.
- A one-minute window is used for market-wise aggregation.
- High-price records are detected as events arrive.

The streaming implementation demonstrates simulated data velocity. It does not represent a continuously connected live AGMARKNET feed.

## 5.3 Variety

The dataset contains multiple data types:

- Date fields such as `Arrival_Date`.
- Categorical fields such as `Commodity`, `Market`, `District`, `Grade`, and `Variety`.
- Numerical fields such as `Min_Price`, `Max_Price`, and `Modal_Price`.
- JSON-formatted records used for Kafka message transmission.

# 6. SYSTEM ARCHITECTURE

The architecture combines historical data processing and simulated real-time streaming.

## 6.1 Architecture flow

1. Agricultural market-price data is collected from AGMARKNET/data.gov.in.
2. Python is used for data inspection, cleaning, and validation.
3. The historical dataset is stored in Google BigQuery.
4. A curated Ramanagara dataset is created using BigQuery.
5. Curated records are transferred from BigQuery to MongoDB Atlas.
6. Python and Windows Task Scheduler automate the ETL process.
7. Historical CSV records are replayed through a Kafka producer.
8. Apache Kafka receives the records through the `mandi-prices` topic.
9. Spark Structured Streaming processes the incoming events.
10. Streaming output includes raw records, one-minute aggregations, and high-price alerts.
11. MongoDB data and forecasting outputs are presented through a Streamlit dashboard.

## 6.2 Architecture diagram

The architecture diagram is maintained separately in:

`DOCS/architecture_diagram.md`

It contains the Mermaid flowchart showing the AGMARKNET source, Python preparation, BigQuery, MongoDB, ETL, forecasting, dashboard, Kafka, Spark, and streaming outputs.

## 6.3 Technology stack

| Technology | Purpose |
|---|---|
| Python | Data preparation, integration, and analytics |
| Pandas and NumPy | Data handling and numerical operations |
| Google BigQuery | Cloud data warehouse and SQL analytics |
| MongoDB Atlas | NoSQL document storage |
| PyMongo | Python integration with MongoDB |
| Apache Kafka | Streaming data ingestion |
| Apache Spark Structured Streaming | Continuous stream processing |
| Streamlit | Interactive dashboard |
| Scikit-learn | Machine-learning forecasting |
| Git and GitHub | Version control and source-code management |
| Visual Studio Code | Development environment |
| Windows Task Scheduler | Automated ETL execution |

# 7. DATA PREPROCESSING AND QUALITY VALIDATION

## 7.1 Data preparation

The agricultural market-price dataset was prepared before loading and analysis.

The preparation and validation workflow included:

1. Inspecting the dataset structure and field names.
2. Checking the required agricultural price attributes.
3. Checking missing values in the selected dataset.
4. Checking the price fields used for analysis.
5. Ensuring that arrival dates could be used in date-based analysis.
6. Maintaining consistent field names for the BigQuery schema.
7. Preparing the curated Ramanagara FAQ-grade dataset for downstream storage and analysis.
8. Preparing records in JSON format for Kafka transmission.

The implemented scripts also apply type conversion and validation at the relevant processing stages. The dashboard converts arrival dates to datetime values, removes incomplete rows, and standardizes market values as strings. The forecasting script converts price fields to numeric values, filters Ramanagara records, removes rows missing the required date or modal price, aggregates daily prices, fills the daily date sequence using time interpolation, and creates lag, rolling-average, and calendar features. The Spark streaming script defines a JSON schema, converts price fields to numeric values and arrival dates to date values, and filters records with missing modal prices or market names.

## 7.2 Data-quality verification

The initial BigQuery data-quality verification returned 673 records. The missing-field checks for the selected dataset returned zero missing values.

| Validation item | Verified result |
|---|---|
| Total records in selected dataset | 673 |
| Number of attributes | 11 |
| Missing-field check | 0 missing values reported |
| Number of markets | 9 |
| Commodity | Tomato |
| State | Karnataka |

The curated Ramanagara FAQ-grade table contains 160 records.

## 7.3 Data preparation limitations

The report does not claim that every possible data-cleaning operation was performed. In particular, no unsupported claim is made that a specific number of duplicate or noisy records was removed.

The project uses the validated dataset and its curated subset for the subsequent BigQuery, MongoDB, forecasting, and dashboard operations.

# 8. GOOGLE BIGQUERY CLOUD DATA WAREHOUSE

## 8.1 Cloud storage

Google BigQuery was selected as the cloud data warehouse because it supports SQL-based analysis of structured datasets without requiring the primary analytical dataset to remain only on a local computer.

**Google Cloud project:** `agrimarketanalytics`  
**BigQuery dataset:** `mandi_price_data`  
**Main table:** `tomato_karnataka_2025`

The main table contains the 673 Karnataka tomato market-price records.

## 8.2 Curated dataset

A separate curated table was created:

`agrimarketanalytics.mandi_price_data.ramanagara_tomato_curated`

The curated table contains 160 Ramanagara FAQ-grade records.

| Property | Configuration |
|---|---|
| Source | Karnataka tomato market-price dataset |
| Market | Ramanagara |
| Grade | FAQ |
| Records | 160 |
| Partitioning | `Arrival_Date` |
| Clustering | `Grade` |

The wider Ramanagara dataset before the FAQ-grade selection contained 284 records, with an average modal price of approximately ₹1,603.70. The 160-record FAQ subset had an average modal price of approximately ₹1,210.63.

## 8.3 Overall dataset statistics

| Metric | Result |
|---|---:|
| Total records | 673 |
| Number of markets | 9 |
| Average modal price | ₹1,924.81 |
| Minimum modal price | ₹500 |
| Maximum modal price | ₹6,000 |
| Records above ₹2,000 | 205 |

# 9. AUTOMATED ETL PIPELINE

## 9.1 Purpose

The ETL pipeline transfers curated agricultural market-price records from Google BigQuery to MongoDB Atlas.

The pipeline follows three stages:

- **Extract:** Retrieve the curated records from BigQuery.
- **Transform:** Prepare the retrieved records in the structure required for MongoDB storage.
- **Load:** Insert or update records in the MongoDB collection.

## 9.2 Implementation components

| Component | File or configuration |
|---|---|
| ETL script | `transfer_bigquery_to_mongodb.py` |
| Batch file | `run_etl.bat` |
| Scheduler | Windows Task Scheduler |
| Scheduled task | `AgriMarket_ETL_Automation` |
| Database | `agri_market_intelligence` |
| Collection | `ramanagara_tomato_prices` |
| Configured schedule | Daily at 8:00 AM |

The batch file executes the Python ETL script using the project's virtual environment.

## 9.3 ETL verification

The ETL process was executed and verified successfully. The transfer script reads the curated BigQuery table, converts date values into MongoDB-compatible ISO strings, and uses an ascending unique index on `Arrival_Date` with an upsert operation.

This upsert strategy prevents repeated insertion for the same arrival date in the curated collection. It assumes one document per arrival date; it is not a general-purpose duplicate-detection strategy for datasets containing multiple market or grade records on the same date.

| Metric | Result |
|---|---:|
| Records fetched from BigQuery | 160 |
| Records processed | 160 |
| New records inserted in verification run | 0 |
| Existing records updated in verification run | 0 |
| Scheduled task result code | 0 |

The zero insertions and updates in the verification run indicate that the records were already present and unchanged.

The Windows Task Scheduler task was configured for daily execution and its successful execution was verified.

## 9.4 ETL execution command

From the project root:

```powershell
.\run_etl.bat
```

The scheduled task provides automated execution rather than relying only on manual execution.

# 10. MONGODB ATLAS NOSQL DATABASE

## 10.1 Database selection

MongoDB Atlas was selected as the NoSQL database because it stores data in flexible JSON-like documents and supports filtering, aggregation, and indexing.

It is suitable for the project's structured and semi-structured agricultural market-price records.

## 10.2 Database details

| Property | Value |
|---|---|
| Database | `agri_market_intelligence` |
| Collection | `ramanagara_tomato_prices` |
| Collection records | 160 |
| Data source | Curated BigQuery table |
| Index | `Arrival_Date_1` |
| Index type | Ascending |

## 10.3 MongoDB query documentation

The following five queries are implemented in:

`MONGODB/mongodb_queries.py`

### MongoDB Query 1: Indexed date-range search

**Business question:** How many tomato price records are available for January 2025?

```python
query1 = {
    "Arrival_Date": {
        "$gte": "2025-01-01",
        "$lt": "2025-02-01"
    }
}

january_records = list(
    collection.find(query1, {"_id": 0})
    .hint("Arrival_Date_1")
    .limit(5)
)

print("January record count:", collection.count_documents(query1))
```

**Sample output:**

| Metric | Result |
|---|---:|
| January records | 29 |
| Sample records retrieved | 5 |
| Index keys examined | 29 |
| Documents examined | 29 |

**Execution time:** 49.201 ms (date-range count and sample-record retrieval; client-observed time).

### MongoDB Query 2: Overall price statistics

**Business question:** What are the average, minimum, and maximum modal prices in the curated dataset?

```python
result2 = list(collection.aggregate([
    {
        "$group": {
            "_id": None,
            "average_price": {"$avg": "$Modal_Price"},
            "minimum_price": {"$min": "$Modal_Price"},
            "maximum_price": {"$max": "$Modal_Price"},
            "total_records": {"$sum": 1}
        }
    }
]))

print(result2)
```

**Sample output:**

| Metric | Result |
|---|---:|
| Average modal price | ₹1,210.625 |
| Minimum price | ₹500 |
| Maximum price | ₹2,600 |
| Total records | 160 |

**Execution time:** 24.525 ms (client-observed aggregation time).

### MongoDB Query 3: Grade-wise price analysis

**Business question:** What is the average modal price and record count for each grade?

```python
result3 = list(collection.aggregate([
    {
        "$group": {
            "_id": "$Grade",
            "average_price": {"$avg": "$Modal_Price"},
            "record_count": {"$sum": 1}
        }
    },
    {
        "$sort": {"average_price": -1}
    }
]))

for record in result3:
    print(record)
```

**Sample output:**

| Grade | Average price | Records |
|---|---:|---:|
| FAQ | ₹1,210.625 | 160 |

**Execution time:** 24.660 ms (client-observed aggregation time).

### MongoDB Query 4: High-price record identification

**Business question:** Which tomato price records have a modal price greater than ₹2,000?

```python
query4 = {
    "Modal_Price": {"$gt": 2000}
}

high_price_records = list(
    collection.find(
        query4,
        {"_id": 0, "Arrival_Date": 1, "Market": 1,
         "Modal_Price": 1}
    ).sort("Modal_Price", -1).limit(10)
)

print("High-price record count:",
      collection.count_documents(query4))

for record in high_price_records:
    print(record)
```

**Sample output:**

| Metric | Result |
|---|---:|
| Records above ₹2,000 | 6 |
| Highest modal price | ₹2,600 |
| Date of highest-price record | 02-07-2025 |
| Other identified prices | ₹2,500 and ₹2,400 |

**Execution time:** 49.822 ms (high-price count and record retrieval; client-observed time).

### MongoDB Query 5: Monthly average price analysis

**Business question:** How do average, minimum, and maximum modal prices change month by month?

```python
result5 = list(collection.aggregate([
    {
        "$group": {
            "_id": {
                "$substrBytes": ["$Arrival_Date", 0, 7]
            },
            "average_price": {"$avg": "$Modal_Price"},
            "minimum_price": {"$min": "$Modal_Price"},
            "maximum_price": {"$max": "$Modal_Price"},
            "record_count": {"$sum": 1}
        }
    },
    {
        "$sort": {"_id": 1}
    }
]))

for record in result5:
    print(record)
```

**Sample output:**

| Month | Average price | Records |
|---|---:|---:|
| January 2025 | ₹1,222.41 | 29 |
| February 2025 | ₹1,197.50 | 20 |
| March 2025 | ₹632.61 | 23 |
| April 2025 | ₹1,029.63 | 27 |
| May 2025 | ₹1,178.33 | 30 |
| June 2025 | ₹1,779.31 | 29 |
| July 2025 | ₹2,500.00 | 2 |

**Execution time:** 25.046 ms (client-observed aggregation time).

## 10.4 MongoDB query summary

Five MongoDB queries were executed on the 160-record curated collection.

The queries demonstrate:

- Date-range filtering.
- Indexed retrieval.
- Statistical aggregation.
- Grade-wise grouping.
- High-price filtering.
- Monthly aggregation and sorting.

The five query executions completed successfully. Their measured client-observed times were:

| MongoDB query | Measured time |
|---|---:|
| Query 1 – Indexed January date search | 49.201 ms |
| Query 2 – Overall price statistics | 24.525 ms |
| Query 3 – Grade-wise aggregation | 24.660 ms |
| Query 4 – High-price identification | 49.822 ms |
| Query 5 – Monthly aggregation | 25.046 ms |

The timings represent the measured operations in the Python query script. For Queries 1 and 4, the measured operation includes the count and sample-record retrieval. These values are retained as observed; they are not estimates.

# 11. APACHE KAFKA DATA INGESTION

## 11.1 Purpose

Apache Kafka is used to receive agricultural market-price records as messages. The Python producer reads records from the historical CSV file and sends them to a Kafka topic.

This simulates an incoming market-price data feed.

## 11.2 Kafka configuration

| Property | Value |
|---|---|
| Kafka topic | `mandi-prices` |
| Configured broker | `localhost:9092` |
| Producer file | `STREAMING/kafka_price_producer.py` |
| Source file | `DATA/RAW/tomato_karnataka_2025.csv` |
| Message format | JSON |
| Replay delay | 1 second |

## 11.3 Producer operation

The Kafka producer:

1. Reads the CSV dataset.
2. Retrieves each row as a dictionary.
3. Prepares the record for JSON serialization.
4. Uses the market name as the Kafka message key.
5. Sends the record to the `mandi-prices` topic.
6. Waits for message acknowledgement.
7. Pauses for one second before sending the next record.

The producer supports replaying the historical dataset as a simulated stream.

# 12. APACHE SPARK STRUCTURED STREAMING

## 12.1 Purpose

Apache Spark Structured Streaming consumes the Kafka messages and performs continuous processing.

The Spark implementation contains three streaming queries:

1. Raw structured record processing.
2. One-minute market-wise price aggregation.
3. High-price alert detection.

## 12.2 Streaming configuration

| Configuration | Value |
|---|---|
| Kafka topic | `mandi-prices` |
| Kafka broker in script | `localhost:9092` |
| Spark application | `AgriMarketPriceIntelligence` |
| Spark master | `local[2]` |
| Shuffle partitions | 4 |
| Processing trigger | 10 seconds |
| Window duration | 1 minute |
| Watermark | 2 minutes |
| High-price threshold | ₹2,000 |
| Checkpoint directories | Separate directories for each query |

## 12.3 Data parsing and validation

The Spark script reads the Kafka message value and parses the JSON content using a defined schema.

It then:

- Converts the arrival date into a date field.
- Converts minimum, maximum, and modal prices into numerical values.
- Filters records with missing modal prices or missing market names.
- Adds Kafka event timestamps for window-based processing.

## 12.4 Streaming Query 1: Continuous raw record processing

**Business question:** Can incoming agricultural market-price records be continuously received, parsed, and displayed?

```python
raw_query = (
    parsed_stream.writeStream
    .queryName("MandiRawRecords")
    .format("console")
    .outputMode("append")
    .option("truncate", "false")
    .option("numRows", "10")
    .option("checkpointLocation", CHECKPOINT_ROOT + "/raw")
    .trigger(processingTime="10 seconds")
    .start()
)
```

**Sample output:** Incoming historical mandi-price records were parsed and displayed in the Spark console. The complete replay contained 673 records, processed in seven non-empty batches: six batches of 100 records and one batch of 73 records.

**Measured trigger execution time:** Average 1,538 ms; minimum 726 ms; maximum 4,810 ms across the seven non-empty batches. The configured processing trigger is 10 seconds; it is not the measured execution time.

## 12.5 Streaming Query 2: One-minute market-wise price aggregation

**Business question:** What is the average modal price and number of records received for each market within a one-minute window?

```python
windowed_prices = (
    parsed_stream
    .withWatermark("event_time", "2 minutes")
    .groupBy(
        window(col("event_time"), "1 minute"),
        col("Market")
    )
    .agg(
        avg("Modal_Price").alias("Average_Modal_Price"),
        count("*").alias("Record_Count")
    )
)

window_query = (
    windowed_prices.writeStream
    .queryName("MarketPriceAggregation")
    .format("console")
    .outputMode("update")
    .option("truncate", "false")
    .option("checkpointLocation", CHECKPOINT_ROOT + "/windowed")
    .trigger(processingTime="10 seconds")
    .start()
)
```

**Sample output from the replayed dataset:**

| Market | Example average modal price | Example record count |
|---|---:|---:|
| Binny Mill (F&V), Bangalore | ₹1,561.29 | 31 |
| Doddaballa Pur APMC | ₹2,372.73 | 11 |
| Channapatana APMC | ₹3,166.67 | 3 |
| Ramanagara APMC | ₹3,528.89 | 45 |

The aggregation grouped records into one-minute windows using Kafka event timestamps. These are examples from the actual streaming output, not a single manually created test event.

**Measured trigger execution time:** Average 2,688 ms; minimum 1,499 ms; maximum 6,667 ms across the seven non-empty batches. The configured processing trigger is 10 seconds; it is not the measured execution time.

## 12.6 Streaming Query 3: High-price alert detection

**Business question:** Can the system identify incoming tomato price records with a modal price greater than ₹2,000?

```python
price_alerts = (
    parsed_stream
    .filter(col("Modal_Price") > PRICE_ALERT_THRESHOLD)
    .select(
        "Arrival_Date",
        "Market",
        "Commodity",
        "Modal_Price",
        "District"
    )
)

alert_query = (
    price_alerts.writeStream
    .queryName("HighPriceAlerts")
    .format("console")
    .outputMode("append")
    .option("truncate", "false")
    .option("checkpointLocation", CHECKPOINT_ROOT + "/alerts")
    .trigger(processingTime="10 seconds")
    .start()
)
```

**Sample output:** The alert query successfully identified replayed records whose modal prices were strictly greater than ₹2,000. Actual alert values included ₹2,400, ₹3,400, ₹3,700, ₹5,200, and ₹6,000.

**Measured trigger execution time:** Average 1,368.29 ms; minimum 722 ms; maximum 3,708 ms across the seven non-empty batches. The configured processing trigger is 10 seconds; it is not the measured execution time.

## 12.7 Streaming verification

All three Structured Streaming queries were started successfully and processed the 673 records replayed through Kafka. Each query independently read the same topic and processed all 673 records in seven non-empty batches: 100 + 100 + 100 + 100 + 100 + 100 + 73. The windowed query also displayed an additional empty batch after the input had been exhausted; this was normal end-of-input behavior.

The measured trigger execution times across the seven non-empty batches were:

| Spark query | Average (ms) | Minimum (ms) | Maximum (ms) |
|---|---:|---:|---:|
| `MandiRawRecords` | 1,538 | 726 | 4,810 |
| `MarketPriceAggregation` | 2,688 | 1,499 | 6,667 |
| `HighPriceAlerts` | 1,368.29 | 722 | 3,708 |

The averages include the first batch's startup overhead. They are measured trigger execution times, not the configured 10-second processing interval.

The verification demonstrated:

- Kafka topic ingestion of 673 historical records.
- JSON schema parsing and field conversion.
- Raw structured record output.
- One-minute market-wise window aggregation.
- High-price filtering for modal prices greater than ₹2,000.
- Separate checkpoint directories for the three streaming queries.

The following screenshots are stored in `DOCS/Screenshots/`:

- `kafka_sample_records.png`
- `kafka_topic_verification.png`
- `spark_streaming_live_alert_verification.png`
- `spark_streaming_output.png`

The screenshots provide implementation evidence for Kafka and Spark processing.

# 13. QUERY OPTIMIZATION AND PERFORMANCE ANALYSIS

## 13.1 BigQuery partitioning

The curated BigQuery table `ramanagara_tomato_curated` was partitioned using `Arrival_Date`.

Partitioning organizes data by date and supports date-based filtering and retrieval.

## 13.2 BigQuery clustering

The curated table was clustered by `Grade`.

Clustering organizes records based on the selected field and supports queries that filter or group by grade.

## 13.3 MongoDB indexing

An ascending index was created on the `Arrival_Date` field.

**Index name:** `Arrival_Date_1`

The index was tested using a January 2025 date-range query.

## 13.4 Indexed versus collection-scan comparison

The comparison was recorded in `MONGODB/mongodb_results.txt`.

| Performance metric | Indexed search | Collection scan |
|---|---:|---:|
| Records found | 29 | 29 |
| Execution time | 169.0366 ms | 129.6801 ms |
| Keys examined | 29 | 0 |
| Documents examined | 29 | 160 |

## 13.5 Performance analysis

The indexed query examined 29 documents, while the collection scan examined all 160 documents.

The reduction in documents examined was approximately 81.9%.

However, the indexed query took longer in this particular test:

- Indexed search: 169.0366 ms.
- Collection scan: 129.6801 ms.

The collection scan was faster because the collection contained only 160 records. This demonstrates that indexing can reduce the amount of document scanning, but does not guarantee lower elapsed time for every small dataset or query.

The project therefore reports the actual measured result rather than claiming that the index improved execution time.

## 13.6 Optimization outcome

The project implemented:

- BigQuery date partitioning.
- BigQuery grade clustering.
- MongoDB ascending date indexing.

The MongoDB comparison demonstrated fewer documents examined with the index. The measured execution time was slower in that test, so a speed improvement was not demonstrated.

# 14. BIGQUERY SQL QUERY DOCUMENTATION

Eight analytical SQL queries were executed in Google BigQuery.

**Main table:** `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`

The complete query script is available at:

`SCRIPTS/bigquery_queries.sql`

## Query 1: Market-wise price analysis

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
```

**Sample output/observation:** The query returned market-wise record counts, average modal prices, and minimum and maximum prices. It applied `HAVING COUNT(*) >= 10` to retain markets with at least ten records.

**Execution time:** 162 ms.

## Query 2: Monthly price analysis

**Business question:** How do average, minimum, and maximum tomato prices vary across the months of 2025?

```sql
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
```

**Sample output/observation:**

- The query returned monthly statistics across 12 months.
- December had the highest monthly average modal price, approximately ₹3,586.81.
- March had the lowest monthly average modal price, approximately ₹895.56.

**Execution time:** 216 ms.

## Query 3: Grade-wise price analysis

**Business question:** How do tomato prices differ across the available grades?

```sql
SELECT
    Grade,
    COUNT(*) AS Total_Records,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price,
    MIN(Modal_Price) AS Minimum_Price,
    MAX(Modal_Price) AS Maximum_Price
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
GROUP BY Grade
ORDER BY Average_Modal_Price DESC;
```

**Sample output/observation:**

- Five grades were returned.
- Medium grade had an average modal price of approximately ₹2,602.38.
- Local grade contained 332 records.
- FAQ grade contained 299 records, with an average modal price of approximately ₹1,280.94.
- Ref grade-2 had the lowest average modal price, approximately ₹1,000.

**Execution time:** 193 ms.

## Query 4: Above-average price analysis using a subquery

**Business question:** Which markets contain records with modal prices above the overall average modal price?

```sql
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
```

**Sample output/observation:**

- The query identified 242 above-average records across nine markets.
- Ramanagara APMC had an average modal price of approximately ₹3,709.80 among the records returned by this query.
- Binny Mill APMC had an average modal price of approximately ₹3,928 among the returned records.

**Execution time:** 205 ms.

## Query 5: Market performance using CTEs

**Business question:** Which markets have an average modal price above or below the overall dataset average?

```sql
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
```

**Sample output/observation:**

- The query returned nine markets.
- Four markets were classified as above the overall average.
- Five markets were classified as below the overall average.
- The overall average modal price was approximately ₹1,924.81.
- Binny Mill APMC had the highest market average, approximately ₹3,770.37.

**Execution time:** 186 ms.

## Query 6: Market ranking using a window function

**Business question:** How can markets be ranked according to their average tomato modal prices?

```sql
SELECT
    Market,
    ROUND(AVG(Modal_Price), 2) AS Average_Modal_Price,
    RANK() OVER (
        ORDER BY AVG(Modal_Price) DESC
    ) AS Market_Rank
FROM `agrimarketanalytics.mandi_price_data.tomato_karnataka_2025`
GROUP BY Market
ORDER BY Market_Rank;
```

**Sample output/observation:**

- Binny Mill APMC ranked first, with an average modal price of approximately ₹3,770.37.
- Doddaballa Pur ranked ninth, with an average modal price of approximately ₹1,375.

**Execution time:** 173 ms.

## Query 7: Daily price movement using LAG

**Business question:** How does the modal price change compared with the previous recorded date for each market?

```sql
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
```

**Sample output/observation:** The query returns each market's arrival date and modal price, along with the previous recorded modal price and the difference between the two. The first available record for each market has no previous recorded price.

**Execution time:** 194 ms.

## Query 8: High-price categorization

**Business question:** Which records have modal prices of at least ₹3,000, and how can they be classified by price level?

```sql
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
```

**Sample output/observation:**

- Nine records met the filter condition of modal price greater than or equal to ₹3,000.
- The highest modal price was ₹6,000.
- Six records had modal prices of at least ₹5,000.

**Execution time:** 221 ms.

## 14.1 BigQuery query coverage

| Query | SQL concept demonstrated |
|---|---|
| Query 1 | GROUP BY, HAVING, aggregation |
| Query 2 | Date extraction, GROUP BY, aggregation |
| Query 3 | GROUP BY, aggregation |
| Query 4 | Subquery, filtering, aggregation |
| Query 5 | CTEs, CROSS JOIN, CASE |
| Query 6 | RANK window function |
| Query 7 | LAG window function |
| Query 8 | CASE expression and filtering |

The eight queries demonstrate the required analytical SQL techniques.

# 15. MACHINE-LEARNING PRICE FORECASTING

## 15.1 Objective

The forecasting component uses historical Ramanagara tomato price records to estimate short-term modal prices.

The model is implemented in:

`FORECASTING/price_forecasting.py`

## 15.2 Model

**Algorithm:** Random Forest Regression

The model uses historical price data to learn relationships in the available dataset and generate predictions.

## 15.3 Model evaluation

| Metric | Result |
|---|---:|
| Training records | 240 |
| Testing records | 61 |
| Mean Absolute Error (MAE) | ₹413.69 |
| Root Mean Squared Error (RMSE) | ₹462.72 |

MAE measures the average absolute difference between actual and predicted prices. RMSE measures prediction error while giving greater weight to larger errors.

## 15.4 Forecast output

The project generates a seven-day forecast, stored in:

`FORECASTING/next_7_days_forecast.csv`

The evaluation output is stored in:

`FORECASTING/model_evaluation.csv`

The available Ramanagara historical data ends in 2025. Therefore, the forecast is based on historical records and must not be interpreted as a live November 2026 market prediction.

# 16. STREAMLIT ANALYTICS DASHBOARD

## 16.1 Objective

The dashboard presents agricultural market-price information in an interactive visual format.

**Dashboard file:** `DASHBOARD/app_corrected.py`

## 16.2 Dashboard features

1. Daily tomato modal-price trend.
2. Market-wise price comparison.
3. High-price record analysis.
4. Actual versus predicted price visualization.
5. Seven-day price forecast.
6. Historical market-price records table.

## 16.3 Verified dashboard results

The dashboard successfully connected to MongoDB Atlas and displayed the full 673-record Karnataka tomato dataset across nine markets. This is the dashboard's full-dataset scope; the separate curated MongoDB collection used in the ETL and NoSQL query demonstrations contains 160 Ramanagara FAQ-grade records.

| Dashboard metric | Result |
|---|---:|
| Total records | 673 |
| Markets | 9 |
| Average modal price | ₹1,924.81 |
| Minimum modal price | ₹500 |
| Maximum modal price | ₹6,000 |
| Records above ₹2,000 | 205 |

The dashboard's charts, forecast visualizations, alerts, and market-record table were verified during execution.

## 16.4 Running the dashboard

From the project root:

```powershell
python -m streamlit run DASHBOARD/app_corrected.py
```

Open the local URL displayed in the terminal.

# 17. RESULTS AND DISCUSSION

## 17.1 Overall results

| Component | Result |
|---|---|
| Historical dataset | 673 records |
| Markets covered | 9 |
| BigQuery analytical queries | 8 |
| Curated Ramanagara FAQ records | 160 |
| MongoDB analytical queries | 5 |
| MongoDB query execution times | 24.525–49.822 ms (measured) |
| Automated ETL | Successfully tested |
| Kafka topic | `mandi-prices` |
| Spark streaming queries | 3; all processed 673 records each |
| Kafka/Spark replay | 673 records processed by each of 3 queries |
| High-price threshold | ₹2,000 |
| Forecasting model | Random Forest Regression |
| Forecast MAE | ₹413.69 |
| Forecast RMSE | ₹462.72 |
| Dashboard | Successfully launched and verified |

## 17.2 Key observations

1. The full Karnataka tomato dataset contained 673 records across nine markets.
2. The overall average modal price was ₹1,924.81.
3. The maximum recorded modal price was ₹6,000.
4. The dashboard identified 205 historical records above ₹2,000.
5. The curated Ramanagara FAQ dataset contained 160 records.
6. The BigQuery queries provided market, monthly, grade-wise, ranking, and price-movement analysis.
7. MongoDB queries demonstrated date filtering, aggregation, and high-price identification.
8. The ETL pipeline successfully processed the 160 curated records.
9. Kafka replayed 673 historical records, and each of the three Spark queries processed all 673 records across seven non-empty batches.
10. The Spark queries performed raw record processing, one-minute market aggregation, and high-price filtering for modal prices greater than ₹2,000.
11. The Random Forest model achieved an MAE of ₹413.69 and RMSE of ₹462.72 on the evaluated historical dataset.

# 18. CHALLENGES FACED

## 18.1 Data quality and schema consistency

The source dataset required inspection and validation to ensure that field names, date formats, and price values were suitable for analysis.

## 18.2 Cloud integration

Connecting Python applications to BigQuery and MongoDB Atlas required configuring the correct authentication and connection settings.

## 18.3 ETL automation

The BigQuery-to-MongoDB transfer needed to be automated using a Python script, a batch file, and Windows Task Scheduler.

## 18.4 Kafka and Spark integration

Configuring the Kafka broker connection and Spark Kafka dependencies required careful setup.

## 18.5 Streaming checkpoints

Separate checkpoint directories were configured for raw record processing, window aggregation, and high-price alerts.

## 18.6 Query optimization

The MongoDB performance comparison showed that fewer documents examined do not necessarily result in lower elapsed execution time for a small collection.

# 19. LEARNINGS

Through this project, the following practical skills were developed:

- Working with public agricultural market datasets.
- Inspecting and validating structured data.
- Using Google BigQuery as a cloud data warehouse.
- Writing analytical SQL queries.
- Applying subqueries, CTEs, aggregations, and window functions.
- Integrating BigQuery with MongoDB Atlas.
- Developing and testing automated ETL.
- Using Windows Task Scheduler for automation.
- Producing records through Apache Kafka.
- Processing streaming data using PySpark Structured Streaming.
- Implementing windowed aggregation and event-based alerts.
- Applying MongoDB indexing.
- Evaluating machine-learning models using MAE and RMSE.
- Developing interactive dashboards using Streamlit.
- Managing project source code using Git and GitHub.

# 20. LIMITATIONS

1. The historical dataset is limited to Karnataka tomato prices for the selected 2025 period.
2. The dataset contains 673 records and is a modest academic-scale dataset rather than a large production dataset.
3. The streaming component uses replayed historical records and test events; it is not connected to a continuous live AGMARKNET feed.
4. The high-price alert is demonstrated through Spark console output.
5. The forecasting model is trained on historical Ramanagara records and does not provide a verified live market forecast.
6. Model performance may be affected by weather, seasonal variations, demand, supply, and other external factors.
7. The MongoDB index reduced documents examined but did not produce a faster measured execution time in the recorded test.
8. The Spark trigger timings are batch-level measurements from the replay run and include first-batch startup overhead; they should not be interpreted as end-to-end production latency.

# 21. FUTURE ENHANCEMENTS

1. Extend the dataset to additional commodities and states.
2. Integrate a continuously updated live agricultural market-price source.
3. Increase the volume and historical coverage of the dataset.
4. Deploy the streaming pipeline and dashboard on cloud infrastructure.
5. Add persistent storage for streaming alerts and aggregations.
6. Improve forecasting using additional time-series models and external features.
7. Incorporate weather, rainfall, demand, and supply information.
8. Develop farmer-friendly mobile and web applications.
9. Add automated notifications for significant price changes.
10. Conduct larger-scale performance testing to evaluate partitioning, clustering, and indexing.

# 22. PROJECT REPOSITORY AND FILE STRUCTURE

The complete source code and project documentation are maintained in GitHub.

**Repository:**

https://github.com/sanjanamonteiro/Agricultural-Market-Price-Intelligence

Important project files include:

```text
Agricultural_Market_Price_Intelligence/
│
├── DASHBOARD/
│   └── app_corrected.py
│
├── DATA/
│   └── RAW/
│       └── tomato_karnataka_2025.csv
│
├── DOCS/
│   ├── Project_Report.md
│   ├── architecture_diagram.md
│   └── Screenshots/
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
├── SCRIPTS/
│   └── bigquery_queries.sql
│
├── STREAMING/
│   ├── kafka_price_producer.py
│   └── spark_kafka_stream.py
│
├── requirements.txt
├── run_etl.bat
├── transfer_bigquery_to_mongodb.py
└── .gitignore
```

Private credentials, environment files, virtual environments, and generated checkpoint files are excluded from version control.

# 23. INSTALLATION AND EXECUTION GUIDE

## 23.1 Prerequisites

- Python
- Git
- Google Cloud and BigQuery access
- MongoDB Atlas account
- Apache Kafka
- Apache Spark
- Java
- Visual Studio Code

## 23.2 Clone the repository

```powershell
git clone https://github.com/sanjanamonteiro/Agricultural-Market-Price-Intelligence.git

cd Agricultural-Market-Price-Intelligence
```

## 23.3 Create a Python environment

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

## 23.4 Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## 23.5 Configure credentials

Configure Google Cloud authentication and the MongoDB Atlas connection details required by the project scripts.

Do not upload passwords, API keys, service-account JSON files, or private environment files to GitHub.

## 23.6 Execute ETL

```powershell
.\run_etl.bat
```

The batch file runs the BigQuery-to-MongoDB transfer script. Automated execution is configured through Windows Task Scheduler.

## 23.7 Run the dashboard

```powershell
python -m streamlit run DASHBOARD/app_corrected.py
```

## 23.8 Run the forecasting script

```powershell
python FORECASTING/price_forecasting.py
```

## 23.9 Run the streaming components

The Kafka broker must be running before the producer and Spark consumer are started.

The producer script is:

`STREAMING/kafka_price_producer.py`

The Spark Structured Streaming script is:

`STREAMING/spark_kafka_stream.py`

The scripts use the Kafka configuration defined in their source files.

# 24. DEMONSTRATION PLAN

The project demonstration can follow this sequence:

1. Introduce the problem statement and dataset.
2. Explain the system architecture and technology choices.
3. Show the BigQuery dataset and curated table.
4. Execute the eight BigQuery analytical queries.
5. Explain the BigQuery partitioning and clustering configuration.
6. Show the MongoDB database and 160 curated records.
7. Execute the five MongoDB queries.
8. Explain the date index and performance comparison.
9. Demonstrate the automated ETL script and scheduled task.
10. Show the Kafka topic and producer records.
11. Demonstrate Spark raw record processing.
12. Demonstrate one-minute market aggregation.
13. Demonstrate the high-price alert using replayed records with modal prices greater than ₹2,000.
14. Show the Streamlit dashboard.
15. Explain the Random Forest forecasting results and limitations.
16. Summarize the project outcomes and future enhancements.

# 25. CONCLUSION

The project **Agricultural Market Price Intelligence and Short-Term Crop Price Forecasting Using Big Data Analytics** demonstrates an integrated Big Data analytics workflow using agricultural market-price data.

The project collects and validates public tomato market-price records from AGMARKNET, stores and analyzes the historical dataset in Google BigQuery, transfers curated records into MongoDB Atlas, and automates the ETL process.

Eight analytical SQL queries and five MongoDB queries demonstrate data retrieval, filtering, grouping, aggregation, and market-price analysis. BigQuery partitioning and clustering, along with MongoDB indexing, demonstrate data organization and query optimization techniques.

Apache Kafka and Apache Spark Structured Streaming demonstrate simulated continuous ingestion, raw record processing, one-minute window aggregation, and high-price alert detection. The project also includes a Random Forest forecasting model and an interactive Streamlit dashboard.

The implementation demonstrates the integration of cloud data warehousing, NoSQL storage, automated ETL, streaming analytics, machine learning, and visualization in one agricultural market intelligence application.

The system provides a foundation for understanding historical agricultural price movements and can be extended with larger datasets, live market feeds, improved forecasting, and cloud deployment.

# 26. REFERENCES

1. Government of India, Open Government Data Platform – https://www.data.gov.in/
2. AGMARKNET, Agricultural Marketing Information Network – https://agmarknet.gov.in/
3. Google Cloud, BigQuery Documentation – https://cloud.google.com/bigquery/docs
4. MongoDB Documentation – https://www.mongodb.com/docs/
5. MongoDB Atlas Documentation – https://www.mongodb.com/docs/atlas/
6. Apache Kafka Documentation – https://kafka.apache.org/documentation/
7. Apache Spark Structured Streaming Documentation – https://spark.apache.org/docs/latest/streaming/index.html
8. Streamlit Documentation – https://docs.streamlit.io/
9. Python Documentation – https://docs.python.org/3/
10. Scikit-learn Documentation – https://scikit-learn.org/stable/

---

**END OF PROJECT REPORT**