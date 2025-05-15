import pandas as pd

# Load the Excel file
input_file = "sms-list-with-status.xlsx"
output_file = "not-sent.xlsx"

# Read the file
df = pd.read_excel(input_file)

# Function to check if a value can be interpreted as an integer
def is_int(val):
    try:
        int(str(val).strip())
        return True
    except:
        return False

# Filter rows based on your conditions
filtered_df = df[
    df['phone_number1'].apply(is_int) &
    ~df['Status'].isin(['Success', 'Sent'])
]

# Save the filtered data to a new Excel file
filtered_df.to_excel(output_file, index=False)

print("Filtered file saved as:", output_file)
