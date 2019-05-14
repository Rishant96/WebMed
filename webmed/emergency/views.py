from django.shortcuts import render
from django.http import HttpResponse

import json

from .models import Emergency_Group, Emergency
from .models import Condition, Variety


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


def get_condition_variety(request):
    tag = request.GET.get('tag', '').capitalize()
    condition_var = Condition.objects.get(name=tag)

    if 'conditions' not in request.session:
        request.session['conditions'] = []
    request.session['conditions'].append(condition_var)
    print('request.session["conditions"] =', request.session['conditions'])

    varieties = (Variety.objects.filter(condition=condition_var)
                 .values('name'))
    response_data = json.dumps(list(varieties))
    return HttpResponse(response_data, content_type=response_data)
