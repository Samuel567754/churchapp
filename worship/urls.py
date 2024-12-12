from django.urls import path
from . import views

urlpatterns = [
    path('sermons/', views.sermons, name='sermons'),
]
