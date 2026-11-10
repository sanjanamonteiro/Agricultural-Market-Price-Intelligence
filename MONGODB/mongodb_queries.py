
import os
from time import perf_counter

from dotenv import load_dotenv
from pymongo import MongoClient

# Connect to MongoDB Atlas
load_dotenv()

client = MongoClient(
    os.getenv("MONGODB_URI"),
    serverSelectionTimeoutMS=15000
)

client.admin.command("ping")

db = client["agri_market_intelligence"]
collection = db["ramanagara_tomato_prices"]

print("\nMONGODB CONNECTION SUCCESSFUL")
print("Total records:", collection.count_documents({}))


# QUERY 1: INDEXED DATE-RANGE SEARCH
print("\nQUERY 1: JANUARY 2025 RECORDS")

query1 = {
    "Arrival_Date": {
        "$gte": "2025-01-01",
        "$lt": "2025-02-01"
    }
}

start = perf_counter()

january_count = collection.count_documents(query1)

january_records = list(
    collection.find(query1, {"_id": 0})
    .hint("Arrival_Date_1")
    .limit(5)
)

query1_time = (perf_counter() - start) * 1000

print("January record count:", january_count)
print("Sample records:", january_records)
print("Execution time:", round(query1_time, 3), "ms")

explain = (
    collection.find(query1)
    .hint("Arrival_Date_1")
    .explain()
)

print("Index keys examined:",
      explain["executionStats"]["totalKeysExamined"])

print("Documents examined:",
      explain["executionStats"]["totalDocsExamined"])


# QUERY 2: OVERALL PRICE STATISTICS
print("\nQUERY 2: PRICE STATISTICS")

start = perf_counter()

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

query2_time = (perf_counter() - start) * 1000

print(result2)
print("Execution time:", round(query2_time, 3), "ms")


# QUERY 3: GRADE-WISE PRICE ANALYSIS
print("\nQUERY 3: GRADE-WISE PRICE ANALYSIS")

start = perf_counter()

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

query3_time = (perf_counter() - start) * 1000

for record in result3:
    print(record)

print("Execution time:", round(query3_time, 3), "ms")


# QUERY 4: HIGH-PRICE RECORD IDENTIFICATION
print("\nQUERY 4: HIGH-PRICE RECORDS")

query4 = {
    "Modal_Price": {"$gt": 2000}
}

start = perf_counter()

high_price_count = collection.count_documents(query4)

high_price_records = list(
    collection.find(
        query4,
        {
            "_id": 0,
            "Arrival_Date": 1,
            "Market": 1,
            "Modal_Price": 1
        }
    ).sort("Modal_Price", -1).limit(10)
)

query4_time = (perf_counter() - start) * 1000

print("High-price record count:", high_price_count)

for record in high_price_records:
    print(record)

print("Execution time:", round(query4_time, 3), "ms")


# QUERY 5: MONTHLY AVERAGE PRICE
print("\nQUERY 5: MONTHLY PRICE ANALYSIS")

start = perf_counter()

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

query5_time = (perf_counter() - start) * 1000

for record in result5:
    print(record)

print("Execution time:", round(query5_time, 3), "ms")


# EXECUTION TIME SUMMARY
print("\n===== MONGODB EXECUTION TIME SUMMARY =====")

timings = [
    ("Query 1: Indexed date search", query1_time),
    ("Query 2: Price statistics", query2_time),
    ("Query 3: Grade-wise analysis", query3_time),
    ("Query 4: High-price records", query4_time),
    ("Query 5: Monthly analysis", query5_time)
]

for name, elapsed in timings:
    print(f"{name}: {elapsed:.3f} ms")

print("\nALL FIVE MONGODB QUERIES EXECUTED SUCCESSFULLY.")

client.close()
