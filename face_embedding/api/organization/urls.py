from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('<id>', views.show, name='show'),
    path('<id>/update', views.update, name='update'),
    path('<id>/employees', views.show_employees, name='show_employees'),
    path('<id>/events', views.show_events, name='show_events'),


    # ToDo: add employees
]
