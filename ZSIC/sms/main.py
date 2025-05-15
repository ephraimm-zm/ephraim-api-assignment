import pandas as pd
from datetime import datetime
import africastalking
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Africa's Talking credentials
username = "ephraimm-zm"  # Replace with your Africa's Talking username
api_key = "atsk_a49aedf62388d4d2813cd7adba6a39e2feea984c4beb66ee22a99fa6e6515550cde28a3b"    # Replace with your Africa's Talking API key

# Initialize Africa's Talking
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# Load the Excel file
df = pd.read_excel("sms-list.xlsx")

# Process each row
today = datetime.today().date()

for index, row in df.iterrows():
    try:
        name = str(row['name']).strip()
        raw_phone = str(int(float(row['phone_number1']))).strip()
        phone = f"+{raw_phone}" if raw_phone.startswith("260") else raw_phone
        risk_name = str(row['risk_name']).strip()
        expiry_date = pd.to_datetime(row['policy_expiry_date']).date()
        policy_number = str(row['policy_number']).strip()

        if expiry_date <= today:
            message = (
                f"Dear {name}, your insurance policy for {risk_name} expired on {expiry_date}. "
                "Visit our Chililabombwe office. For queries, concerns and options to renew your policy using Mobile Money, "
                "contact 0977188819. For reference you can present the following policy number: "
                f"{policy_number} – ZSIC General Insurance Chililabombwe Office"
            )
        else:
            message = (
                f"Dear {name}, your insurance policy for {risk_name} is expiring on {expiry_date}. "
                "Visit our Chililabombwe office. For queries, concerns and options to renew your policy using Mobile Money, "
                "contact 0977188819. For reference you can present the following policy number: "
                f"{policy_number} – ZSIC General Insurance Chililabombwe Office"
            )

        # Send SMS
        response = sms.send(message, [phone])
        logging.info(f"Sent to {phone}: {response}")
    except Exception as e:
        logging.error(f"Failed to process row {index + 1}: {e}")
