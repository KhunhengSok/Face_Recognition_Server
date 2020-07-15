from django.urls import path, include
from . import views

urlpatterns = [
    path('account/', include('face_embedding.api.account.urls')),
    path('organization/', include('face_embedding.api.organization.urls')),

    path('create', views.create, name='create'),
    path('compare', views.compare, name='compare'),
    path('update', views.update, name='update')
]
