import smtplib
from email.mime.text import MIMEText
import psycopg2
from psycopg2.extras import RealDictCursor
import os


def send_email_alert():
    try:
        # DB connection config
        conn = psycopg2.connect(
            host= "postgres_main",  
            dbname="nrbproperties",
            user="postgres",
            password="postgres"
        )

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT title, price, location, bedrooms, bathrooms, parking
                FROM clean_listings
                ORDER BY inserted_at DESC
                LIMIT 1;
            """)
            listing = cursor.fetchone()

        conn.close()

        if not listing:
            print("[Email Notifier] No listings found to email.")
            return

        # Compose message
        sender = "samexample8@gmail.com"
        recipient = "sam2wanyua@gmail.com"
        subject = "New Property Alert"

        body = (
            f"New Listing: {listing['title']}\n\n"
            f"Location: {listing['location']}\n"
            f"Price: KES {listing['price']:,.0f} per month\n"
            f"Bedrooms: {listing['bedrooms']}, "
            f"Bathrooms: {listing['bathrooms']}, "
            f"Parking: {listing['parking']}\n\n"
            "Check it out on Property24 or your dashboard!"
        )

        # Send email
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        with smtplib.SMTP("mailserver", 587) as server:
            server.starttls()
            server.login("admin", "admin")
            server.sendmail(sender, recipient, msg.as_string())

        print(f"[Email Notifier] Email sent to {recipient}")

    except Exception as e:
        print(f"[Email Notifier] Error: {e}")
        raise
