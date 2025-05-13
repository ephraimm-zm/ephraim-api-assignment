import pandas as pd

# Initialize the Debits list
debits = []

# Helper function to check if a debit note number exists in the debits list
def debit_exists(debit_note_number):
    return any(debit["Debit_note_number"] == debit_note_number for debit in debits)

# Process CUsr-Comm-Claim-Form.csv
usr_df = pd.read_csv("CUsr-Comm-Claim-Form.csv")

for _, row in usr_df.iterrows():
    debit_note = str(row["DEBIT NOTE NUMBER"]).strip()
    amount = row["DEBITED AMOUNT"]

    if not debit_exists(debit_note):
        debits.append({
            "Debit_note_number": debit_note,
            "Amount": amount
        })

# Process CSys-Comm-Claim-Form.csv
sys_df = pd.read_csv("CSys-Comm-Claim-Form.csv")

for _, row in sys_df.iterrows():
    debit_note = str(row["DEBIT NOTE NUMBER"]).strip()
    amount = row["GROSS PREMIUM"]

    if not debit_exists(debit_note):
        debits.append({
            "Debit_note_number": debit_note,
            "Amount": amount
        })

# Convert to DataFrame and export to Excel
debits_df = pd.DataFrame(debits)
debits_df.to_excel("Debits_List.xlsx", index=False)

