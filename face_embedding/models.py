from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

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

#
# class Person(models.Model):
#     first_name = models.CharField(max_length=64, null=False)
#     last_name = models.CharField(max_length=64, null=False)
#     # image_url = models.TextField(null=True, editable=True)
#     # face_embedding = models.TextField(null=True, editable=True,)
#
#     created_at = models.DateTimeField(editable=False, null=True)
#     update_at = models.DateTimeField(null=True)
#     # face_embedding = PickledObjectField(null=True, default=None, editable=True)
#
#     def save(self, *args, **kwargs):
#         """On save, update the updated_at field, and set the created_at when first save"""
#         if not self.id:
#             self.created_at = timezone.now()
#         self.update_at = timezone.now()
#         return super(Person,self).save(*args, **kwargs)
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}. Created_at: {self.created_at}, updated_at: {self.update_at}"


class Organization(models.Model):
    name = models.CharField(max_length=64,  unique=True, null=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organization', db_column='created_by')
    created_at = models.DateTimeField(editable=False, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Organization, self).save(*args, **kwargs)

    def to_dict(self):
        dict = {
            'name':         self.name,
            'created_by':   self.created_by,
            'created_at':   self.created_at,
        }
        return dict

    def __str__(self):
        return f'{self.name}.   Created_by: {self.created_by}'


class Employee(models.Model):
    # declaring enum for the class
    class Role(models.TextChoices):
        MEMBER = 'member'
        ADMIN = 'admin'

    name = models.CharField(max_length=64, null=False, unique=False)
    birth_of_date = models.DateField(blank=True, null=True)
    # person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='employment')
    position = models.CharField(max_length=64, null=False)
    department = models.CharField(max_length=64, null=False)
    role = models.CharField(max_length=8, default=Role.MEMBER, choices=Role.choices)
    organization = models.ForeignKey(Organization, null=False, editable=False,  related_name='employee', on_delete=models.CASCADE, db_column='organization')
    email = models.CharField(max_length=64, null=True)
    employed_date = models.DateField(null=True)
    profile_url = models.TextField(null=True, editable=True)
    created_at = models.DateTimeField(editable=False, null=True)
    updated_at = models.DateTimeField(null=True, )

    def save(self, *args, **kwargs):
        """On save, update the updated_at field, and set the created_at when first save"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}    Position: {self.position}. Department: {self.department}"


class FaceEmbedding(models.Model):
    face_embedding = models.TextField(null=False)
    image_url = models.TextField(null=False)
    owner = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="face", null=False, db_column='owner')
    created_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        """On save, update the updated_at field, and set the created_at when first save"""
        if not self.id:
            self.created_at = timezone.now()
        return super(FaceEmbedding, self).save(*args, **kwargs)

    def __str__(self):
        return f"Username: {self.owner.name} Url:{self.image_url}"


class Event(models.Model):
    name = models.CharField(max_length=64, null=False)
    created_by = models.ForeignKey(User, editable=False, on_delete=models.CASCADE, null=False, related_name='event', db_column='created_by')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, related_name='event', db_column='organization')
    date = models.DateField(null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    attendees = models.ManyToManyField(Employee, related_name='event', null=False, blank=True, through='Employee_Event')
    # repeated_every = models.BigIntegerField(default=None)


class Employee_Event(models.Model):
    event = models.ForeignKey(Event, related_name='event', null=False, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, related_name='attendee', null=False, on_delete=models.CASCADE)
    attend_time = models.TimeField(null=False, default=datetime.datetime.time(datetime.datetime.now()))

    class Meta:
        unique_together = ('event', 'employee',)


class EventTemplate(models.Model):
    name = models.CharField(max_length=64, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='event_template', db_column='created_by')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, related_name='event_template', db_column='organization', editable=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    repeated_every = models.BigIntegerField(null=True)
