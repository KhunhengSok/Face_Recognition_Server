from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('<id>', views.show, name='show'),
    path('<id>/update', views.update, name='update'),
    path('<id>/delete', views.delete, name='delete'),

]
