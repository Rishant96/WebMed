from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q

import json
import requests

from .models import Emergency_Group, Emergency
from .models import Condition, Variety


site_url = 'http://127.0.0.1:8000'
mimetype = 'application/json'


# Create your views here.
def toolhome(request):
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
        if q is '':
            q = 'NOQUERY'
        if 'usedconditions' in request.session:
            pks = request.session['usedconditions']
        else:
            pks = []
        payload = {'term': q}
        data = requests.get(site_url
            + reverse('api:get_conditions_by_name',
                      kwargs=payload))
        data_json = json.loads(data.content)
        for key in data_json:
            if str(key) in pks:
                data_json.pop(str(key), None)
        data = json.dumps(data_json)
    else:
        data = 'none'
    return HttpResponse(data, mimetype)


def get_condition_variety(request):
    tag = request.GET.get('tag', '').capitalize()
    condition_var = Condition.objects.get(name=tag)

    request.session['currentcondition'] = condition_var.pk

    varieties = (Variety.objects.filter(condition=condition_var)
                 .values('name', 'pk'))

    response_data = json.dumps(list(varieties))
    return HttpResponse(response_data, mimetype)


def set_variety(request):
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


def delete_variety(request):
    variety_id = int(request.GET.get('variety_id'))
    condition_id = int(request.GET.get('condition_id'))

    conditions = request.session['conditions']
    conditions.remove([condition_id, variety_id])

    usedconditions = request.session['usedconditions']
    usedconditions.remove(condition_id)

    request.session['conditions'] = conditions
    request.session['usedconditions'] = usedconditions

    return HttpResponse('success')


def delete_condition(request):
    condition_id = int(request.GET.get('condition_id'))

    conditions = request.session['conditions']
    conditions.remove([condition_id, None])

    usedconditions = request.session['usedconditions']
    usedconditions.remove(condition_id)

    request.session['conditions'] = conditions
    request.session['usedconditions'] = usedconditions

    return HttpResponse('success')


def filter_post(request):
    conditions = []
    if 'conditions' in request.session:
        conditions = request.session['conditions']
    age = int(request.GET.get('age'))
    gender = request.GET.get('gender')
    varieties = []
    nonvarieties = []
    for condition in conditions:
        if condition[1] is not None:
            varieties.append(condition[1])
        else:
            nonvarieties.append(condition[0])
    emergencies = Emergency.objects\
        .filter(Q(varieties__pk__in=varieties)
                | Q(conditions__pk__in=nonvarieties),
                age_min__lte=age,
                age_max__gte=age,
                genders_affected__icontains=gender)\
        .distinct()\
        .values('pk', 'name')
    response_data = json.dumps(list(emergencies))
    return HttpResponse(response_data, mimetype)
