# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('/', views.index, name='message'),
    path('/action', views.message, name='message'),
]