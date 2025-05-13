import pandas as pd

# Load Usr-Comm-Claim-Form starting from row 16 (i.e., header=15)
usr_df = pd.read_excel("Usr-Comm-Claim-Form.xlsx", header=15)
usr_df.columns = usr_df.columns.str.strip()

# Load Sys-Comm-Claim-Form starting from row 17 (i.e., header=16)
sys_df = pd.read_excel("Sys-Comm-Claim-Form.xlsx", header=16)
sys_df.columns = sys_df.columns.str.strip()

# Clean column names
usr_cols = ["INSURED", "DEBIT NOTE NUMBER", "DEBITED AMOUNT", "AMOUNT PAID"]
sys_cols = ["INSURED", "DEBIT NOTE NUMBER", "GROSS PREMIUM", "PREMIUM PAID"]

# Filter and rename Usr data
usr_data = usr_df[[col for col in usr_cols if col in usr_df.columns]].copy()
usr_data.rename(columns={"DEBITED AMOUNT": "DEBITED", "AMOUNT PAID": "PAID"}, inplace=True)

# Filter and rename Sys data
sys_data = sys_df[[col for col in sys_cols if col in sys_df.columns]].copy()
sys_data.rename(columns={
    "GROSS PREMIUM": "DEBITED",
    "PREMIUM PAID": "PAID"
}, inplace=True)

# Combine both dataframes
combined = pd.concat([
    usr_data[["INSURED", "DEBIT NOTE NUMBER", "DEBITED", "PAID"]],
    sys_data[["INSURED", "DEBIT NOTE NUMBER", "DEBITED", "PAID"]]
], ignore_index=True)

# Drop duplicates based on INSURED + DEBIT NOTE NUMBER
results = combined.drop_duplicates(subset=["INSURED", "DEBIT NOTE NUMBER"])

# Save to Excel
results.to_excel("Results.xlsx", index=False)
print("Results.xlsx created.")
