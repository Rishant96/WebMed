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
        if 'conditions' in request.session:
            del request.session['conditions']
        if 'usedconditions' in request.session:
            del request.session['usedconditions']
        emergencygroups = []
        for emergencygroup in Emergency_Group.objects.all():
            emergencygroups.append(emergencygroup)
    return render(request, "emergency/index.html",
                  {
                      'emergencygroups': emergencygroups
                  })


def get_conditions_by_name(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        if 'usedconditions' in request.session:
            pks = request.session['usedconditions']
        else:
            pks = []
        search_qs = Condition.objects.filter(name__startswith=q)\
            .exclude(pk__in=pks)
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

    request.session['currentcondition'] = condition_var.pk

    varieties = (Variety.objects.filter(condition=condition_var)
                 .values('name', 'pk'))

    response_data = json.dumps(list(varieties))
    mimetype = 'application/json'
    return HttpResponse(response_data, mimetype)


def set_variety(request):
    mimetype = 'application/json'
    tag = request.GET.get('tag', '').capitalize()
    variety_pk = int(tag)
    variety = Variety.objects.filter(pk=tag).values(
        'name', 'pk')[0]
    if 'currentcondition' not in request.session:
        return HttpResponse({}, mimetype)
    condition_pk = request.session['currentcondition']
    condition = Condition.objects.filter(pk=condition_pk).values(
        'name', 'pk')[0]

    condition_name = condition['name']
    variety_name = variety['name']

    response = [{'name': condition_name, 'pk': condition_pk},
                {'name': variety_name, 'pk': variety_pk}]
    response_data = json.dumps(response)

    if 'conditions' not in request.session:
        request.session['conditions'] = []

    if 'usedconditions' not in request.session:
        request.session['usedconditions'] = []

    conditions = request.session['conditions']
    conditions.append([condition_pk, variety_pk])

    usedconditions = request.session['usedconditions']
    usedconditions.append(condition_pk)

    request.session['conditions'] = conditions
    request.session['usedconditions'] = usedconditions
    return HttpResponse(response_data, mimetype)


def no_variety(request):
    mimetype = 'application/json'
    if 'currentcondition' in request.session:
        currentcondition_pk = request.session['currentcondition']
        currentcondition = Condition.objects.get(pk=currentcondition_pk)
        currentcondition_name = currentcondition.name
        result = {'name': currentcondition_name, 'pk': currentcondition_pk}
        if 'conditions' not in request.session:
            request.session['conditions'] = []
        conditions = request.session['conditions']
        conditions.append([currentcondition_pk, None])
        request.session['conditions'] = conditions
        if 'usedconditions' not in request.session:
            request.session['usedconditions'] = []
        usedconditions = request.session['usedconditions']
        usedconditions.append(currentcondition_pk)
        request.session['usedconditions'] = usedconditions
    else:
        result = {}
    return HttpResponse(json.dumps(result), mimetype)


def filter_post(request):
    conditions = []
    if 'conditions' in request.session:
        conditions = request.session['conditions']
    age = request.GET.get('age')
    if age is not int:
        age = 0
    gender = request.GET.get('gender')
