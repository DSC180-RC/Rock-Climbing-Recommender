from django.shortcuts import render

import sys
sys.path.append('../../..')

def bootstrap4_index(request):
    if(request.method == "POST" and "run_script" in request.POST):
        from run import main

        config = {"mongodb": True, "top_pop": True}

        result = main(config)
        return render(request, 'index.html', {"test": result})

    return render(request, 'index.html', {"test": "test"})
