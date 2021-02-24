# Brian Cheng
# Eric Liu
# Brent Min

# model_functions.py contains various functions useful across all recommender models.

import math

def distance(start_lat_lng, end_lat_lng):
    """
    This function returns the distance between two lat/lng pairs in miles

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