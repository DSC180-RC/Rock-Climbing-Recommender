# Brian Cheng
# Eric Liu
# Brent Min

# get_raw_data.py contains all the logic needed to scrape data from the mountainproject website

import requests
import json

from bs4 import BeautifulSoup
from tqdm import tqdm

from src.functions import make_absolute

def get_raw_data(data_params):
    """
    This function collates all scraping logic

    :param:     data_params     A dictionary containing all data parameters. The only one used is
                                the location at which to save raw data
    """
    # store raw data here
    raw_data = []

    # for now, just scrape Yosemite routes
    area_url = "https://www.mountainproject.com/area/105833381/yosemite-national-park"
    # area_url = "https://www.mountainproject.com/area/113603736/the-box" # only 7 climbs!
    all_routes = find_all_routes_in_area(area_url)

    # for every route in Yosemite, get the route data
    for route_url in tqdm(all_routes):
        raw_data.append(get_route_data(route_url))

    # save the raw data
    with open(make_absolute(data_params["raw_data_folder"] + "yosemite.json"), "w") as f:
        json.dump(raw_data, f)

def get_route_data(route_url):
    """
    Get all route data for a single route

    :param:     route_url   The URL at which the route lives

    :return:    dict        A dictionary containing the following information:
                            "@context": N/A
                            "@type": N/A
                            "name": Name of the climb
                            "description": Description of the climb
                            "image": link to the climb image
                            "geo": dict with lat/long
                            "aggregateRating": dict with average rating/number of ratings
                            "route_url": url at which the route can be found
                            "user_ratings": dict with key user_id and value user_rating (0-4)
    """
    # get the climb description
    text = requests.get(route_url).text
    soup = BeautifulSoup(text, 'html.parser')

    # split up the stuff we want
    data = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
    description = soup.find('div', {'class': 'fr-view'}).contents
    data['description'] = ''.join([x for x in description if isinstance(x, str)])
    data['route_url'] = route_url

    # if there exists more than zero ratings for this climb, then get those user(s)
    if(int(data["aggregateRating"]["reviewCount"]) > 0):
        data["user_ratings"] = get_route_rating_data(route_url)
    # otherwise just add an empty dict
    else:
        data["user_ratings"] = {}

    return data

def get_route_rating_data(route_url):
    """
    Get all user_ids and the ratings for the input route

    :param:     route_url   The URL at which the route lives. NOTE (!) this is not the URL at which
                            rating data can be found, it is modified in this function

    :return:    dict        A dictionary containing the key of user_id and value of user rating
                            for the input climb url
    """
    # first modify the route_url to access the stats
    route_stats_url = route_url.split("/")
    route_stats_url.insert(4, "stats")
    route_stats_url = "/".join(route_stats_url)

    # get the html of the stats page
    text = requests.get(route_stats_url).text
    soup = BeautifulSoup(text, 'html.parser')

    # get the first table which should contain ratings
    ratings_table = soup.find("table", attrs={"class": "table"})

    # make sure that a table exists 
    if(ratings_table == None):
        print(route_stats_url)
        return {}

    # get the rows of the rating table
    rows = ratings_table.find_all("tr")
    
    # store ratings here
    user_ratings = {}

    # every single row is a users rating
    for row in rows:
        # first col contains the user_id
        cols = row.find_all("td")
        user_url = cols[0].find("a").get("href")
        user_id = user_url.split("/")[4]

        # second col contains the user rating (0-4 stars)
        stars = len(cols[1].find_all("img"))

        # the above interprets avoid (single image of a bomb) the same as one star (single image
        # of a star)
        # adjust for that
        if(stars == 1 and ("bomb" in cols[1].find("img")["src"])):
            stars = 0
        
        # store the rating
        user_ratings[user_id] = stars
            
    # return the ratings
    return user_ratings

def get_user_history(user_url):
    """
    Get all routes this user has climbed
    Note: this function is not used

    :param:     user_url    The URL of the user profile

    :return:    list        A list containing the url of all climbs this user has rated
    """
    # store links here
    links = []

    # get the html for the user
    text = requests.get(user_url + '/ticks').text
    soup = BeautifulSoup(text, 'html.parser')

    # iterate over each page of climbs that the user has done
    num_pages = int(soup.find_all('a', {"class":"no-click"})[2].contents[0].strip()[-1])
    for i in range(num_pages):
        text = requests.get(user + '/ticks?page=' + str(i + 1)).text

        # parse the page of climbs
        soup = BeautifulSoup(text, 'html.parser')

        # get and store all links to the climbs the user has done
        all_links = soup.find_all('a')
        for link in all_links:
            if len(link.find_all('strong')) > 0 and len(link) < 2:
                links.append({link.find('strong').contents[0]: link.get('href')})

    # return the list of links
    return links

def find_all_routes_in_area(area_url):
    """
    Get all the URLS of all the routes that exist in the input area

    :param:     area_url    The URL of the area to look in. It does not matter how high level of 
                            an area this URL points to, as long as it is an area of some sort
    """
    def add_links(soup):
        """
        TODO

        :param:     soup    TODO
        """
        # TODO: document function
        div = soup.find('div', {'class': 'max-height max-height-md-0 max-height-xs-400'})
        if div:
            a_hrefs = div.find_all('a')
            for link in a_hrefs:
                links.append(link.get('href'))
    # TODO: document function
    text = requests.get(area_url).text
    soup = BeautifulSoup(text, 'html.parser')
    links = []
    route_links = []
    add_links(soup)
    while len(links) > 0:
        link = links[0]
        if '/area/' in link:
            text = requests.get(link).text
            new_soup = BeautifulSoup(text, 'html.parser')
            add_links(new_soup)
        else:
            if link != '#':
                route_links.append(link)
        links.remove(link)
    return route_links