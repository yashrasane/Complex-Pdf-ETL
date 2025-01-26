
import re
import pdfplumber
import pandas as pd
from collections import namedtuple
# import sqlite3


# Define the namedtuple structureF
Line = namedtuple('Line', 'company_id company_name doctype reference currency voucher inv_date due_date open_amt_tc open_amt_bc current months1 months2 months3')

# Regular expressions for parsing
company_re = re.compile(r'(V\d+) (.*) Phone:')
line_re = re.compile(r'\d{2}/\d{2}/\d{4} \d{2}/\d{2}/\d{4}')

# Input PDF file
file = 'pone.pdf'

lines = []
total_check = 0

# Open the PDF file
with pdfplumber.open(file) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.split('\n'):
            comp = company_re.search(line)
            if comp:
                vend_no, vend_name = comp.group(1), comp.group(2)

            elif line.startswith('INVOICES'):
                doctype = 'INVOICE'

            elif line.startswith('CREDITNOTES'):
                doctype = 'CREDITNOTE'

            elif line_re.search(line):
                items = line.split()
                # Append parsed data as a namedtuple
                lines.append(Line(vend_no, vend_name, doctype, *items))

            elif line.startswith('Supplier total'):
                tot = float(line.split()[2].replace(',', ''))
                total_check += tot

# Convert lines to a pandas DataFrame
columns = ['Company ID', 'Company Name', 'Doc Type', 'Reference', 'Currency', 'Voucher',
           'Invoice Date', 'Due Date', 'Open Amount TC', 'Open Amount BC', 'Current',
           '1 Month', '2 Months', '3 Months']
df = pd.DataFrame(lines, columns=columns)




def needs_preprocessing(df):
    
    # Check if preprocessing is needed for the DataFrame.

    # Condition 1: Check for missing values
    if df.isnull().values.any():
        print("Preprocessing needed: Missing values detected.")
        return True

    # Condition 2: Check for non-numeric values in numeric columns
    numeric_columns = ["Open Amount TC", "Open Amount BC", "Current", "1 Month", "2 Months", "3 Months"]
    for col in numeric_columns:
        if col in df.columns:
            non_numeric = pd.to_numeric(df[col], errors='coerce').isnull().any()
            if non_numeric:
                print(f"Preprocessing needed: Non-numeric values found in column '{col}'.")
                return True

    # Condition 3: Check for invalid date formats
    date_columns = ["Invoice Date", "Due Date"]
    for col in date_columns:
        if col in df.columns:
            invalid_dates = pd.to_datetime(df[col], errors='coerce').isnull().any()
            if invalid_dates:
                print(f"Preprocessing needed: Invalid dates found in column '{col}'.")
                return True

    # Condition 4: Check for duplicate rows
    if df.duplicated().any():
        print("Preprocessing needed: Duplicate rows detected.")
        return True

    # If no issues are found
    print("No preprocessing needed.")
    return False

def preprocess(df):
   
    # Step 1: Handle missing values
    df = df.dropna(how="all")  # Drop rows where all elements are NaN
    df = df.fillna(value="")  # Replace remaining NaNs with empty strings

    # Step 2: Convert data types
    # Convert numeric columns to appropriate types
    numeric_columns = ["Open Amount TC", "Open Amount BC", "Current", "1 Month", "2 Months", "3 Months"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")  # Convert to float; invalid entries become NaN
            df[col] = df[col].fillna(0)  # Replace NaN with 0 for numeric columns

    # Step 3: Standardize date formats
    date_columns = ["Invoice Date", "Due Date"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")  # Convert to datetime; invalid entries become NaT
            df[col] = df[col].fillna(pd.Timestamp.min)  # Replace NaT with a default date

    # Step 4: Remove duplicates
    df = df.drop_duplicates()

    # Step 5: Clean text columns
    text_columns = ["Company Name", "Doc Type", "Reference", "Currency", "Voucher"]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].str.strip()  # Remove leading and trailing whitespaces

    # Step 6: Add derived columns (if needed)
    # Example: Calculate overdue days
    if "Due Date" in df.columns and "Invoice Date" in df.columns:
        df["Overdue Days"] = (df["Due Date"] - df["Invoice Date"]).dt.days

    print("Data preprocessing complete.")
    return df





if needs_preprocessing(df):
    print("Preprocessing is needed. Preprocessing data.......")
    preprocess(df)
else:
    print("No preprocessing needed.")
if not df.empty:
    output_file = 'output_data.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Data has been exported to {output_file}")
else:
    print("The data is not tabular and cannot be processed further.")

