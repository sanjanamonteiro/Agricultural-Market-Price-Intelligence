
import os
import time
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(
    os.getenv("MONGODB_URI"),
    serverSelectionTimeoutMS=15000
)

client.admin.command("ping")

collection = client["agri_market_intelligence"][
    "ramanagara_tomato_prices"
]

query = {
    "Arrival_Date": {
        "$gte": "2025-01-01",
        "$lt": "2025-02-01"
    }
}

print("\nMONGODB INDEX PERFORMANCE COMPARISON")
print("Total documents:", collection.count_documents({}))


# 1. INDEXED SEARCH

start = time.perf_counter()

indexed_result = list(
    collection.find(query).hint("Arrival_Date_1")
)

indexed_time = time.perf_counter() - start

indexed_explain = (
    collection.find(query)
    .hint("Arrival_Date_1")
    .explain()
)

print("\nINDEXED SEARCH")
print("Records found:", len(indexed_result))
print("Execution time:", round(indexed_time * 1000, 4), "ms")
print("Keys examined:",
      indexed_explain["executionStats"]["totalKeysExamined"])
print("Documents examined:",
      indexed_explain["executionStats"]["totalDocsExamined"])


# 2. COLLECTION SCAN

start = time.perf_counter()

scan_result = list(
    collection.find(query).sort("$natural", 1)
)

scan_time = time.perf_counter() - start

scan_explain = (
    collection.find(query)
    .sort("$natural", 1)
    .explain()
)

print("\nCOLLECTION SCAN")
print("Records found:", len(scan_result))
print("Execution time:", round(scan_time * 1000, 4), "ms")
print("Keys examined:",
      scan_explain["executionStats"]["totalKeysExamined"])
print("Documents examined:",
      scan_explain["executionStats"]["totalDocsExamined"])


# 3. COMPARISON

print("\nPERFORMANCE SUMMARY")
print("Indexed search:", round(indexed_time * 1000, 4), "ms")
print("Collection scan:", round(scan_time * 1000, 4), "ms")

if indexed_time < scan_time:
    print("Indexed search was faster in this run.")
elif scan_time < indexed_time:
    print("Collection scan was faster in this run.")
else:
    print("Both searches took approximately equal time.")

client.close()

print("\nPERFORMANCE TEST COMPLETED.")
