from django.urls import path
from . import views

app_name = 'siteadmin'

urlpatterns = [
    path('', views.index, name='index'),
]
