# Brian Cheng
# Eric Liu
# Brent Min

# model_functions.py contains various functions useful across all recommender models.

import pandas as pd

import math

def filter_df(df, location, distance, diff_ranges):
    """
    This function filters the input df based on the other three paramters, using the functions 
    below

    :param:     df              The input df to filter. It is expected at minimum to have the 
                                columns "latitude", "longitude", "boulder_climb", "rock_climb", 
                                and "difficulty"
    :param:     location        The center location. A lat/lng pair
    :param:     distance        The distance from the center location in miles
    :param:     diff_ranges     A dictionary of the following format: {"boulder": [int, int],
                                "route": [int, int]}. Typically, these values are generated by the
                                website. If the user does not want a type of climb, the list will
                                be [-1, -1]

    :return:    pd.DataFrame    The input df filtered based on the parameters
    """
    # in order to reduce compute time, first filter by difficulty
    df = filter_type_difficulty(df, diff_ranges)

    # make sure that the df is not empty before filtering by location
    if(len(df.index) == 0):
        return df

    # now filter by location
    df["dis_mi"] = df.apply(lambda x: distance(location, [x["latitude"], x["longitude"]]), axis=1)
    df = df.loc[df["dis_mi"] <= distance]

    # return the filtered df
    return df

def distance(start_lat_lng, end_lat_lng):
    """
    This function returns the distance between two lat/lng pairs in miles
    TODO: use a approximation function to cut down on compute time?

    :param:     start_lat_lng   The first lat/lng pair. Any of list, tuple, iterable, etc.
    :param:     end_lat_lng     The second lat/lng pair. Any of list, tuple, iterable, etc.
        
    :return:    float           The distance between the two lat/lng pairs in miles
    """
    # earth radius in miles
    _radius = 3958.8

    # convert all lat/lng to radians
    start_lat_lng = (math.radians(start_lat_lng[0]), math.radians(start_lat_lng[1]))
    end_lat_lng = (math.radians(end_lat_lng[0]), math.radians(end_lat_lng[1]))

    # get the differences between the lats/lngs
    lat_distance = end_lat_lng[0] - start_lat_lng[0]
    lng_distance = end_lat_lng[1] - start_lat_lng[1]

    # apply the haversine formula: https://www.movable-type.co.uk/scripts/latlong.html
    a = (math.sin(lat_distance / 2) ** 2) + \
            (math.cos(start_lat_lng[0]) * math.cos(end_lat_lng[0]) * \
            (math.sin(lng_distance / 2) ** 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = _radius * c

    # since the initial radius was in miles, the final distance should also be in miles
    return d

def filter_type_difficulty(df, diff_ranges):
    """
    This function takes the input df and filters it by climb type and by difficulty

    :param:     df              A pandas dataframe. It is expected at minimum to have the columns 
                                "boulder_climb", "rock_climb", and "difficulty"
    :param:     diff_ranges     A dictionary of the following format: {"boulder": [int, int],
                                "route": [int, int]}. Typically, these values are generated by the
                                website. If the user does not want a type of climb, the list will
                                be [-1, -1]

    :return:    pd.DataFrame    The input df filtered based on the parameters
    """
    # check if the user wants bouders
    if(diff_ranges["boulder"][0] != -1):
        # if the user wants boulders, filter by difficulty
        df = df.loc[(df["boulder_climb"] == 1) & \
            (df["difficulty"] >= diff_ranges["boulder"][0]) & \
            (df["difficulty"] <= diff_ranges["boulder"][1])]
    else:
        # if the user does not want boulders, remove all boulders
        df = df.loc[df["boulder_climb"] == 0]

    # check if the user wants routes
    if(diff_ranges["route"][0] != -1):
        # if the user wants routes, filter by difficulty
        df = df.loc[(df["rock_climb"] == 1) & \
            (df["difficulty"] >= diff_ranges["route"][0]) & \
            (df["difficulty"] <= diff_ranges["route"][1])]
    else:
        # if the user does not want boulders, remove all boulders
        df = df.loc[df["rock_climb"] == 0]

    # return the filtered df
    return df
