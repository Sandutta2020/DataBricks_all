# Databricks notebook source
# MAGIC %run ./Classroom-Setup-Common

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG IDENTIFIER(DA.catalog_name);
# MAGIC USE SCHEMA IDENTIFIER(DA.schema_name);

# COMMAND ----------

import csv

def corrupt_first_order_id(input_csv, output_csv):
    """
    Keeps only the first 5 rows and first 3 columns,
    and replaces the first order_id value with 'aaa'.
    """
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=',')
        rows = list(reader)

    # Keep only the first 5 rows and first 3 columns
    trimmed_rows = [row[:3] for row in rows[:5]]
    print(trimmed_rows)
    # Replace the first order_id in the first data row (row index 1) with 'aaa'
    if len(trimmed_rows) > 1:
        trimmed_rows[1][2] = 'aaa'

    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerows(trimmed_rows)

username_cleaned = DA.username.replace('.', '_')
# Example usage
corrupt_first_order_id(
    '/Volumes/dbx_catalog/dbx_schema/dbx_volume/csv_for_copy_into/Virginia.csv.csv',
    '/Volumes/dbx_catalog/dbx_schema/dbx_volume/csv_for_copy_into/malformed_Virginia.csv'
)

# COMMAND ----------

import csv

def blank_out_first_header_and_trim_five_rows(input_csv, output_csv):
    """
    Keeps only the first 5 rows and first 3 columns, and blanks out the first column header.
    """
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=',')  # <-- Key fix here
        rows = list(reader)

    # Keep only the first 5 rows and first 3 columns
    trimmed_rows = [row[:3] for row in rows[:5]]

    # Replace only the first header value with an empty string
    if trimmed_rows:
        trimmed_rows[0][0] = ''
    print(trimmed_rows)
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=',')  # Match delimiter here too
        writer.writerows(trimmed_rows)

# Example usage
blank_out_first_header_and_trim_five_rows(
    '/Volumes/dbx_catalog/dbx_schema/dbx_volume/csv_for_copy_into/Virginia.csv.csv',
   '/Volumes/dbx_catalog/dbx_schema/dbx_volume/csv_for_copy_into/missing_header_Virginia.csv'
)
