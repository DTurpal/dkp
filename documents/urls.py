from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_dkp, name='create_dkp'),
    path('history/', views.dkp_history, name='dkp_history'),
]