import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def get_logger(module_name):
    """
    Configures a logger that writes to a Unity Catalog Volume and the console.
    """
    # The Unity Catalog Volume path verified in your environment
    log_directory = "/Volumes/Movie_Demo/Movie_Schema/movie_vol/logDir/"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_name  = f"{module_name}_{timestamp}.log"
    log_file = os.path.join(log_directory,log_name)

    # Ensure the Volume directory exists
    try:
        os.makedirs(log_directory, exist_ok=True)
    except Exception as e:
        # Fallback print if the filesystem is unreachable
        print(f"CRITICAL: Error creating log directory: {e}")

    logger = logging.getLogger(module_name)
    
    # Set global logging level
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if the logger is already initialized 
    # (Crucial for Databricks notebook environments)
    if not logger.handlers:
        # 1. File Handler (Writes to the Volume)
        # delay=False ensures the file is created/opened as soon as the handler is added
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024, # 10MB
            backupCount=5,
            delay=False
        )
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # 2. Console Handler (Shows logs in Databricks cell output)
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(name)s - %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Prevent logs from propagating to the Databricks root logger 
        # This stops the "double log" effect in notebooks
        logger.propagate = False

    return logger
