import pandas as pd
from datetime import datetime
import africastalking
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Africa's Talking
username = "ephraimm-zm"  # replace with your Africa's Talking username
api_key = "atsk_e99b599780f3640ef69a6bd6b7c66cc747bb7ef74cd40cfff814af4d3008f26c5b03d4c7"    # replace with your Africa's Talking API key
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# Load Excel file
file_path = "rejected-sms-list.xlsx"
df = pd.read_excel(file_path)

# Loop through each row
for index, row in df.iterrows():
    try:
        name = str(row["name"]).strip()
        phone = str(row["phone_number1"]).strip()

        # Format phone number
        if phone.endswith(".0"):
            phone = phone.replace(".0", "")
        if not phone.startswith("+"):
            phone = "+" + phone

        risk_name = str(row["risk_name"]).strip()
        expiry_str = str(row["policy_expiry_date"]).strip()
        expiry_date = datetime.strptime(expiry_str.split()[0], "%Y-%m-%d").date()
        today = datetime.today().date()

        # Compose message
        if expiry_date < today:
            message = (
                f"Dear {name}, your insurance for {risk_name} expired on {expiry_date}. "
                "Visit our Chililabombwe office or call 0977188819 – ZSIC General Insurance"
            )
        else:
            message = (
                f"Dear {name}, your insurance for {risk_name} expires on {expiry_date}. "
                "Visit our Chililabombwe office or call 0977188819 – ZSIC General Insurance"
            )

        # Send SMS
        response = sms.send(message, [phone])
        logging.info(f"Sent to {phone}: {response}")

    except Exception as e:
        logging.error(f"Failed to process row {index + 1}: {e}")
