
import csv
import json
import time
from pathlib import Path
from kafka import KafkaProducer

# Project and dataset paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_DIR / "DATA" / "RAW" / "tomato_karnataka_2025.csv"

# Kafka settings
KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "mandi-prices"
DELAY_SECONDS = 1

def main():
    if not CSV_FILE.exists():
        print(f"Dataset not found: {CSV_FILE}")
        return

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda data: json.dumps(data).encode("utf-8"),
        key_serializer=lambda key: key.encode("utf-8")
    )

    sent_count = 0

    try:
        with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                record = {
                    key: value.strip() if isinstance(value, str) else value
                    for key, value in row.items()
                }

                # Send each market-price record to Kafka
                market = record.get("Market", "unknown")
                future = producer.send(
                    TOPIC_NAME,
                    key=market,
                    value=record
                )
                future.get(timeout=10)

                sent_count += 1
                print(f"Sent record {sent_count}: {record}")

                # Simulate a live incoming data feed
                time.sleep(DELAY_SECONDS)

    except KeyboardInterrupt:
        print("\nStreaming stopped by user.")

    finally:
        producer.flush()
        producer.close()
        print(f"Total records sent: {sent_count}")

if __name__ == "__main__":
    main()
