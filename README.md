# PDF ETL (Extract, Transform, Load) Pipeline
## Overview
This project is a Python-based ETL pipeline designed to process complex, unstructured PDF documents. It extracts text and tabular data, validates and preprocesses the data, and exports it to an Excel file. The project also includes mechanisms to detect whether preprocessing is required and handle missing or invalid data.

## Dataset used
- <a href="https://github.com/yashrasane/Complex-Pdf-ETL/blob/db927768af00c84a576d481ee5de44475afddef2/Dataset.pdf">Dataset</a>

## Features
-Extracts text and tabular data from PDFs using pdfplumber.

-Parses structured information, such as company details, document type, and financial data.

-Validates data for missing values, non-numeric entries, invalid date formats, and duplicates.

-Preprocesses data (handles missing values, converts data types, standardizes date formats, removes duplicates).

-Exports clean, structured data to an Excel file for further use.

-(Optional) Stores processed data in a database for future analysis.

Excel Interaction <a href="https://github.com/yashrasane/Complex-Pdf-ETL/blob/db927768af00c84a576d481ee5de44475afddef2/output_data.xlsx">View Output</a>

## Dependencies
-pdfplumber (for PDF parsing)

-pandas (for data handling and export)

-re (for regular expressions)

-collections (for named tuples)


## Dashboard

![Screenshot (495)](https://github.com/yashrasane/Complex-Pdf-ETL/blob/0734eb29232e8bf459f581b52e4a3f4fc3820ee8/Output.jpeg)

## Code Highlights
-Data Extraction: Utilizes pdfplumber to extract text and tables from unstructured PDFs.

-Data Cleaning:Handles missing and invalid data in numeric and date fields.Removes duplicate rows.

-Custom Derived Columns:Calculates fields like overdue days based on invoice and due dates.

-Flexible Pipeline:Skips preprocessing if the data is already clean.

-Outputs results directly to an Excel file.
