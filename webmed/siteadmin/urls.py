from django.urls import path
from . import views

app_name = 'siteadmin'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('emergency/add/', views.add_emergency, name='addemergency'),
    path('emergency/detail/<int:pk>', views.detail_emergency, name='detailemergency')
]
