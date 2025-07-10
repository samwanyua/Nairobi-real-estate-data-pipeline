import smtplib
from email.mime.text import MIMEText
import psycopg2

def send_email_alert():
    # Step 1: Connect to clean_db
    conn = psycopg2.connect(
        host="clean_db",
        dbname="clean_db",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()

    # Step 2: Fetch the latest listing
    cursor.execute("""
        SELECT title, price, location, bedrooms, bathrooms, parking
        FROM clean_listings
        ORDER BY inserted_at DESC
        LIMIT 1;
    """)
    listing = cursor.fetchone()

    if not listing:
        print("No listings found.")
        return

    title, price, location, bedrooms, bathrooms, parking = listing

    # Step 3: Compose custom message
    sender = "samexample8@gmail.com"
    recipient = "sam2wanyua@gmail.com"
    subject = "New Property Alert"
    body = (
        f"New Listing: {title}\n\n"
        f"Location: {location}\n"
        f"Price: KES {price:,.0f} per month\n"
        f"Bedrooms: {bedrooms}, Bathrooms: {bathrooms}, Parking: {parking}\n"
        f"\nCheck it out on Property24 or your dashboard!"
    )

    # Step 4: Send the email
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP("mailserver", 587) as server:
        server.starttls()
        server.login("admin", "admin")
        server.sendmail(sender, recipient, msg.as_string())

    print(f"Email sent: {subject}")

    # Step 5: Clean up
    cursor.close()
    conn.close()
