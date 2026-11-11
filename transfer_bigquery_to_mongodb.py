import math
import os
from datetime import date, datetime
from decimal import Decimal
from collections import OrderedDict

from dotenv import load_dotenv
from google.cloud import bigquery
from pymongo import MongoClient, ASCENDING


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

load_dotenv()

PROJECT_ID = "agrimarketanalytics"
DATASET_ID = "mandi_price_data"
TABLE_ID = "ramanagara_tomato_curated"

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "agri_market_intelligence"
COLLECTION_NAME = "ramanagara_tomato_prices"

PRICE_FIELDS = ("Min_Price", "Modal_Price", "Max_Price")
REQUIRED_FIELDS = (
    "Arrival_Date",
    "Commodity",
    "District",
    "Grade",
    "Market",
    "Min_Price",
    "Modal_Price",
    "Max_Price",
    "State",
    "Variety",
)

# Business key: one record per date, commodity, location, market,
# grade and variety. This allows multiple legitimate records per date.
BUSINESS_KEY_FIELDS = (
    "Arrival_Date",
    "Commodity",
    "State",
    "District",
    "Market",
    "Grade",
    "Variety",
)

if not MONGODB_URI:
    raise ValueError("MONGODB_URI was not found in .env")


# ---------------------------------------------------------------------
# Preprocessing helpers
# ---------------------------------------------------------------------

def make_mongo_safe(record):
    """Clean text and convert BigQuery values to MongoDB-safe values."""
    cleaned = {}

    for key, value in record.items():
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                value = None
        elif isinstance(value, (date, datetime)):
            value = value.isoformat()
        elif isinstance(value, Decimal):
            value = float(value)

        cleaned[key] = value

    return cleaned


def validate_schema(record):
    """Ensure every required source field is present."""
    missing_columns = [field for field in REQUIRED_FIELDS if field not in record]
    if missing_columns:
        raise ValueError(
            "BigQuery schema is missing required columns: "
            + ", ".join(missing_columns)
        )


def validate_and_normalize_record(record):
    """
    Validate required values and price relationships.
    Return (cleaned_record, rejection_reason).
    """
    cleaned = make_mongo_safe(record)

    missing_values = [
        field for field in REQUIRED_FIELDS
        if cleaned.get(field) is None
    ]
    if missing_values:
        return None, "missing_required_values"

    # Validate date format.
    try:
        datetime.fromisoformat(cleaned["Arrival_Date"])
    except (TypeError, ValueError):
        return None, "invalid_arrival_date"

    # Validate required text fields.
    for field in ("Commodity", "District", "Grade", "Market", "State", "Variety"):
        if not isinstance(cleaned[field], str) or not cleaned[field]:
            return None, "invalid_text_value"

    # Convert prices to finite numeric values.
    prices = {}
    for field in PRICE_FIELDS:
        try:
            value = float(cleaned[field])
        except (TypeError, ValueError, OverflowError):
            return None, "non_numeric_price"

        if not math.isfinite(value):
            return None, "non_finite_price"

        if value < 0:
            return None, "negative_price"

        prices[field] = value

    # Market-price consistency check. Do not remove merely high prices;
    # only reject records that violate the min <= modal <= max rule.
    if not (
        prices["Min_Price"]
        <= prices["Modal_Price"]
        <= prices["Max_Price"]
    ):
        return None, "inconsistent_price_range"

    for field, value in prices.items():
        cleaned[field] = value

    return cleaned, None


def business_key(record):
    """Build the natural key used for deduplication and MongoDB upserts."""
    return tuple(record[field] for field in BUSINESS_KEY_FIELDS)


def preprocess_records(source_records):
    """
    Clean, validate and deduplicate source records.
    Exact duplicates are removed. Conflicting records with the same
    business key stop the load instead of silently overwriting data.
    """
    accepted = OrderedDict()
    rejected_counts = {}
    duplicate_count = 0

    for source_record in source_records:
        validate_schema(source_record)

        cleaned, reason = validate_and_normalize_record(source_record)

        if reason:
            rejected_counts[reason] = rejected_counts.get(reason, 0) + 1
            continue

        key = business_key(cleaned)

        if key in accepted:
            if accepted[key] == cleaned:
                duplicate_count += 1
                continue

            raise ValueError(
                "Conflicting source records share the same business key "
                f"{key}. No records were loaded. Review the BigQuery source."
            )

        accepted[key] = cleaned

    return list(accepted.values()), duplicate_count, rejected_counts


# ---------------------------------------------------------------------
# ETL workflow
# ---------------------------------------------------------------------

def main():
    bq_client = bigquery.Client(project=PROJECT_ID)
    mongo_client = None

    try:
        query = f"""
            SELECT *
            FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
            ORDER BY Arrival_Date
        """

        query_job = bq_client.query(query)
        source_records = [dict(row.items()) for row in query_job.result()]

        print(f"Fetched {len(source_records)} records from BigQuery.")

        if not source_records:
            print("No records found. Nothing to transfer.")
            return

        # PREPROCESS: schema validation, cleaning, quality checks,
        # format conversion and deduplication.
        clean_records, duplicate_count, rejected_counts = preprocess_records(
            source_records
        )

        rejected_total = sum(rejected_counts.values())

        print("\nPREPROCESSING SUMMARY")
        print(f"Source records: {len(source_records)}")
        print(f"Exact duplicates removed: {duplicate_count}")
        print(f"Invalid records rejected: {rejected_total}")

        if rejected_counts:
            for reason, count in sorted(rejected_counts.items()):
                print(f"  {reason}: {count}")

        print(f"Valid unique records: {len(clean_records)}")

        if not clean_records:
            raise ValueError(
                "No valid records remain after preprocessing. "
                "MongoDB was not modified."
            )

        mongo_client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=10000
        )
        mongo_client.admin.command("ping")

        collection = mongo_client[DATABASE_NAME][COLLECTION_NAME]

        # Create the composite business-key index first. If existing
        # MongoDB data contains duplicate business keys, this fails safely
        # before the old index is removed or any records are changed.
        collection.create_index(
            [(field, ASCENDING) for field in BUSINESS_KEY_FIELDS],
            unique=True,
            name="market_price_business_key"
        )

        # Remove the previous date-only unique index. It would incorrectly
        # prevent multiple legitimate market records on the same date.
        existing_indexes = collection.index_information()

        for index_name, index_info in existing_indexes.items():
            index_keys = index_info.get("key", [])
            is_date_only_unique = (
                index_keys == [("Arrival_Date", ASCENDING)]
                and index_info.get("unique", False)
            )

            if is_date_only_unique:
                collection.drop_index(index_name)
                print(f"Replaced old date-only unique index: {index_name}")

        inserted = 0
        updated = 0
        unchanged = 0

        for record in clean_records:
            filter_document = {
                field: record[field] for field in BUSINESS_KEY_FIELDS
            }

            result = collection.update_one(
                filter_document,
                {"$set": record},
                upsert=True
            )

            if result.upserted_id is not None:
                inserted += 1
            elif result.modified_count:
                updated += 1
            else:
                unchanged += 1

        print("\nSUCCESS: BigQuery to MongoDB ETL completed.")
        print(f"New records inserted: {inserted}")
        print(f"Existing records updated: {updated}")
        print(f"Existing records unchanged: {unchanged}")
        print(f"Valid records processed: {len(clean_records)}")
        print(f"MongoDB collection count: {collection.count_documents({})}")
        print(f"MongoDB database: {DATABASE_NAME}")
        print(f"MongoDB collection: {COLLECTION_NAME}")

    finally:
        if mongo_client is not None:
            mongo_client.close()
        bq_client.close()


if __name__ == "__main__":
    main()
