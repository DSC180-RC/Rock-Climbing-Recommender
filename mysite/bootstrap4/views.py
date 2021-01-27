from django.shortcuts import render

import sys
sys.path.append('../../..')

def bootstrap4_index(request):
    if(request.method == "POST" and "run_script" in request.POST):
        from src.test_function import test_function
        x = test_function(5)
        return HttpResponse("test run")

    return render(request, 'index.html', {})
