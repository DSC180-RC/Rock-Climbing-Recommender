# Brian Cheng
# Eric Liu
# Brent Min

# top_pop.py contains all the logic needed to return the most basic top 10 most popular/well received routes

import pandas as pd
from pymongo import MongoClient

from src.functions import make_absolute

def top_pop(args=None, data_params=None, web_params=None):
    """
    TODO

    :param:     args            TODO
    :param:     data_params     TODO
    :param:     web_params      TODO
    """
    # change behavior if testing
    if((args is not None) and args["test"]):
        # get the url at which raw data will be found
        clean_data_path = make_absolute(data_params["clean_data_folder"] + "climbs.csv")
        print(clean_data_path)
        
        # get the data
        df = pd.read_csv(clean_data_path)
    else:
        # accessing the data from our MongoDB
        client = MongoClient('mongodb+srv://DSC102:coliniscool@cluster0.4gstr.mongodb.net/MountainProject?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
        
        # get the data
        climbs = client.MountainProject.climbs
        df = pd.DataFrame.from_records(list(climbs.find()))

    # TODO: filter by location

    # TODO: filter by difficulty

    # TODO: filter by type of climb
    
    # returns a a simple TopPopular in dict format
    toppop = df[df['avg_rating'] >= 3.5].sort_values('num_ratings', ascending=False)[:10]

    # create the formatted recommendations dict
    result = list(toppop[['climb_id', 'name']].apply(lambda x: {"name": x[1], "url": x[0]}, axis=1))

    # make sure the correct number of climbs were returned
    notes = ""
    if(len(result) < web_params["num_recs"]):
        notes = f"Could not generate {web_params['num_recs']} recommendations based on the " \
            "selected options."

    result = {"recommendations": result, "notes": notes}

    return result