import sys
from pipeline import PySparkJob

def main():
    order_path ='/Volumes/dbx_catalog/dbx_schema/orders_data/data_src'

    job =PySparkJob()
    print("<<< PySparkJob object creation succeeded")
    print("<<< Loading and Cleaning Data >>>>")
    orders_df =job.load_and_clean_data(order_path)
    sample_data = orders_df.limit(5).collect()
    for row in sample_data:
        print(f"Processing: {row}")
    job.stop()
if __name__ == "__main__":
    main()