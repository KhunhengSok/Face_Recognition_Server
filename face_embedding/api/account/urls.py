from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='signup'),
    path('user', views.user, name='signup'),
    path('<id>/organization', views.show_organizations, name='show_organization'),
    path('<id>', views.show, name='show'),
    # path('<id>/update', views.update, name='update'),

]
