
from google.cloud import bigquery

PROJECT_ID = "agrimarketanalytics"

try:
    client = bigquery.Client(project=PROJECT_ID)

    query = """
        SELECT table_name, table_type
        FROM `agrimarketanalytics.mandi_price_data.INFORMATION_SCHEMA.TABLES`
        ORDER BY table_name
    """

    results = client.query(query).result()

    print("SUCCESS: Connected to BigQuery!")
    print("\nTables in mandi_price_data:")

    for row in results:
        print(f"{row.table_name} — {row.table_type}")

except Exception as error:
    print("BigQuery connection failed:")
    print(error)
