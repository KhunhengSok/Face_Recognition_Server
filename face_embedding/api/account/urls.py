from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='signup'),
    path('user', views.user, name='signup'),
    path('organizations', views.organizations, name='signup'),

]
