import pandas as pd

# File paths
sms_list_path = "sms-list.xlsx"
bulk_messages_path = "BulkMessages-e.mulilo1@alustudent.com-2025-05-14.csv"
output_path = "sms-list-with-status.xlsx"

# Read the input files
sms_df = pd.read_excel(sms_list_path)
bulk_df = pd.read_csv(bulk_messages_path)

# Function to find status by checking if risk_name is in the Message
def find_status(risk):
    match = bulk_df[bulk_df['Message'].astype(str).str.contains(str(risk), na=False)]
    if not match.empty:
        return match.iloc[0]['Status']
    return 'Not Found'

# Apply the function to each row in sms_df
sms_df['Status'] = sms_df['risk_name'].apply(find_status)

# Save the updated DataFrame
sms_df.to_excel(output_path, index=False)

print("File saved as:", output_path)
