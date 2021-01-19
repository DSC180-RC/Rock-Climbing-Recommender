# Brian Cheng
# Eric Liu
# Brent Min

# run_data.py collates all data scraping and cleaning code into one convenient place

from src.data.get_raw_data import get_raw_data
from src.functions import check_folder

def run_data():
    """
    TODO
    """
    # create the folders in which to save data if the folders do not exist
    check_folder("data/")
    check_folder("data/raw")
    check_folder("data/cleaned")

    # get raw data
    get_raw_data()

    # clean data