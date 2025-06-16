import smtplib
from email.message import EmailMessage
import snowflake.connector
from dotenv import load_dotenv
import os

# Load secrets from .env
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

# Fetch summary from Snowflake
def get_summary():
    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            ocsp_fail_open=True,         # Allow connection if OCSP fails
    client_session_keep_alive=True,
    protocol='https'
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT summary_date, domain, count
            FROM BID_SUMMARY_TABLE
            ORDER BY summary_date DESC
            LIMIT 5;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Format summary
        summary = "📊 DSP Daily Bid Summary\n\nDate       | Domain        | Count\n"
        summary += "-----------|---------------|------\n"
        for row in rows:
            summary += f"{row[0]} | {row[1]:<14} | {row[2]}\n"
        return summary
    except Exception as e:
        return f"❌ Failed to fetch summary: {e}"

# Send the email
def send_email(summary_text):
    msg = EmailMessage()
    msg['Subject'] = "DSP Daily Summary Report"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(summary_text)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Run
if __name__ == "__main__":
    summary = get_summary()
    print("📬 Email content:\n", summary)
    send_email(summary)
