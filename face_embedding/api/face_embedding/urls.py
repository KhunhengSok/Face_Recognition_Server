from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('recognize', views.compare_faces, name='compare_faces'),

    # ToDo: add employees
]
