from django.contrib import admin
from .models import Employee, Organization, Event, EventTemplate, FaceEmbedding

# Register your models here.
admin.site.register((Employee, Organization, Event, EventTemplate, FaceEmbedding))
