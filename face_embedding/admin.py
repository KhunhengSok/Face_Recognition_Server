from django.contrib import admin
from .models import Employee, Organization, Event, EventTemplate, FaceEmbedding, Employee_Event


class Employee_Event_Admin(admin.ModelAdmin):
    fields = ['employee', 'event', 'attend_time']


# Register your models here.
admin.site.register((Employee, Organization, Event, EventTemplate, FaceEmbedding))
admin.site.register(Employee_Event, Employee_Event_Admin)


