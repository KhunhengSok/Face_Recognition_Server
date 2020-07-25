from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('<id>', views.show, name='show'),
    path('<id>/update', views.update, name='update'),
    path('<id>/delete', views.delete, name='delete'),
    path('<id>/join', views.join, name='join'),
    path('<id>/attendees', views.show_all_attendees, name='show_all_attendees'),
    path('<id>/late', views.show_late_attendees, name='show_late_attendees'),
    path('<id>/early', views.show_early_attendees, name='show_early_attendees'),
    path('<id>/absent', views.show_absent_attendees, name='show_absent_attendees'),

]
