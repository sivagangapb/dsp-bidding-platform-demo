import snowflake.connector

# Replace these with your actual values
conn = snowflake.connector.connect(
    user='YOUR_USERNAME',
    password='YOUR_PASSWORD',
    account='YOUR_ACCOUNT_REGION',
    warehouse='COMPUTE_WH',
    database='YOUR_DATABASE',
    schema='YOUR_SCHEMA'
)

cursor = conn.cursor()

# Query the latest summary
query = """
SELECT summary_date, site_domain, total_bids
FROM bid_summary_table
WHERE summary_date = CURRENT_DATE()
ORDER BY total_bids DESC
LIMIT 5;
"""

cursor.execute(query)
rows = cursor.fetchall()

# Compose mock email
if rows:
    print("📧 Daily Bid Summary Email:")
    print("Subject: DSP Daily Summary")
    print("Body:")
    for row in rows:
        print(f"- {row[1]} received {row[2]} bids on {row[0]}")
else:
    print("📭 No summary data found for today.")

cursor.close()
conn.close()
