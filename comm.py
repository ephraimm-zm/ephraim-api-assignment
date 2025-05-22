import pandas as pd

# Load the Excel file
file_path = 'BNA-Commission-Claim-Form.xlsx'
df = pd.read_excel(file_path, header=18)  # Line 19 means header=18 (0-indexed)

# Calculate AMOUNT PAID MINUS LEVY (5%)
df['AMOUNT PAID MINUS LEVY'] = df['AMOUNT PAID'] * 0.95

# Function to determine commission rate based on DEBIT NOTE NUMBER
def get_commission_rate(note):
    try:
        parts = note.split('/')
        if len(parts) >= 3:
            code = parts[2]
            if code in ['204', '205']:
                return 0.20
            elif code in ['318', '310', '301']:
                return 0.125
            elif code in ['300', '347', '316', '309']:
                return 0.15
    except:
        pass
    return 0  # Default to 0 if pattern doesn't match

# Calculate Commission
df['Commission'] = df.apply(
    lambda row: row['AMOUNT PAID MINUS LEVY'] * get_commission_rate(str(row['DEBIT NOTE NUMBER'])), axis=1
)

# Save to new Excel file
df.to_excel('result.xlsx', index=False)  # Save without the original Excel formatting
