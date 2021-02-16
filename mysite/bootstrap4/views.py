from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import RecInputForm

import sys
sys.path.append('../../..')

def template(form=None, rec="", latitude=33.8734, longitude=-115.9010):
    """
    TODO

    TODO
    """
    template_default = {
        "form": form,
        "recommendations": rec,
        "latitude": latitude,
        "longitude": longitude
    }

    return template_default

def bootstrap4_index(request):
    # enter the if if the button is pressed on the website
    if(request.method == "POST"):

        form = RecInputForm(request.POST)

        if(form.is_valid()):

            # run the secondary validation code
            inputs = secondary_validation(request)

            # if there are errors, then the bool flag would be true
            if(inputs[0]):
                return render(request, 'index.html', template(form, inputs[2], 
                    inputs[1]["location"][0], inputs[1]["location"][1]))

            # run the main code
            from run import main
            result = main(inputs[1])

            # return the value of the main code
            return render(request, 'index.html', template(form, result, inputs[1]["location"][0], 
                inputs[1]["location"][1]))

        return render(request, 'index.html', template(form))

    form = RecInputForm()
    return render(request, 'index.html', template(form))

def secondary_validation(request):
    """
    This function runs some secondary validation code that I could not integrate into django
    without it messing up the website style

    :param:     request     The POST request

    :return:    (bool, dict, str)   The bool is if there is an error, the dict contains the input
                                    to the main function, and the string contains the error message
    """
    # store error string here if necessary
    error_str = ""

    # get the boulder grades
    bl = request.POST.get("boulder_lower")
    bu = request.POST.get("boulder_upper")

    # validate the boulder grades
    if(bl > bu):
        error_str += "Lowest Boulder Grade should be less than or equal to Highest Boulder Grade.\n"

    # get the route grades
    rl = route_to_int(request.POST.get("route_lower"))
    ru = route_to_int(request.POST.get("route_upper"))

    # validate the route grades
    if(rl is None):
        error_str += "Lowest Route Grade is an invalid difficulty.\n"
    if(ru is None):
        error_str += "Highest Route Grade is an invalid difficulty.\n"
    if((rl is not None) and (ru is not None)):
        if(rl > ru):
            error_str += "Lowest Route Grade should be less than or equal to Highest Route Grade.\n"

    # create the config dictionary to pass into main
    inputs = {
        "user_url": request.POST.get("url"),
        "location": [request.POST.get("latitude"), request.POST.get("longitude")],
        "recommender": request.POST.get("rec"),
        "num_recs": request.POST.get("num_recs"),
        "difficulty_range": {
            "boulder": [bl, bu],
            "route": [rl, ru]
        }
    }
    return (not error_str, inputs, error_str)

def route_to_int(route_str):
    """
    This function takes a route string and turns it into an integer

    :param:     route_str   The stuff after the "5.". Can be anything from "1" to "15d"

    :return:    int         An integer representation of the grade
    """
    mapping = ["1", "2", "3", "4", "5", "6", "7", "", "8", "9", "10a", "10b", "10c", "10d", "11a", 
        "11b", "11c", "11d", "12a", "12b", "12c", "12d", "13a", "13b", "13c", "13d", "14a", "14b", 
        "14c", "14d", "15a", "15b", "15c", "15d"]

    try:
        return mapping.index(route_str)
    except ValueError:
        return None
