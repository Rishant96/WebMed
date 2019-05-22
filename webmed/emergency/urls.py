from django.urls import path
from . import views

app_name = 'emergency'

urlpatterns = [
    path('', views.toolhome, name="home"),
    path('ajax/condition/search/', views.get_conditions_by_name,
         name="condition_search"),
    path('ajax/condition/selection/',
         views.get_condition_variety,
         name="selected_condition"),
    path('ajax/variety/selection/',
         views.set_variety,
         name="variety_selected"),
    path('ajax/no_variety',
         views.no_variety,
         name="no_variety"),
    path('ajax/filter/get_results',
         views.filter_post,
         name='filter_post'),
    path('ajax/delete/variety',
         views.delete_variety,
         name='delete_variety'),
    path('ajax/delete/condition',
         views.delete_condition,
         name='delete_condition'),
]
