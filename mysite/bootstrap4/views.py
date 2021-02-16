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

            # create the config dictionary to pass into main
            inputs = {
                "user_url": request.POST.get("url"),
                "location": [request.POST.get("latitude"), request.POST.get("longitude")],
                "recommender": request.POST.get("rec")
            }

            # run the main code
            from run import main
            result = main(inputs)

            # return the value of the main code
            return render(request, 'index.html', template(form, result, inputs["location"][0], inputs["location"][1]))

        else:
            form = RecInputForm()

        return render(request, 'index.html', template(form, "bad submit"))

    form = RecInputForm()
    return render(request, 'index.html', template(form))
