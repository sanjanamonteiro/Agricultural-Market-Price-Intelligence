
import os
from pathlib import Path
from datetime import datetime

import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent
CSV_PATH = PROJECT_ROOT / "DATA" / "RAW" / "tomato_karnataka_2025.csv"

load_dotenv(PROJECT_ROOT / ".env")

MONGODB_URI = os.getenv("MONGODB_URI")

DATABASE_NAME = "agri_market_intelligence"
COLLECTION_NAME = "karnataka_tomato_prices"


def main():

    if not MONGODB_URI:
        raise ValueError("MONGODB_URI not found in project .env file.")

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {CSV_PATH}")

    print("Reading original CSV dataset...")

    df = pd.read_csv(CSV_PATH)

    print("Original records:", len(df))

    # Parse dates using the exact CSV format: DD/MM/YYYY
    df["Arrival_Date"] = pd.to_datetime(
        df["Arrival_Date"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    if df["Arrival_Date"].isna().any():
        raise ValueError("Invalid or missing dates found. Import cancelled.")

    # Convert price columns to numeric values
    price_columns = ["Min_Price", "Max_Price", "Modal_Price"]

    for column in price_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

        if df[column].isna().any():
            raise ValueError(
                f"Invalid or missing values found in {column}. Import cancelled."
            )

    required_columns = [
        "Arrival_Date",
        "Market",
        "Modal_Price",
        "Min_Price",
        "Max_Price"
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Required fields contain missing values.")

    # Convert records to MongoDB-compatible Python values
    df = df.astype(object).where(pd.notna(df), None)

    records = []

    for record in df.to_dict("records"):
        for key, value in record.items():

            if isinstance(value, pd.Timestamp):
                record[key] = value.to_pydatetime()

            elif hasattr(value, "item"):
                record[key] = value.item()

        records.append(record)

    print("Validated records:", len(records))
    print("Invalid dates: 0")
    print("Date range:", df["Arrival_Date"].min(), "to", df["Arrival_Date"].max())

    # Connect to MongoDB
    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=15000
    )

    try:
        client.admin.command("ping")
        print("\nMongoDB connection successful.")

        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_name = f"{COLLECTION_NAME}_backup_{timestamp}"
        temp_name = f"{COLLECTION_NAME}_temp_{timestamp}"

        backup_collection = db[backup_name]
        temp_collection = db[temp_name]

        # Back up the existing collection before replacement
        old_count = collection.count_documents({})

        if old_count > 0:
            print(f"\nCreating backup of {old_count} existing records...")

            old_records = list(collection.find({}))

            backup_collection.insert_many(old_records)

            backup_count = backup_collection.count_documents({})

            if backup_count != old_count:
                raise RuntimeError("Backup verification failed. Import cancelled.")

            print("Backup verified:", backup_count, "records")
            print("Backup collection:", backup_name)

        # Load corrected data into a temporary collection
        print("\nLoading corrected records into temporary collection...")

        temp_collection.insert_many(records)

        temp_collection.create_index("Arrival_Date")
        temp_collection.create_index("Market")

        temp_count = temp_collection.count_documents({})

        if temp_count != len(records):
            raise RuntimeError("Temporary collection verification failed.")

        invalid_dates = temp_collection.count_documents(
            {"Arrival_Date": None}
        )

        if invalid_dates > 0:
            raise RuntimeError("Temporary collection contains invalid dates.")

        print("Temporary collection verified:", temp_count, "records")

        # Replace the original collection only after validation
        print("\nReplacing original collection with verified data...")

        temp_collection.rename(
            COLLECTION_NAME,
            dropTarget=True
        )

        # Final verification
        final_collection = db[COLLECTION_NAME]

        final_count = final_collection.count_documents({})

        if final_count != len(records):
            raise RuntimeError("Final MongoDB record count does not match.")

        print("\n========== IMPORT SUCCESS ==========")
        print("Total documents:", final_count)
        print("Available markets:", len(final_collection.distinct("Market")))
        print("Earliest date:", final_collection.find_one(
            {}, sort=[("Arrival_Date", 1)]
        )["Arrival_Date"])
        print("Latest date:", final_collection.find_one(
            {}, sort=[("Arrival_Date", -1)]
        )["Arrival_Date"])

        print("Indexes:", final_collection.index_information().keys())

        if old_count > 0:
            print("Backup preserved:", backup_name)

        print("====================================")

    finally:
        client.close()


if __name__ == "__main__":
    main()
