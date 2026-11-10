
import json
import time
from datetime import date, datetime
from decimal import Decimal

from google.cloud import bigquery
from kafka import KafkaProducer

# BigQuery source
PROJECT_ID = "agrimarketanalytics"
TABLE_ID = "agrimarketanalytics.mandi_price_data.tomato_karnataka_2025"

# Kafka settings
KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "mandi-prices"
DELAY_SECONDS = 1

QUERY = f"""
    SELECT *
    FROM `{TABLE_ID}`
    ORDER BY Arrival_Date, Market
"""


def json_default(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()

    if isinstance(value, Decimal):
        return float(value)

    raise TypeError(f"Cannot convert {type(value).__name__} to JSON")


def main():
    bigquery_client = bigquery.Client(project=PROJECT_ID)
    producer = None
    sent_count = 0

    try:
        print("Retrieving records from BigQuery...")

        rows = bigquery_client.query(QUERY).result()
        print("BigQuery query completed. Connecting to Kafka...")

        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda data: json.dumps(
                data, default=json_default
            ).encode("utf-8"),
            key_serializer=lambda key: key.encode("utf-8")
        )

        for row in rows:
            record = dict(row.items())

            market = str(record.get("Market") or "unknown")

            future = producer.send(
                TOPIC_NAME,
                key=market,
                value=record
            )

            future.get(timeout=10)
            sent_count += 1

            print(f"Sent record {sent_count}: {record}")

            time.sleep(DELAY_SECONDS)

    except KeyboardInterrupt:
        print("\nStreaming stopped by user.")

    finally:
        if producer is not None:
            producer.flush()
            producer.close()

        bigquery_client.close()

        print(f"Total records sent: {sent_count}")


if __name__ == "__main__":
    main()
