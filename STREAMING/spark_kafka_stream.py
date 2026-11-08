
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg, col, count, from_json, to_date, window
)
from pyspark.sql.types import StructType, StructField, StringType

KAFKA_SERVER = "localhost:9092"
KAFKA_TOPIC = "mandi-prices"
PRICE_ALERT_THRESHOLD = 2000

PROJECT_ROOT = (
    "/mnt/c/Users/SANJANA/BIG DATA/"
    "Agricultural_Market_Price_Intelligence"
)

CHECKPOINT_ROOT = PROJECT_ROOT + "/STREAMING/checkpoints_v2"

schema = StructType([
    StructField("Arrival_Date", StringType(), True),
    StructField("Commodity", StringType(), True),
    StructField("Commodity_Code", StringType(), True),
    StructField("District", StringType(), True),
    StructField("Grade", StringType(), True),
    StructField("Market", StringType(), True),
    StructField("Max_Price", StringType(), True),
    StructField("Min_Price", StringType(), True),
    StructField("Modal_Price", StringType(), True),
    StructField("State", StringType(), True),
    StructField("Variety", StringType(), True),
])

spark = (
    SparkSession.builder
    .appName("AgriMarketPriceIntelligence")
    .master("local[2]")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.1"
    )
    .config("spark.sql.shuffle.partitions", "4")
    .config("spark.default.parallelism", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("Starting Agricultural Market Price Streaming...")
print("Kafka server:", KAFKA_SERVER)
print("Shuffle partitions: 4")

kafka_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_SERVER)
    .option("subscribe", KAFKA_TOPIC)
    .option("startingOffsets", "earliest")
    .option("maxOffsetsPerTrigger", "100")
    .load()
)

parsed_stream = (
    kafka_stream
    .select(
        from_json(
            col("value").cast("string"), schema
        ).alias("data"),
        col("timestamp").alias("event_time")
    )
    .select("data.*", "event_time")
    .withColumn(
        "Arrival_Date",
        to_date(col("Arrival_Date"), "dd/MM/yyyy")
    )
    .withColumn("Max_Price", col("Max_Price").cast("double"))
    .withColumn("Min_Price", col("Min_Price").cast("double"))
    .withColumn("Modal_Price", col("Modal_Price").cast("double"))
    .filter(
        col("Modal_Price").isNotNull()
        & col("Market").isNotNull()
    )
)

# Query 1: Structured mandi-price records
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

# Query 2: One-minute average price by market
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

# Query 3: High-price alerts
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

print("All three streaming queries started!")
print("1. Structured mandi-price records")
print("2. One-minute market price aggregation")
print("3. High-price alerts above Rs.", PRICE_ALERT_THRESHOLD)

spark.streams.awaitAnyTermination()
