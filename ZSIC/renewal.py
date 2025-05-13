import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load files
policy_file = "PolicyRenewalRegister.csv"
debit_file = "DebitSettlements.csv"
customer_file = "CustomerList.csv"

# Load PolicyRenewalRegister
try:
    policy_df = pd.read_csv(policy_file)
    logging.info("Loaded PolicyRenewalRegister.csv")
except Exception as e:
    logging.error(f"Error loading {policy_file}: {e}")
    raise
policy_df.columns = policy_df.columns.str.strip()

# Load DebitSettlements
try:
    debit_df = pd.read_csv(debit_file)
    logging.info("Loaded DebitSettlements.csv")
except Exception as e:
    logging.error(f"Error loading {debit_file}: {e}")
    raise
debit_df.columns = debit_df.columns.str.strip()

print("PolicyRenewalRegister columns:", list(policy_df.columns))
print("DebitSettlements columns:", list(debit_df.columns))

# Load CustomerList
try:
    customer_df = pd.read_csv(customer_file, low_memory=False)
    logging.info("Loaded CustomerList.csv")
except Exception as e:
    logging.error(f"Error loading {customer_file}: {e}")
    raise
customer_df.columns = customer_df.columns.str.strip()
print("CustomerList columns:", list(customer_df.columns))

# Create Result list
results = []

# Step 1: Extract data from PolicyRenewalRegister
for _, row in policy_df.iterrows():
    try:
        policy_number = str(row.get("Policy No", "")).strip()
        risk_name = str(row.get("Risk Name", "")).strip()
        name = str(row.get("Insured Name", "")).strip()
        expiry_raw = str(row.get("Policy Period To", "")).strip()

        # Parse date if valid
        if not expiry_raw or expiry_raw.lower() == 'nan':
            logging.warning("Skipping row due to missing or invalid date: %s", expiry_raw)
            continue
        try:
            expiry_date = datetime.strptime(expiry_raw, "%d/%m/%Y").date()
        except ValueError:
            logging.warning("Skipping row due to date format error: %s", expiry_raw)
            continue

        results.append({
            "name": name,
            "phone_number1": "",
            "risk_name": risk_name,
            "policy_expiry_date": expiry_date,
            "customer_code": "",
            "policy_number": policy_number
        })
    except Exception as e:
        logging.warning(f"Error processing policy row: {e}")

# Step 2: Match with DebitSettlements to fill in customer_code
for result in results:
    match = debit_df[debit_df["Policy No"].astype(str).str.strip() == result["policy_number"]]
    if not match.empty:
        debtor = str(match.iloc[0].get("Debtor", "")).strip()
        result["customer_code"] = debtor[:9]

# Step 3: Match with CustomerList to fill in phone_number1
for result in results:
    if result["customer_code"]:
        match = customer_df[customer_df["CUST_CODE"].astype(str).str[:9] == result["customer_code"]]
        if not match.empty:
            result["phone_number1"] = str(match.iloc[0].get("PHONE_1", "")).strip()

# Export to Excel
result_df = pd.DataFrame(results)
result_df.to_excel("Results.xlsx", index=False)
logging.info("Exported Results.xlsx")
