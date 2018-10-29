from django.urls import path
from . import views

urlpatterns = [
    path('', views.explorer, name='explorer'),
]