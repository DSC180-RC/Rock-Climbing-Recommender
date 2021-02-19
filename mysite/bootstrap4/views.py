# Brian Cheng
# Eric Liu
# Brent Min

# views.py contains the logic needed to do form validation and render the various webpages of
# the heroku app

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.validators import URLValidator

from .forms import RecInputForm

import ast

import sys
sys.path.append('../../..')

def template(form=None, notes="", latitude=33.8734, longitude=-115.9010, results=[]):
    """
    A nice way to update all template inputs to the render functions all at once.

    :param:     form        The current contents of the main form. This input allows the site to
                            remember what the user has previously entered
    :param:     notes       Various notes to display to the user. Commonly used for debug messages
                            and reporting errors from form validation
    :param:     latitude    The latitude to display on the map. Default is at JTree
    :param:     longitude   The longitude to display on the map. Default is at JTree
    :param:     results     A list containing the recommendations. This is formatted by django
                            templates

    :return:    dict        A dictionary as shown below 
    """
    template_default = {
        "form": form,
        "notes": notes,
        "latitude": latitude,
        "longitude": longitude,
        "results": results
    }

    return template_default

def bootstrap4_index(request):
    # enter the if if the button is pressed on the website
    if(request.method == "POST"):

        form = RecInputForm(request.POST)

        if(form.is_valid()):

            # run the secondary validation code
            inputs = secondary_validation(form)

            # if there are errors, then the bool flag would be true
            if(inputs[1]):
                return render(request, 'index.html', template(form, inputs[1], 
                    inputs[0]["location"][0], inputs[0]["location"][1]))

            # run the main code
            from run import main
            results = main(inputs[0])

            # # transform the return dictionary into the proper format for django templates
            # trans_results = format_django(results)

            # return the value of the main code
            return render(request, 'index.html', template(form, results["notes"], 
                inputs[0]["location"][0], inputs[0]["location"][1], results["recommendations"]))

        return render(request, 'index.html', template(form))

    form = RecInputForm()
    return render(request, 'index.html', template(form))

# def format_django(results):
#     """
#     Take the output of the recommender and modify it so that django can automatically put it into
#     table form

#     :param:     results     The output of the recommender

#     :return:    [{"name", "url"}, etc.]     The input recommendations formatted such that django
#                                             template and correctly put them into a table
#     """
#     formatted = []
#     for key, value in ast.literal_eval(results)["name"].items():
#         formatted.append({
#             "name": value,
#             "url": f"https://www.mountainproject.com/route/{key}"
#         })

#     return formatted

def secondary_validation(form):  
    """
    This function runs some secondary validation code that I could not integrate into django
    without it messing up the website style

    :param:     form            The form containing cleaned data

    :return:    (dict, str)     The dict contains the input to the main function, and the string 
                                contains the error message (can be "")
    """
    # store error string here if necessary
    error_str = ""

    # get the url
    url = form.cleaned_data["url"]

    # validate the url structure
    validator = URLValidator()
    try:
        validator(url)
    except ValidationError:
        error_str += f"Mountain Project URL ({url}) is not a valid user page.\n"

    # validate that the url contains both "mountainproject.com" and "user"
    if((not error_str) and (("mountainproject.com" not in url) or ("user" not in url))):
        error_str += f"Mountain Project URL ({url}) is not a valid user page.\n"

    # get the boulder grades
    bl = int(form.cleaned_data["boulder_lower"])
    bu = int(form.cleaned_data["boulder_upper"])

    # validate the boulder grades if the box is checked
    if((form.cleaned_data["get_boulder"]) and (bl > bu)):
        error_str += f"Lowest Boulder Grade (V{bl}) should be less than or equal to Highest " \
            f"Boulder Grade (V{bu}).\n"

    # get the route grades
    rl = route_to_int(form.cleaned_data["route_lower"])
    ru = route_to_int(form.cleaned_data["route_upper"])

    # validate the route grades if the box is checked
    if(form.cleaned_data["get_route"]):
        if(rl is None):
            error_str += f"Lowest Route Grade (5.{form.cleaned_data['route_lower']}) is an " \
                "invalid difficulty.\n"
        if(ru is None):
            error_str += f"Highest Route Grade (5.{form.cleaned_data['route_upper']}) is an " \
                "invalid difficulty.\n"
        if((rl is not None) and (ru is not None)):
            if(rl > ru):
                error_str += f"Lowest Route Grade (5.{form.cleaned_data['route_lower']}) should " \
                    "be less than or equal to Highest Route Grade " \
                    f"(5.{form.cleaned_data['route_upper']}).\n"

    # create the config dictionary to pass into main
    inputs = {
        "user_url": form.cleaned_data["url"],
        "location": [form.cleaned_data["latitude"], form.cleaned_data["longitude"]],
        "max_distance": form.cleaned_data["max_distance"],
        "recommender": form.cleaned_data["rec"][0], # note for some reason ["rec"] is a list
        "num_recs": form.cleaned_data["num_recs"],
        "difficulty_range": {
            "boulder": [bl, bu],
            "route": [rl, ru]
        }
    }
    return (inputs, error_str)

def route_to_int(route_str):
    """
    This function takes a route string and turns it into an integer

    :param:     route_str   The stuff after the "5.". Can be anything from "1" to "15d"

    :return:    int         An integer representation of the grade
    """
    mapping = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10a", "10b", "10c", "10d", "11a", 
        "11b", "11c", "11d", "12a", "12b", "12c", "12d", "13a", "13b", "13c", "13d", "14a", "14b", 
        "14c", "14d", "15a", "15b", "15c", "15d"]

    try:
        return mapping.index(route_str.lower())
    except ValueError:
        return None
