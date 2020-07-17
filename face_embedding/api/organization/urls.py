from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('user', views.index, name='index'),
    path('<id>', views.show, name='index'),
    path('<id>/update', views.update, name='index'),
    # ToDo: add employees
]
