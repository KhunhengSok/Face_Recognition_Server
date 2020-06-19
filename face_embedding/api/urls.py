from django.urls import path 
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('compare', views.compare, name='compare'),
    path('update', views.update, name='update')
]
