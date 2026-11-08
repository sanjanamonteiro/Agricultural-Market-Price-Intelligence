
import os
from datetime import date, datetime

from dotenv import load_dotenv
from google.cloud import bigquery
from pymongo import MongoClient, ASCENDING

# Load credentials from the existing .env file
load_dotenv()

PROJECT_ID = "agrimarketanalytics"
DATASET_ID = "mandi_price_data"
TABLE_ID = "ramanagara_tomato_curated"

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "agri_market_intelligence"
COLLECTION_NAME = "ramanagara_tomato_prices"

if not MONGODB_URI:
    raise ValueError("MONGODB_URI was not found in .env")

def make_mongo_safe(record):
    """Convert BigQuery date/time values into MongoDB-compatible values."""
    for key, value in record.items():
        if isinstance(value, (date, datetime)):
            record[key] = value.isoformat()
    return record

def main():
    bq_client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        ORDER BY Arrival_Date
    """

    rows = bq_client.query(query).result()
    records = [make_mongo_safe(dict(row.items())) for row in rows]

    print(f"Fetched {len(records)} records from BigQuery.")

    if not records:
        print("No records found. Nothing to transfer.")
        return

    mongo_client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=10000
    )

    try:
        mongo_client.admin.command("ping")
        collection = mongo_client[DATABASE_NAME][COLLECTION_NAME]

        # Use the date as a unique key to prevent duplicate daily records.
        collection.create_index(
            [("Arrival_Date", ASCENDING)],
            unique=True
        )

        inserted = 0
        updated = 0

        for record in records:
            result = collection.update_one(
                {"Arrival_Date": record["Arrival_Date"]},
                {"$set": record},
                upsert=True
            )

            if result.upserted_id is not None:
                inserted += 1
            elif result.modified_count:
                updated += 1

        print("SUCCESS: BigQuery to MongoDB transfer completed!")
        print(f"New records inserted: {inserted}")
        print(f"Existing records updated: {updated}")
        print(f"Total records processed: {len(records)}")
        print(f"MongoDB database: {DATABASE_NAME}")
        print(f"MongoDB collection: {COLLECTION_NAME}")

    finally:
        mongo_client.close()
        bq_client.close()

if __name__ == "__main__":
    main()
