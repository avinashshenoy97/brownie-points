from django.urls import path
from . import views

urlpatterns = [
    path('', views.explorer, name='explorer'),
    path('getPoolData',views.poolDataView.as_view()),
]