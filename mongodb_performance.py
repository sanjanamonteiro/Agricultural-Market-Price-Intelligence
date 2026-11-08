from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
collection = client["agri_market_intelligence"]["ramanagara_tomato_prices"]

try:
    query = {
        "Arrival_Date": {
            "$gte": "2025-01-01",
            "$lt": "2025-02-01"
        }
    }

    indexed = collection.find(query).hint("Arrival_Date_1").explain()["executionStats"]
    unindexed = collection.find(query).hint([("$natural", 1)]).explain()["executionStats"]

    print("\nINDEXED QUERY")
    print("Keys examined:", indexed["totalKeysExamined"])
    print("Documents examined:", indexed["totalDocsExamined"])
    print("Execution time (ms):", indexed["executionTimeMillis"])

    print("\nUNINDEXED QUERY")
    print("Keys examined:", unindexed["totalKeysExamined"])
    print("Documents examined:", unindexed["totalDocsExamined"])
    print("Execution time (ms):", unindexed["executionTimeMillis"])

finally:
    client.close()
