from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-cities/', views.get_cities, name='get_cities'),
]