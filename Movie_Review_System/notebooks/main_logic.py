import sys
import os
import logging
import argparse
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, current_timestamp
root_path = "/Workspace/Users/sandutta2020@gmail.com/DataBricks_all/Movie_Review_System"
if root_path not in sys.path:
    sys.path.insert(0, root_path)
from src.job.pipeline import PySparkJob
from src.utils.config_loader import load_config
from src.utils.logger_utils import get_logger
def main(run_id):
    logger = get_logger("process_data_module")
    try:
        # -------------------------------------------------------
        # Loading Configuration --->
        # -------------------------------------------------------        
        cfg =load_config()
        print(cfg)
        job_name   = cfg.get('job_name', 'lure_pipeline')
        env        = cfg.get('env', 'DEV')                  # DEV | PROD
        logger.info("Lure Data Analysis Job  started---------Main logic")
        job =PySparkJob()
        logger.info("<<< PySparkJob object creation succeeded")
        print("<<< PySparkJob object creation succeeded")
        logger.info("<<< Loading configuration--------------- >>>>")
        job_name = cfg['job_name']
        logger.info(f"Lure Data analysis job : {job_name} started")
        landing_path = cfg.get('paths', {}).get('landing')
        processing_path = cfg.get('paths', {}).get('processing')
        archive_path = cfg.get('paths', {}).get('archived')
        log_path   = cfg.get('paths', {}).get('logpath')
        # -------------------------------------------------------
        # Move file: Landing → Processing
        # -------------------------------------------------------
        logger.info(f"landing_path : --> {landing_path} processing_path :--> {processing_path}")
        if(job.move_file(landing_path,processing_path)):
            logger.info("<<< File move successful,Processing for next step >>>>")
        else:
            logger.error("<<< No Files for processing ,Hence quitting ...>>>>")
            return
        # -------------------------------------------------------
        # Ingesting the loading and cleaning data
        # -------------------------------------------------------        
        logger.info("<<< Loading and Cleaning Data started >>>>")
        lure_oracle_df =job.load_and_clean_data(processing_path)
        logger.info("<<< Loading and Cleaning Data  Ended>>>>")
        # -------------------------------------------------------
        # Ingesting the loading and cleaning data
        # ------------------------------------------------------- 
        lure_table_name = cfg.get('tables',{}).get('movie_rating_bronze')
        logger.info("<<< Writing Data to Bronze Table >>>> ---{lure_table_name}")
        job.write_to_bronze(lure_oracle_df,lure_table_name)
        logger.info("<<< Writing Data to Bronze Table Ended >>>>")
        # -------------------------------------------------------
        # Move file: Processing → Archive
        # -------------------------------------------------------
        logger.info("<<< Data Processing successfull, now  moving processed to archive folder>>>")
        logger.info(f"Processing path : --> {processing_path} archived path :--> {archive_path}")       
        if(job.move_file(processing_path,archive_path)):
            logger.info("<<< File moved to archive foler successfully >>>>")
        else:
            print("<<< File moved failed>>>>")


    except Exception as e:
        logger.info("-----In exception ------------")
        logger.error(f"Job failed with an unexpected error: {str(e)}", exc_info=True)
        if job:
            logger.info("Stopping Spark session .")
            job.stop()
        raise
    finally:
        # 7. Cleanup
        logger.info("-----In Finally ------------")
        if job:
            logger.info("Stopping Spark session.")
            job.stop()
        # CRITICAL: Force flush logs to the Unity Catalog Volume
        logger.info("Shutting down logging system and flushing buffers.")
        logging.shutdown()
    job.stop()
if __name__ == "__main__":
    print(f"Received args: {sys.argv}")
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_id", type=str, help="The Databricks Job Run ID")
    parser.add_argument("--job_id", type=str, help="The Databricks Job Run ID")
    args = parser.parse_args()    
    run_id = args.run_id
    print(f"Currently executing Run ID: {run_id} for job_id: {args.job_id}")
    main(run_id)