
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# --------------------------------------------------
# CONNECT TO MONGODB ATLAS
# --------------------------------------------------

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


# --------------------------------------------------
# QUERY 1: INDEXED DATE-RANGE SEARCH
# Find records for January 2025
# --------------------------------------------------

print("\nQUERY 1: JANUARY 2025 RECORDS")

query1 = {
    "Arrival_Date": {
        "$gte": "2025-01-01",
        "$lt": "2025-02-01"
    }
}

january_records = list(
    collection.find(query1, {"_id": 0})
    .hint("Arrival_Date_1")
    .limit(5)
)

print("January record count:", collection.count_documents(query1))
print("Sample records:", january_records)

explain = (
    collection.find(query1)
    .hint("Arrival_Date_1")
    .explain()
)

print("Index keys examined:",
      explain["executionStats"]["totalKeysExamined"])

print("Documents examined:",
      explain["executionStats"]["totalDocsExamined"])


# --------------------------------------------------
# QUERY 2: PRICE STATISTICS
# Find average, minimum and maximum modal price
# --------------------------------------------------

print("\nQUERY 2: PRICE STATISTICS")

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

print(result2)


# --------------------------------------------------
# QUERY 3: GRADE-WISE PRICE ANALYSIS
# Group records according to grade
# --------------------------------------------------

print("\nQUERY 3: GRADE-WISE PRICE ANALYSIS")

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

for record in result3:
    print(record)


# --------------------------------------------------
# QUERY 4: HIGH-PRICE ALERT
# Find records with modal price above Rs. 2000
# --------------------------------------------------

print("\nQUERY 4: HIGH-PRICE RECORDS")

query4 = {
    "Modal_Price": {"$gt": 2000}
}

high_price_records = list(
    collection.find(
        query4,
        {"_id": 0, "Arrival_Date": 1, "Market": 1,
         "Modal_Price": 1}
    ).sort("Modal_Price", -1).limit(10)
)

print("High-price record count:",
      collection.count_documents(query4))

for record in high_price_records:
    print(record)


# --------------------------------------------------
# QUERY 5: MONTHLY AVERAGE PRICE
# Calculate average modal price for each month
# --------------------------------------------------

print("\nQUERY 5: MONTHLY PRICE ANALYSIS")

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

for record in result5:
    print(record)


# --------------------------------------------------
# CLOSE CONNECTION
# --------------------------------------------------

client.close()

print("\nALL FIVE MONGODB QUERIES EXECUTED.")
