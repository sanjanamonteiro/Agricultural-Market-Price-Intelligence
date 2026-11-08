from dotenv import load_dotenv
import os
from pymongo import MongoClient, DESCENDING

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
collection = client["agri_market_intelligence"]["ramanagara_tomato_prices"]

try:
    print("\n1. JANUARY RECORD COUNT")
    january = {
        "Arrival_Date": {
            "$gte": "2025-01-01",
            "$lt": "2025-02-01"
        }
    }
    print("January records:", collection.count_documents(january))

    print("\n2. HIGH-PRICE RECORDS (MODAL PRICE >= 2000)")
    high_price = {"Modal_Price": {"$gte": 2000}}
    print("High-price records:", collection.count_documents(high_price))

    print("\n3. TOP 5 HIGHEST-PRICED DATES")
    for record in collection.find(
        {},
        {"_id": 0, "Arrival_Date": 1, "Modal_Price": 1}
    ).sort("Modal_Price", DESCENDING).limit(5):
        print(record)

    print("\n4. MONTHLY AVERAGE MODAL PRICE")
    monthly = collection.aggregate([
        {
            "$group": {
                "_id": {"$substrBytes": ["$Arrival_Date", 0, 7]},
                "average_price": {"$avg": "$Modal_Price"},
                "record_count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ])
    for result in monthly:
        print(result)

    print("\n5. OVERALL PRICE STATISTICS")
    statistics = list(collection.aggregate([
        {
            "$group": {
                "_id": None,
                "total_records": {"$sum": 1},
                "average_price": {"$avg": "$Modal_Price"},
                "minimum_price": {"$min": "$Modal_Price"},
                "maximum_price": {"$max": "$Modal_Price"}
            }
        }
    ]))
    for result in statistics:
        result.pop("_id", None)
        print(result)

    print("\nINDEX PERFORMANCE")
    explain = collection.find(january).hint("Arrival_Date_1").explain()
    print("Keys examined:", explain["executionStats"]["totalKeysExamined"])
    print("Documents examined:", explain["executionStats"]["totalDocsExamined"])

finally:
    client.close()
