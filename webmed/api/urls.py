from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('conditions/<slug:term>/', views.get_conditions_by_name,
         name='get_conditions_by_name'),
]
