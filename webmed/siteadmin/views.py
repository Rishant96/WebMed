from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import LoginForm
from emergency.models import Emergency, Emergency_Group
from emergency.models import Condition, Variety
from emergency.models import Presenting_Complaint


def index(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if User is not None:
            login(request, user)
            return redirect('siteadmin:home')
        else:
            pass
    return render(request, 'siteadmin/index.html', {
            'loginform': LoginForm()
        })


def home(request):
    return render(request, 'siteadmin/home.html', {
        'emergencies': Emergency.objects.all,
    })


def add_emergency(request):
    return render(request, 'siteadmin/create/emergency.html',{
            'groups': Emergency_Group.objects.all,
        })


def detail_emergency(request, pk=0):
    emergency = None
    if pk is not 0:
        emergency = Emergency.objects.get(pk=pk)
        presenting_complaints = Presenting_Complaint.objects.filter(emergency=emergency)
    return render(request, 'siteadmin/detail/emergency.html',
        {
            'emergency': emergency,
            'presenting_complaints': presenting_complaints,
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
