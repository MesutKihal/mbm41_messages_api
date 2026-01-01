
from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send),
]
