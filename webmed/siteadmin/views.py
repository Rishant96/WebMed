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
    conditions = Condition.objects.all()
    return render(request, 'siteadmin/create/emergency.html',{
            'groups': Emergency_Group.objects.all,
            'conditions': conditions,
        })


def condition_selected(request, id=0):
    return 


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
