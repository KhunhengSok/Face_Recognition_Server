from django.urls import path, include
from . import views

urlpatterns = [
    path('account/', include('face_embedding.api.account.urls')),
    path('organization/', include('face_embedding.api.organization.urls')),
    path('employee/', include('face_embedding.api.employee.urls')),
    path('event/', include('face_embedding.api.event.urls')),
    path('event-template/', include('face_embedding.api.event_template.urls')),
    path('organization/<id>/face-embedding/', include('face_embedding.api.face_embedding.urls')),


    # path('create', views.create, name='create'),
    # path('compare', views.compare, name='compare'),
    # path('update', views.update, name='update')
]
