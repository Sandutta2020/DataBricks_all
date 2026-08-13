import sys
from pipeline import PySparkJob

def main():
    order_path ='/Volumes/dbx_catalog/dbx_schema/orders_data/data_src'

    job =PySparkJob()
    print("<<< Loading and Cleaning Data >>>>")
    orders_df =job.load_and_clean_data(order_path)
    orders_df.show(5,truncate=False)
    job.stop()
if __name__ == "__main__":
    main()