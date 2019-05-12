from django.urls import path
from . import views

app_name = 'emergency'

urlpatterns = [
    path('', views.toolhome, name="home"),
    path('ajax/condition/search/', views.get_conditions_by_name,
         name="condition_search"),
    path('ajax/condition/selection/',
         views.get_condition_pill,
         name="selected_pill"),
]
