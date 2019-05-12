from django.shortcuts import render
from django.http import HttpResponse

import json

from .models import Emergency_Group, Condition


# Create your views here.
def toolhome(request):
    if request.method == 'POST':
        pass
    else:
        emergencygroups = []
        for emergencygroup in Emergency_Group.objects.all():
            emergencygroups.append(emergencygroup)
    return render(request, "emergency/index.html",
                  {
                      'emergencygroups': emergencygroups
                  })


def get_conditions_by_name(request):
    print('here')
    if request.is_ajax():
        print('here ajax')
        q = request.GET.get('term', '').capitalize()
        print('q =', q)
        search_qs = Condition.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
    else:
        data = 'none'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_condition_pill(request):
    tag = request.GET.get('tag', '').capitalize()
    response = HttpResponse()
    response.write('<div class="condition-pill">')
    response.write(f'<label class="pill-name">{tag}</label>')
    response.write('<button class="pill-close">x</button>')
    response.write('</div>')
    return response


# get_varieties_for_condition(request, condition), for ajax calls
def get_varieties_for_condition(request):
    condition = request.GET.get('condition', '')
