# Brian Cheng
# Eric Liu
# Brent Min

# top_pop.py contains a top popular recommender, where climbs are first filtered to those over
# 3.5/4 stars, then sorted by number of reviews.

import pandas as pd
from pymongo import MongoClient

from src.functions import make_absolute
from src.model.model_functions import filter_df

from math import sin, cos, sqrt, atan2, radians

def top_pop(args=None, data_params=None, web_params=None):
    """
    A simple top popular which takes climbs over 3.5/4 stars and returns those climbs with the
    most number of reviews.

    :param:     args            Command line arguments
    :param:     data_params     Data params for running the project from the command line
    :param:     web_params      Params from the website

    :return:    dict            A dictionary in the following format:   
                                {
                                    "recommendations": [{"name": str, "url": int, "reason": str,
                                        "difficulty": str, "description": str}, {}, ...],
                                    "notes": str
                                }
                                Where each item in the "recommendations" list is a singular 
                                recommendation. All recommenders should return in this format
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

    # cleans the data
    df['climb_type'] = df['climb_type'].apply(lambda x: x.strip('][').split(', '))

    # returns a simple TopPopular
    toppop = df[df['avg_rating'] >= 3.5].sort_values('num_ratings', ascending=False)

    # # filter by location
    # def calc_distance(x):
    #     # approximate radius of earth in km
    #     R = 6373.0
    #     lat1 = radians(web_params['location'][0])
    #     lon1 = radians(web_params['location'][1])
    #     lat2 = radians(x['latitude'])
    #     lon2 = radians(x['longitude'])
    #     dlon = lon2 - lon1
    #     dlat = lat2 - lat1
    #     a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    #     c = 2 * atan2(sqrt(a), sqrt(1 - a))
    #     distance = R * c * 0.621371 #convert to miles by multiplying by 0.621371
    #     return distance
    # toppop = toppop[toppop.apply(calc_distance, axis=1) <= web_params['max_distance']]
    
    # # filter by type of climb and difficulty
    # def type_and_difficulty_check(x):
    #     if x['boulder_climb'] == 1 and x['difficulty'] >= web_params['difficulty_range']['boulder'][0] and x['difficulty'] <= web_params['difficulty_range']['boulder'][1]:
    #         return True
    #     if x['rock_climb'] == 1 and x['difficulty'] >= web_params['difficulty_range']['route'][0] and x['difficulty'] <= web_params['difficulty_range']['route'][1]:
    #         return True
    #     return False
    # toppop = toppop[toppop.apply(type_and_difficulty_check, axis=1)]

    # web_params = {
    #     "location": [37.709807, -119.566228],
    #     "max_distance": 50,
    #     "difficulty_range": {
    #         "boulder": [0, 3],
    #         "route": [0, 15]
    #     },
    #     "num_recs": 10
    # }

    toppop = filter_df(toppop, web_params["location"], web_params["max_distance"], 
        web_params["difficulty_range"])
    
    # create the formatted recommendations dict based on the number of recommendations to output
    result = list(toppop[['climb_id', 'name']][:web_params['num_recs']].apply(lambda x: {"name": x[1], "url": x[0]}, axis=1))

    # make sure the correct number of climbs were returned
    notes = ""
    if(len(result) < web_params["num_recs"]):
        notes = f"Could not generate {web_params['num_recs']} recommendations based on the " \
            "selected options."

    result = {"recommendations": result, "notes": notes}

    return result