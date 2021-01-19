# Brian Cheng
# Eric Liu
# Brent Min

# run_data.py collates all data scraping and cleaning code into one convenient place

from src.data.get_raw_data import get_raw_data
from src.functions import *

def run_data():
    """
    This function collates all scraping and cleaning code into a single function called by run.py

    TODO: move the folders from a local string to a config file?
    """
    # create the folders in which to save data if the folders do not exist
    check_folder("data/")
    check_folder("data/raw")
    check_folder("data/cleaned")

    # get raw data
    get_raw_data()

    # clean data