from django.db import models
from picklefield.fields import PickledObjectField
from django_mysql.models import ListCharField
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import gettext as _


def format_face_embedding(array):
    return ', '.join(str(ele) for ele in array)


def get_face_embedding(representation_string):
    if representation_string != '':
        r = representation_string.split(', ')
        try:
            l = list(float(ele) for ele in r)
        except ValueError:
            l = []
        return l
    else:
        return []


# Store image_url and face embedding from that url
# Many to one relationship with Person Model


# Create your models here.
# class User(User):
#     email = models.EmailField(_('email address'), blank=True, unique=True)


class Person(models.Model):
    name = models.CharField(max_length=64, null=False)
    # last_name = models.CharField(max_length=64, null=False)
    birth_of_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(editable=False, null=True)
    update_at = models.DateTimeField(null=True, )

    def save(self, *args, **kwargs):
        """On save, update the updated_at field, and set the created_at when first save"""
        if not self.id:
            self.created_at = timezone.now()
        self.update_at = timezone.now()
        return super(Person, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}. Created_at: {self.created_at}, updated_at: {self.update_at}"


class FaceEmbedding(models.Model):
    face_embedding = models.TextField(null=False, editable=True, )
    image_url = models.TextField(null=False, editable=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="face", null=False)

    def __str__(self):
        return f"Username: {self.person.first_name} Url:{self.image_url}"


class Organization(models.Model):
    name = models.CharField(max_length=64, null=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organization')
    created_at = models.DateTimeField(editable=False, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Organization, self).save(*args, **kwargs)


class Employee(models.Model):
    # declaring enum for the class
    class Role(models.TextChoices):
        MEMBER = 'member'
        ADMIN = 'admin'

    name = models.CharField(max_length=64, null=False, default='Khunheng')
    birth_of_date = models.DateField(blank=True, null=True)
    # person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='employment')
    position = models.CharField(max_length=64, null=False)
    department = models.CharField(max_length=64, null=False)
    role = models.CharField(max_length=8, default=Role.MEMBER, choices=Role.choices)
    organization = models.ForeignKey(Organization, null=False, related_name='Employee', on_delete=models.CASCADE)
    email = models.CharField(max_length=64, null=True)
    employ_date = models.DateField(null=True)
    created_at = models.DateTimeField(editable=False, null=True)
    update_at = models.DateTimeField(null=True, )

    def save(self, *args, **kwargs):
        """On save, update the updated_at field, and set the created_at when first save"""
        if not self.id:
            self.created_at = timezone.now()
        self.update_at = timezone.now()
        return super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}    Position: {self.position}. Department: {self.department}"


class Event(models.Model):
    name = models.CharField(max_length=64, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='event')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, related_name='event')
    date = models.DateField(null=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    attendees = models.ManyToManyField(Employee, related_name='event')
    # repeated_every = models.BigIntegerField(default=None)


class EventTemplate(models.Model):
    name = models.CharField(max_length=64, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='event_template')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, related_name='event_template')
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    repeated_every = models.BigIntegerField(default=None)
